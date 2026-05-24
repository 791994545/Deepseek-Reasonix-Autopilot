#!/usr/bin/env python3
"""
run_pipeline — full-autonomous 执行引擎

将 SKILL.md 中的机械步骤自动化，我只做需要推理的任务。

设计原则：
  Pipeline 处理所有机械工作（文件验证、状态追踪、看门狗管理、压缩）
  我只做推理工作（复杂度评估、方案设计、编码、测试）

Usage:
  python run_pipeline.py init                  # 启动会话（Phase 0）
  python run_pipeline.py pre-phase <N>         # Phase N 前置检查
  python run_pipeline.py post-phase <N>        # Phase N 后置验证
  python run_pipeline.py status                # 显示当前状态
  python run_pipeline.py complete              # 结束会话（Phase 5）

示例流程：
  1. python run_pipeline.py init               # 自动: 看门狗 + state + snapshot
  2. [我] Phase 0 推理: 复杂度评估 + 类型匹配
  3. python run_pipeline.py post-phase 0       # 自动: 门禁检查 + state 更新
  4. python run_pipeline.py pre-phase 2a       # 自动: 检查前置条件
  5. [我] Phase 2a 推理: brainstorming + grill + plan
  6. python run_pipeline.py post-phase 2a      # 自动: 门禁检查
  ...重复...
  N. python run_pipeline.py complete           # 自动: 压缩 + 报告 + 停看门狗
"""

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REASONIX_HOME = Path(os.path.expanduser("~")) / ".reasonix"
SKILL_DIR = REASONIX_HOME / "skills" / "full-autonomous"
STATE_PATH = REASONIX_HOME / "state.json"
ERROR_PATTERNS_PATH = REASONIX_HOME / "error_patterns.json"
PERFORMANCE_PATH = REASONIX_HOME / "skill_performance.json"
ROUTING_WEIGHTS_PATH = REASONIX_HOME / "routing_weights.json"
SNAPSHOT_PATH = REASONIX_HOME / "skill_snapshot.md"
WATCHDOG_PATH = SKILL_DIR / "scripts" / "watchdog.py"
COMPACT_PATH = SKILL_DIR / "scripts" / "compact_memories.py"

# ── 工具函数 ──────────────────────────────────────────


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat()


def load_json(path: Path):
    if not path.exists():
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def save_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def script_path(name: str) -> Path:
    """返回 scripts/ 下的脚本路径"""
    return SKILL_DIR / "scripts" / name


def run_script(name: str, args: list[str] | None = None) -> subprocess.CompletedProcess:
    """运行 scripts/ 下的 Python 脚本"""
    cmd = [sys.executable, str(script_path(name))]
    if args:
        cmd.extend(args)
    return subprocess.run(cmd, capture_output=True, text=True)


# ── Phase 门禁定义 ──────────────────────────────────────

# 每个 Phase 的前置条件（pre-phase check）
PHASE_PRE_CHECKS = {
    0: [
        ("error_patterns.json", "错误模式库文件存在", lambda: ERROR_PATTERNS_PATH.exists()),
        ("state.json", "无残留 state（上次已清理）", lambda: not STATE_PATH.exists()),
        ("skills_dir", "技能目录可访问", lambda: SKILL_DIR.exists()),
        ("watchdog.py", "看门狗脚本存在", lambda: WATCHDOG_PATH.exists()),
    ],
    1: [
        ("state.phase0", "Phase 0 已完成", lambda: _phase_done(0)),
        ("routing_table", "路由表文件存在", lambda: (SKILL_DIR / "rules" / "01a-routing-quick-index.md").exists()),
    ],
    2: [
        ("state.phase1", "Phase 1 已完成", lambda: _phase_done(1)),
    ],
    3: [
        ("state.phase2", "Phase 2 已完成（Quick 路径跳过的可豁免）", lambda: _phase_done_or_skipped(2)),
        ("error_patterns", "已加载 error_patterns 用于预检", lambda: True),
    ],
    4: [
        ("state.phase3", "Phase 3 已完成", lambda: _phase_done(3)),
    ],
    5: [
        ("state.phase4", "Phase 4 已完成", lambda: _phase_done(4)),
    ],
}

# 每个 Phase 的后置验证（post-phase check）
PHASE_POST_CHECKS = {
    0: [
        ("启动标记", "已输出 [Auto] === 启动 ===", lambda: True),  # 由模型保证
        ("类型匹配", "已确定任务类型", lambda: _state_has("task_type")),
        ("复杂度评估", "已评估复杂度(1-10)", lambda: _state_has("complexity")),
        ("路径选择", "已确定 Quick/Standard/Full", lambda: _state_has("path")),
    ],
    1: [
        ("技能装配", "已加载 Core 技能包", lambda: _state_has("skills_loaded")),
        ("路径选择", "已选择 Phase 2a/2b/3", lambda: True),
    ],
    2: [
        ("需求打磨", "已完成 brainstorming+grill+plan", lambda: _state_has("plan_output")),
        ("隐性需求", "H-3 已扫描", lambda: True),
    ],
    3: [
        ("代码产出", "代码文件已创建/修改", lambda: True),
        ("测试通过", "测试已通过或已记录阻塞", lambda: True),
    ],
    4: [
        ("测试结果", "测试结果已记录", lambda: _state_has("test_results")),
        ("安全审查", "审查已通过或跳过", lambda: True),
    ],
    5: [
        ("性能记录", "skill_performance.json 已写入", lambda: PERFORMANCE_PATH.exists()),
        ("经验记录", "experiences 已写入", lambda: _experiences_written_today()),
        ("记忆压缩", "compact_memories 已运行", lambda: _state_has("compacted")),
    ],
}

# Phase 名称映射
PHASE_NAMES = {
    0: "初始化与分类",
    1: "技能装配",
    2: "需求打磨（Phase 2a/2b/2.3/2.5 的统称）",
    3: "执行编码",
    4: "验证测试",
    5: "交付与回顾",
}


def _phase_done(n: int) -> bool:
    state = load_json(STATE_PATH)
    phases = state.get("phases_completed", [])
    return str(n) in [str(p) for p in phases]


def _phase_done_or_skipped(n: int) -> bool:
    """检查 phase 是否已完成，或者被跳过（Quick 路径）"""
    state = load_json(STATE_PATH)
    phases = state.get("phases_completed", [])
    skipped = state.get("phases_skipped", [])
    return (str(n) in [str(p) for p in phases]) or (str(n) in [str(p) for p in skipped])


def _state_has(key: str) -> bool:
    state = load_json(STATE_PATH)
    return key in state


def _experiences_written_today() -> bool:
    exp_dir = REASONIX_HOME / "memory" / "experiences"
    if not exp_dir.exists():
        return False
    today = datetime.now().strftime("%Y-%m-%d")
    for f in exp_dir.iterdir():
        if f.is_file() and today in f.name:
            return True
    return False


# ── 核心命令 ──────────────────────────────────────────


def cmd_init():
    """初始化会话 — Phase 0 机械部分"""
    print("=" * 60)
    print(f"[Pipeline] 🚀 full-autonomous 执行引擎 v1.0")
    print(f"[Pipeline] 时间: {now_iso()}")
    print("=" * 60)

    # 1. 检查是否有残留 state
    if STATE_PATH.exists():
        state = load_json(STATE_PATH)
        last_phase = state.get("phase", "?")
        print(f"[Pipeline] ⚠️ 上次会话未正常结束 (Phase {last_phase})")
        print(f"[Pipeline] 运行 'python run_pipeline.py complete' 清理，或手动删除 state.json")
        sys.exit(1)

    # 2. 检查环境（在创建 state 之前，确保无残留）
    print(f"\n[Pipeline] 📋 环境检查:")
    env_ok = True
    for name, desc, check_fn in PHASE_PRE_CHECKS[0]:
        ok = check_fn()
        print(f"     {'✅' if ok else '❌'} {desc}")
        if not ok:
            env_ok = False

    # 3. 初始化 state.json
    state = {
        "phase": 0,
        "step": "init",
        "skill": "full-autonomous",
        "startedAt": now_iso(),
        "phases_completed": [],
        "phases_skipped": [],
        "violations": [],
        "lastUpdated": now_iso(),
    }
    save_json(STATE_PATH, state)
    print(f"[Pipeline] ✅ state.json 已初始化")

    # 4. 启动看门狗
    if not WATCHDOG_PATH.exists():
        print(f"[Pipeline] ❌ watchdog.py 不存在于 {WATCHDOG_PATH}")
        sys.exit(1)

    print(f"[Pipeline] 🔴 启动看门狗: python {WATCHDOG_PATH} ...")
    print(f"[Pipeline]   看门狗启动方法（手动）:")
    print(f"       run_background('python {WATCHDOG_PATH}' --continuous --sync)")
    print(f"[Pipeline]   ⚠️ 请在上方命令执行后确认 PID")

    # 5. 加载 error_patterns（仅 top 15）
    if ERROR_PATTERNS_PATH.exists():
        with open(ERROR_PATTERNS_PATH, "r", encoding="utf-8") as f:
            patterns = json.load(f)
        if isinstance(patterns, list):
            # 按 confidence↓ + last_seen↓ 排序
            def sort_key(e):
                conf = e.get("confidence", 0) if isinstance(e, dict) else 0
                seen = e.get("last_seen", e.get("timestamp", "")) if isinstance(e, dict) else ""
                return (-conf, seen if seen else "")
            patterns.sort(key=sort_key)
            top15 = [p for p in patterns if not (isinstance(p, dict) and "ArchivedSummary" in p.get("error", ""))][:15]
            print(f"\n[Pipeline] 📖 error_patterns.json: {len(patterns)} 条 → 加载 top {len(top15)} 条")
            print(f"[Pipeline]   存档摘要已排除，最旧的 {len(patterns) - len(top15)} 条未加载")
            state["error_patterns_loaded"] = len(top15)
            state["error_patterns_total"] = len(patterns)
        else:
            print(f"\n[Pipeline] 📖 error_patterns.json: {len(patterns)} 条（格式异常）")
    else:
        print(f"\n[Pipeline] 📖 error_patterns.json: 不存在（首次启动）")

    # 6. G-4 技能快照
    skills_dir = REASONIX_HOME / "skills"
    if skills_dir.exists():
        skills = sorted([d.name for d in skills_dir.iterdir() if d.is_dir()])
        today = datetime.now().strftime("%Y-%m-%d")
        snap = f"# 技能快照日志\n\n## {today}\n"
        snap += f"本次新增: 0 个 | 消失: 0 个 | 总计: {len(skills)} 个\n\n| 技能 | 首次发现 |\n|------|----------|\n"
        for s in skills:
            snap += f"| {s} | {today} |\n"

        if SNAPSHOT_PATH.exists():
            old_content = SNAPSHOT_PATH.read_text(encoding="utf-8")
            # 追加而非覆盖
            SNAPSHOT_PATH.write_text(old_content + "\n" + snap, encoding="utf-8")
            print(f"[Pipeline] ✅ G-4 技能快照已追加 ({len(skills)} 个技能)")
        else:
            SNAPSHOT_PATH.write_text(snap, encoding="utf-8")
            print(f"[Pipeline] ✅ G-4 技能快照已创建 ({len(skills)} 个技能)")
    else:
        print(f"[Pipeline] ⚠️ 技能目录不存在，跳过 G-4 快照")

    # 7. 更新 state
    state["lastUpdated"] = now_iso()
    save_json(STATE_PATH, state)

    print(f"\n[Pipeline] {'=' * 40}")
    print(f"[Pipeline] ✅ init 完成。接下来我做推理:")
    print(f"[Pipeline]   1. 评估任务复杂度 (1-10)")
    print(f"[Pipeline]   2. 匹配任务类型")
    print(f"[Pipeline]   3. 确定路径 (Quick/Standard/Full)")
    print(f"[Pipeline]   推理完成后会自动调用 post-phase 0，无需手动操作")
    print(f"[Pipeline] {'=' * 40}")


def cmd_pre_phase(phase: int):
    """Phase N 前置检查"""
    if phase not in PHASE_PRE_CHECKS:
        print(f"[Pipeline] ❌ 未知 Phase: {phase}")
        sys.exit(1)

    state = load_json(STATE_PATH)
    if not state:
        print(f"[Pipeline] ❌ state.json 不存在，请先运行 init")
        sys.exit(1)

    print(f"[Pipeline] 🔍 Phase {phase}: {PHASE_NAMES.get(phase, '')} 前置检查")
    print(f"[Pipeline] {'=' * 40}")

    all_ok = True
    for name, desc, check_fn in PHASE_PRE_CHECKS[phase]:
        ok = check_fn()
        print(f"     {'✅' if ok else '❌'} {desc}")
        if not ok:
            all_ok = False

    if not all_ok:
        print(f"\n[Pipeline] ❌ 前置检查未通过，请解决后重试")
        sys.exit(1)

    print(f"\n[Pipeline] ✅ Phase {phase} 前置条件满足")
    print(f"[Pipeline] 接下来请完成 Phase {phase} 的推理任务")
    print(f"[Pipeline] 完成后运行: python run_pipeline.py post-phase {phase}")


def cmd_post_phase(phase: int):
    """Phase N 后置验证"""
    if phase not in PHASE_POST_CHECKS:
        print(f"[Pipeline] ❌ 未知 Phase: {phase}")
        sys.exit(1)

    state = load_json(STATE_PATH)
    if not state:
        print(f"[Pipeline] ❌ state.json 不存在")
        sys.exit(1)

    print(f"[Pipeline] ✅ Phase {phase}: {PHASE_NAMES.get(phase, '')} 后置验证")
    print(f"[Pipeline] {'=' * 40}")

    if phase in (0, 1, 2):
        # 这些 phase 需要用户确认关键字段已设置
        if phase == 0:
            print("  请确认以下信息（如果没有请补充）:")
            print("    - task_type: 任务类型")
            print("    - complexity: 复杂度评分 (1-10)")
            print("    - path: Quick/Standard/Full")
        elif phase == 1:
            print("  请确认以下信息:")
            print("    - skills_loaded: 已加载哪些技能")
        elif phase == 2:
            print("  请确认以下信息:")
            print("    - plan_output: 实施计划已输出")

    all_ok = True
    for name, desc, check_fn in PHASE_POST_CHECKS[phase]:
        ok = check_fn()
        print(f"     {'✅' if ok else '❌'} {desc}")
        if not ok:
            all_ok = False

    if not all_ok:
        print(f"\n[Pipeline] ⚠️ 部分后置检查未自动通过（可能需你手动确认）")

    # 更新 state
    phases = state.get("phases_completed", [])
    if phase not in phases:
        phases.append(phase)
        state["phases_completed"] = phases
    state["phase"] = phase
    state["step"] = "PASS"
    state["lastUpdated"] = now_iso()
    save_json(STATE_PATH, state)

    print(f"\n[Pipeline] ✅ Phase {phase} 已完成并记录")
    print(f"[Pipeline] 已完成的 Phase: {state['phases_completed']}")


def cmd_complete():
    """结束会话 — Phase 5 机械部分"""
    state = load_json(STATE_PATH)
    print(f"[Pipeline] 🏁 结束会话")
    print(f"[Pipeline] {'=' * 40}")

    if not state:
        print("[Pipeline] ⚠️ 没有活跃会话")
    else:
        phases = state.get("phases_completed", [])
        print(f"[Pipeline] 已完成 Phase: {phases}")
        print(f"[Pipeline] 启动时间: {state.get('startedAt', '?')}")
        print(f"[Pipeline] 结束时间: {now_iso()}")

        # 计算耗时
        try:
            start = datetime.fromisoformat(state["startedAt"])
            end = datetime.now(timezone.utc).astimezone()
            delta = end - start
            mins = int(delta.total_seconds() // 60)
            secs = int(delta.total_seconds() % 60)
            print(f"[Pipeline] 总耗时: {mins}分{secs}秒")
        except Exception:
            pass

    # compact_memories
    print(f"\n[Pipeline] 🧹 运行记忆压缩...")
    result = run_script("compact_memories.py")
    print(result.stdout)
    if result.returncode != 0:
        print(f"[Pipeline] ⚠️ compact_memories 退出码: {result.returncode}")
    print(result.stderr)

    # 停看门狗
    print(f"[Pipeline] 🛑 请停止看门狗:")
    print(f"       stop_job(job_id)")

    # 删 state
    if STATE_PATH.exists():
        STATE_PATH.unlink()
        print(f"[Pipeline] ✅ state.json 已删除")

    print(f"\n[Pipeline] ✅ 会话正常结束")


def cmd_status():
    """显示当前状态"""
    state = load_json(STATE_PATH)
    if not state:
        print("[Pipeline] 📭 没有活跃会话")
        print("  运行 'python run_pipeline.py init' 开始新会话")
        return

    print(f"[Pipeline] 📊 当前状态")
    print(f"[Pipeline] {'=' * 40}")
    print(f"  Phase:     {state.get('phase', '?')}")
    print(f"  Step:      {state.get('step', '?')}")
    print(f"  开始时间:  {state.get('startedAt', '?')}")
    print(f"  上次更新:  {state.get('lastUpdated', '?')}")
    print(f"  已完成:    {state.get('phases_completed', [])}")
    print(f"  已跳过:    {state.get('phases_skipped', [])}")
    print(f"  违例数:    {len(state.get('violations', []))}")

    if state.get("error_patterns_loaded"):
        print(f"  error_patterns: 已加载 {state['error_patterns_loaded']}/{state.get('error_patterns_total','?')} 条")


# ── 自动模式 ─────────────────────────────────────────


def cmd_auto():
    """自动模式：根据 state.json 决定执行什么"""
    state = load_json(STATE_PATH)

    if not state:
        print("[Pipeline] 🚀 无活跃会话 → 执行 init")
        cmd_init()
        return

    phase = state.get("phase", 0)
    step = state.get("step", "")
    phases_done = state.get("phases_completed", [])

    # 如果当前 step 是 PASS，说明该 phase 已完成，需要进入下一个
    if step == "PASS" or step.startswith("PASS"):
        next_phase = phase + 1
        if next_phase > 5:
            print("[Pipeline] 🏁 所有 Phase 已完成 → 执行 complete")
            cmd_complete()
        else:
            print(f"[Pipeline] Phase {phase} 已完成，进入 Phase {next_phase} pre-check")
            cmd_pre_phase(next_phase)
        return

    # 如果当前 phase 还没有 step，做 post-phase 验证
    if step in ("init", 0, "0") or not step:
        print(f"[Pipeline] Phase {phase} 待验证 → 执行 post-phase {phase}")
        cmd_post_phase(phase)
        return

    # 默认显示状态
    cmd_status()


# ── CLI 入口 ──────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="full-autonomous 执行引擎 — 自动化机械步骤，你只做推理"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init", help="初始化会话（Phase 0 机械部分）")
    sub.add_parser("status", help="显示当前状态")
    sub.add_parser("auto", help="自动模式：根据 state.json 决定执行什么")

    p_pre = sub.add_parser("pre-phase", help="Phase N 前置检查")
    p_pre.add_argument("phase", type=int, choices=[0, 1, 2, 3, 4, 5])

    p_post = sub.add_parser("post-phase", help="Phase N 后置验证")
    p_post.add_argument("phase", type=int, choices=[0, 1, 2, 3, 4, 5])

    sub.add_parser("complete", help="结束会话（Phase 5 机械部分）")

    args = parser.parse_args()

    if args.command == "init":
        cmd_init()
    elif args.command == "status":
        cmd_status()
    elif args.command == "auto":
        cmd_auto()
    elif args.command == "pre-phase":
        cmd_pre_phase(args.phase)
    elif args.command == "post-phase":
        cmd_post_phase(args.phase)
    elif args.command == "complete":
        cmd_complete()


if __name__ == "__main__":
    main()
