#!/usr/bin/env python3
"""
full-autonomous v1.0 看门狗 + 自动进化引擎

三层功能：
  1. 协议遵循度检查 — [Auto] 前缀 / Phase 门禁 / 心跳 / 挂起命令 / 危险操作
  2. 🔴 自动进化引擎 — 检测 "❌错误 → ✅修复" 的模式，自动写入 error_patterns.json
  3. 违例同步 — 持续模式下一经检测自动入库

启动方式:
  python watchdog.py --logfile <path> [--continuous] [--interval 30]

退出码：
  0 = 合规
  1 = 存在违例
  124 = 内部错误
"""

import argparse
import io
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# Windows GBK 终端兼容
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# ── 路径配置 ──────────────────────────────────────────────
REASONIX_HOME = Path(os.path.expanduser("~")) / ".reasonix"
ERROR_PATTERNS_PATH = REASONIX_HOME / "error_patterns.json"
ROUTING_WEIGHTS_PATH = REASONIX_HOME / "routing_weights.json"
STATE_PATH = REASONIX_HOME / "state.json"


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat()


def load_json(path: Path) -> list | dict:
    """安全加载 JSON，文件不存在或损坏返回空结构"""
    if not path.exists():
        return [] if path.name == "error_patterns.json" else {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return [] if path.name == "error_patterns.json" else {}


def save_json(path: Path, data: list | dict) -> None:
    """安全写入 JSON"""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ── 消息解析 ──────────────────────────────────────────────


def parse_messages(logfile: str | None) -> list[str]:
    """从日志文件解析消息列表"""
    messages: list[str] = []
    if logfile and os.path.isfile(logfile):
        with open(logfile, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        lines = content.splitlines()
        current_msg = ""
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("[") and current_msg:
                messages.append(current_msg.strip())
                current_msg = stripped
            elif stripped.startswith("["):
                current_msg = stripped
            else:
                current_msg += "\n" + stripped
        if current_msg.strip():
            messages.append(current_msg.strip())
    return messages


# ── 协议检查函数 ──────────────────────────────────────────


def has_auto_prefix(messages: list[str]) -> bool:
    for msg in messages[-5:]:
        if re.search(r"^\s*\[Auto\]", msg, re.MULTILINE):
            return True
    return False


def has_phase_passed(messages: list[str]) -> bool:
    for msg in messages:
        if "=== Phase" in msg and "PASSED ===" in msg:
            return True
    return False


def has_task_call(messages: list[str]) -> bool:
    for msg in messages:
        if re.search(r"\bexplore\b", msg) or re.search(r"\btask-executor\b", msg):
            return True
    return False


def has_heartbeat(messages: list[str]) -> bool:
    for msg in messages[-10:]:
        if re.search(r"^\s*\[心跳\]", msg, re.MULTILINE):
            return True
    return False


HANGING_PATTERNS = [
    (r"Start-Process.*-NoNewWindow(?!.*-RedirectStandardOutput)",
     "Start-Process -NoNewWindow 缺少 -RedirectStandardOutput"),
    (r"Start-Process.*python.*main(?!.*-RedirectStandardOutput)",
     "Start-Process python main.py 无输出重定向"),
    (r"(?<!\w)(?:uvicorn|gunicorn|waitress-serve)\s+\S+",
     "裸启动 ASGI/WSGI 服务器，未用 run_background"),
    (r"(?<!\w)(?:npm start|npm run dev|yarn start|yarn dev)(?!\s*;)",
     "裸启动前端 dev server，未用 run_background"),
    (r"(?<!\w)python\s+(?:main|app|server|api)\.\w+",
     "裸启动 Python 服务器脚本，未用 run_background"),
]


def detect_hanging_command(message: str) -> str | None:
    for pattern, reason in HANGING_PATTERNS:
        if re.search(pattern, message):
            return reason
    return None


DANGEROUS_PATTERNS = [
    r"Remove-Item\s+-Recurse", r"rm\s+-[rf]+\s", r"DROP\s+TABLE",
    r"git\s+push\s+--force", r"Format-Volume",
    r"del\s+/[fqs]*\s", r"rd\s+/[sq]*\s",
]


def has_dangerous_command(message: str) -> bool:
    return any(re.search(p, message) for p in DANGEROUS_PATTERNS)


def has_danger_label_preceding(messages: list[str], idx: int) -> bool:
    start = max(0, idx - 2)
    return any("<danger>" in messages[i] for i in range(start, idx))


def get_current_phase(messages: list[str]) -> int | None:
    for msg in reversed(messages[-10:]):
        m = re.search(r"Phase\s+(\d)", msg)
        if m:
            return int(m.group(1))
    return None


def get_current_step(messages: list[str]) -> str | None:
    for msg in reversed(messages[-5:]):
        m = re.search(r"STEP\s+(\d+\.?\d*)", msg)
        if m:
            return m.group(1)
    return None


# ── 🔴 自动进化引擎 ──────────────────────────────────


# 错误指示器：消息中包含这些模式说明发生了错误
ERROR_INDICATORS = [
    r"❌\s*错误", r"❌\s*Error", r"❌\s*失败", r"❌\s*failed",
    r"Error:", r"Traceback", r"UnicodeEncodeError", r"UnicodeDecodeError",
    r"exit code \d+", r"exit 1", r"exit \d+",
    r"❌",  # 通用的 ❌ 前缀（宽松匹配）
]

# 修复指示器：消息中包含这些模式说明做了修复
FIX_INDICATORS = [
    r"fix", r"fixed", r"修复", r"已修", r"已解决", r"已修复",
    r"已更正", r"修正", r"已改", r"已调整", r"已处理",
    r"edit_file", r"multi_edit", r"written", r"已写入",
]

# 上下文提取正则：从消息中提取文件名/组件名
CONTEXT_EXTRACTORS = [
    r"❌\s*错误:\s*(.+?)(?:$|\n)",       # ❌ 错误: xxx
    r"Error:\s*(.+?)(?:$|\n)",           # Error: xxx
    r"(?:File|文件)\s*[\"']?([^\"'\s]+)", # 文件名
    r"Unicode\w*Error:\s*(.+)",          # UnicodeError detail
]


class AutoEvolutionEngine:
    """自动进化引擎 — 检测修复事件并记录到 error_patterns.json"""

    def __init__(self):
        # 记录上次扫描时看到的最后一条消息
        self._last_scanned: int = 0

    def scan_and_evolve(self, messages: list[str]) -> list[dict]:
        """
        扫描消息，检测 "错误→修复" 事件。
        返回本次新记录的 error patterns 列表。
        """
        if len(messages) <= self._last_scanned:
            return []

        new_messages = messages[self._last_scanned:]
        self._last_scanned = len(messages)

        # 查找错误消息
        error_indices: list[int] = []
        for i, msg in enumerate(new_messages):
            if any(re.search(pat, msg, re.IGNORECASE) for pat in ERROR_INDICATORS):
                error_indices.append(i)

        if not error_indices:
            return []

        # 查找修复消息（错误之后）
        fix_indices: list[int] = []
        for err_idx in error_indices:
            for j in range(err_idx + 1, len(new_messages)):
                if any(re.search(pat, new_messages[j], re.IGNORECASE) for pat in FIX_INDICATORS):
                    fix_indices.append(j)
                    break

        if not fix_indices:
            return []

        # 提取错误描述和修复方案
        new_records: list[dict] = []
        for err_idx, fix_idx in zip(error_indices[:len(fix_indices)], fix_indices):
            err_msg = new_messages[err_idx]
            fix_msg = new_messages[fix_idx]

            # 提取错误描述
            error_desc = "未知错误"
            for extractor in CONTEXT_EXTRACTORS:
                m = re.search(extractor, err_msg)
                if m:
                    error_desc = m.group(1).strip()[:120]
                    break

            # 提取修复方案
            fix_desc = "参见修复消息"
            # 尝试从 fix 消息中提取 edit_file 的内容
            edit_match = re.search(r'```[\s\S]{0,500}?======[\s\S]{0,500}?```', fix_msg)
            if edit_match:
                fix_desc = "代码修改 (SEARCH/REPLACE)"

            # 提取技能名（如果有 skill_id 上下文）
            skill_id = "full-autonomous"
            phase = get_current_phase(messages) or 0

            # 检查是否已存在同类模式
            patterns = load_json(ERROR_PATTERNS_PATH)
            pattern_list = patterns if isinstance(patterns, list) else patterns.get("errors", [])

            duplicate = False
            for existing in pattern_list:
                if isinstance(existing, dict) and error_desc[:40] in existing.get("error", ""):
                    # 同类错误 → 提升 confidence
                    existing["confidence"] = min(1.0, existing.get("confidence", 0.5) + 0.1)
                    existing["last_seen"] = now_iso()
                    duplicate = True
                    new_records.append({
                        "action": "merged",
                        "error": existing["error"][:60],
                        "confidence": existing["confidence"],
                    })
                    print(f"[进化] ⬆ 已有模式提升 confidence → {existing['confidence']}: {error_desc[:50]}")
                    break

            if not duplicate:
                new_entry = {
                    "timestamp": now_iso(),
                    "error": error_desc,
                    "context": f"自动检测于 Phase {phase}: {err_msg[:100]}",
                    "fix": fix_desc,
                    "prevention": f"见上下文: {fix_msg[:100]}",
                    "confidence": 0.7,
                    "skill_id": skill_id,
                    "phase": phase,
                    "last_seen": now_iso(),
                }
                pattern_list.append(new_entry)
                new_records.append({
                    "action": "added",
                    "error": error_desc[:60],
                    "confidence": 0.7,
                })
                print(f"[进化] 🆕 自动记录错误模式 (conf=0.7): {error_desc[:50]}")

            # 写回
            if isinstance(patterns, list):
                save_json(ERROR_PATTERNS_PATH, patterns)
            else:
                patterns["errors"] = pattern_list
                save_json(ERROR_PATTERNS_PATH, patterns)

            # 更新 routing_weights
            self._update_routing_weights(skill_id, new_records)

        return new_records

    def _update_routing_weights(self, skill_id: str, records: list[dict]) -> None:
        """根据新错误更新路由权重"""
        weights = load_json(ROUTING_WEIGHTS_PATH)
        if "weights" not in weights:
            weights["weights"] = {}

        for rec in records:
            if rec.get("action") == "added":
                penalty = 0.1  # 新错误 conf=0.7 → penalty=0.1
                weights["weights"][skill_id] = {
                    "weight_penalty": min(weights["weights"].get(skill_id, {}).get("weight_penalty", 0) + penalty, 0.3),
                    "last_error": rec["error"],
                    "last_error_time": now_iso(),
                }
                print(f"[进化] ⚖ routing_weights 已更新: {skill_id} penalty={weights['weights'][skill_id]['weight_penalty']}")

        save_json(ROUTING_WEIGHTS_PATH, weights)


# ── 协议检查 ──────────────────────────────────────────


def run_compliance_check(messages: list[str]) -> list[dict]:
    """执行协议遵循度检查"""
    violations: list[dict] = []

    if not messages:
        return violations

    current_phase = get_current_phase(messages)
    current_step = get_current_step(messages)

    # Layer 1: 格式
    if not has_auto_prefix(messages):
        violations.append({"type": "missing_auto_prefix", "severity": "L1",
                           "detail": "最近 5 条消息中无 [Auto] 前缀",
                           "phase": current_phase, "step": current_step})

    if current_phase and current_phase > 0 and not has_phase_passed(messages):
        violations.append({"type": "missing_phase_passed", "severity": "L1",
                           "detail": f"Phase {current_phase} 已开始但无 PASSED 标记",
                           "phase": current_phase, "step": current_step})

    if current_phase == 3 and not has_task_call(messages):
        violations.append({"type": "missing_task_call", "severity": "L2",
                           "detail": "Phase 3 但未检测到子代理调用",
                           "phase": current_phase, "step": current_step})

    if current_phase and 2 <= current_phase <= 4 and len(messages) >= 8 and not has_heartbeat(messages):
        violations.append({"type": "missing_heartbeat", "severity": "L3",
                           "detail": "长时间运行但无心跳",
                           "phase": current_phase, "step": current_step})

    for i, msg in enumerate(messages):
        hang_reason = detect_hanging_command(msg)
        if hang_reason:
            surrounding = " ".join(messages[max(0, i-2):min(len(messages), i+3)])
            if "run-with-timeout" not in surrounding:
                violations.append({"type": "hanging_command", "severity": "L2",
                                   "detail": hang_reason, "phase": current_phase, "step": current_step})

        if has_dangerous_command(msg) and not has_danger_label_preceding(messages, i):
            violations.append({"type": "missing_danger_label", "severity": "L2",
                               "detail": f"危险命令前无 <danger> 标签: {msg[:80]}",
                               "phase": current_phase, "step": current_step})

    if violations:
        print(f"[看门狗] ⚠️ {len(violations)} 项协议偏离:")
        for v in violations:
            print(f"  - [{v['severity']}] {v['detail']}")
    else:
        print("[看门狗] ✅ 协议检查通过")

    return violations


def sync_violations(violations: list[dict]) -> None:
    """同步违例到 error_patterns.json"""
    if not violations:
        return
    patterns = load_json(ERROR_PATTERNS_PATH)
    pattern_list = patterns if isinstance(patterns, list) else patterns.get("errors", [])

    entry = {
        "timestamp": now_iso(),
        "error": f"ProtocolViolation ({len(violations)} items)",
        "detail": [v["detail"] for v in violations],
        "severity": max(v["severity"] for v in violations),
        "confidence": 0.7,
        "skill_id": "full-autonomous",
        "phase": max(v["phase"] or 0 for v in violations),
    }
    pattern_list.append(entry)

    if isinstance(patterns, list):
        save_json(ERROR_PATTERNS_PATH, patterns)
    else:
        patterns["errors"] = pattern_list
        save_json(ERROR_PATTERNS_PATH, patterns)
    print(f"[看门狗] 已同步 {len(violations)} 条违例到 error_patterns.json")

    # 写反馈文件 → 下次 init 时读取
    summary = {
        "last_scan": now_iso(),
        "violations_count": len(violations),
        "latest": violations[-1]["detail"] if violations else "",
    }
    save_json(REASONIX_HOME / "violation_summary.json", summary)


# ── CLI 主入口 ──────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="full-autonomous 看门狗 + 自动进化")
    parser.add_argument("--logfile", "-l", default="", help="日志文件路径")
    parser.add_argument("--continuous", "-c", action="store_true", help="持续监控")
    parser.add_argument("--interval", "-i", type=int, default=30, help="扫描间隔（秒）")
    parser.add_argument("--sync", "-s", action="store_true", help="违例同步到 error_patterns.json")
    args = parser.parse_args()

    # 初始化进化引擎（跨扫描保留状态）
    evolution_engine = AutoEvolutionEngine()

    if args.continuous:
        print(f"[看门狗] 持续监控模式启动 (每 {args.interval} 秒)")
        print(f"[看门狗] 自动进化引擎已启用 — 检测修复事件自动入库")
        while True:
            messages = parse_messages(args.logfile)
            violations = run_compliance_check(messages)
            if args.sync:
                sync_violations(violations)
            # 🔴 自动进化：检测修复事件
            evolution_engine.scan_and_evolve(messages)
            time.sleep(args.interval)
    else:
        messages = parse_messages(args.logfile)
        if not messages:
            print("[看门狗] ℹ️ 没有日志输入，跳过检查")
            print("[看门狗] 使用 --logfile 指定日志文件路径")
            sys.exit(0)
        violations = run_compliance_check(messages)
        if args.sync:
            sync_violations(violations)
        # 🔴 单次进化扫描
        evolution_engine.scan_and_evolve(messages)
        sys.exit(1 if violations else 0)


if __name__ == "__main__":
    main()
