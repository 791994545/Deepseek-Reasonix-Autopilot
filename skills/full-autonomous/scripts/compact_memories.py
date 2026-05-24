#!/usr/bin/env python3
"""
compact_memories — 记忆压缩与裁剪引擎

防止 error_patterns.json / skill_performance.json / experiences 无限增长。
每次 Phase 5 结束时自动运行，保持上下文可管理。

策略:
  - error_patterns.json: 保留 top 20 条（按 confidence↓ + recency↓），
    超出的低 confidence 旧记录 → 归档到 summary 条目
  - skill_performance.json: 保留最近 20 条
  - memory/experiences/: 保留最近 20 个文件，旧文件合并为月度摘要

Usage:
  python compact_memories.py              # 正常执行
  python compact_memories.py --dry-run    # 预览但不修改
  python compact_memories.py --force      # 即使未超阈值也执行
"""

import argparse
import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path

REASONIX_HOME = Path(os.path.expanduser("~")) / ".reasonix"

# ── 阈值配置 ──────────────────────────────────────────
MAX_ERROR_PATTERNS = 20       # error_patterns.json 硬上限
MAX_PERFORMANCE = 20          # skill_performance.json 上限
MAX_EXPERIENCES = 20          # experiences 文件数上限
ARCHIVE_SUMMARY_MAX = 5       # 归档摘要中最多保留几条 old 记录


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat()


def load_json(path: Path):
    if not path.exists():
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def save_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ── 1. 压缩 error_patterns.json ─────────────────────


def compact_error_patterns(dry_run: bool = False, force: bool = False) -> dict:
    """
    保留 top N 条，超出的做归档。
    排序: confidence 降序 → last_seen 降序
    """
    path = REASONIX_HOME / "error_patterns.json"
    patterns = load_json(path)
    if not patterns:
        return {"file": "error_patterns.json", "before": 0, "after": 0, "archived": 0}

    before = len(patterns)
    if before <= MAX_ERROR_PATTERNS and not force:
        return {"file": "error_patterns.json", "before": before, "after": before, "archived": 0}

    # 提取 ProtocolViolation（不进排序）
    protocol_violations = [p for p in patterns if isinstance(p, dict) and p.get("error", "").startswith("ProtocolViolation")]
    normal_patterns = [p for p in patterns if p not in protocol_violations]

    # 排序: confidence↓, last_seen↓（没有 last_seen 的排最后）
    def sort_key(e):
        conf = e.get("confidence", 0) if isinstance(e, dict) else 0
        seen = e.get("last_seen", e.get("timestamp", "")) if isinstance(e, dict) else ""
        return (-conf, seen if seen else "")

    normal_patterns.sort(key=sort_key)

    # 保留 top N
    keep = normal_patterns[:MAX_ERROR_PATTERNS]
    archive = normal_patterns[MAX_ERROR_PATTERNS:]

    # 归档旧记录 → 摘要条目
    archived_count = len(archive)
    if archived_count > 0:
        summary = {
            "timestamp": now_iso(),
            "error": f"ArchivedSummary ({archived_count} old patterns compressed)",
            "context": "自动归档：低 confidence / 过时的错误模式",
            "archive_count": archived_count,
            "oldest": archive[-1].get("timestamp", archive[-1].get("last_seen", "unknown")) if archive else "unknown",
            "newest_in_archive": archive[0].get("timestamp", archive[0].get("last_seen", "unknown")) if archive else "unknown",
            "confidence": 0.3,  # 归档摘要的 confidence 很低，不会被优先加载
            "archived_at": now_iso(),
        }
        keep.insert(0, summary)

    # 重新加入 ProtocolViolation
    result = protocol_violations + keep
    after = len(result)

    if not dry_run:
        save_json(path, result)
        # 把归档的详细记录写到单独的存档文件
        if archived_count > 0:
            archive_path = REASONIX_HOME / "error_patterns_archive.jsonl"
            with open(archive_path, "a", encoding="utf-8") as f:
                for entry in archive:
                    f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    return {
        "file": "error_patterns.json",
        "before": before,
        "after": after,
        "archived": archived_count,
        "action": "dry-run" if dry_run else "compressed",
    }


# ── 2. 压缩 skill_performance.json ──────────────────


def compact_performance(dry_run: bool = False, force: bool = False) -> dict:
    path = REASONIX_HOME / "skill_performance.json"
    records = load_json(path)
    if not records:
        return {"file": "skill_performance.json", "before": 0, "after": 0, "archived": 0}

    before = len(records)
    if before <= MAX_PERFORMANCE and not force:
        return {"file": "skill_performance.json", "before": before, "after": before, "archived": 0}

    # 按 timestamp 排序保留最新的
    records.sort(key=lambda r: r.get("timestamp", ""), reverse=True)
    keep = records[:MAX_PERFORMANCE]
    archived = len(records) - len(keep)

    if not dry_run:
        save_json(path, keep)

    return {
        "file": "skill_performance.json",
        "before": before,
        "after": len(keep),
        "archived": archived,
        "action": "dry-run" if dry_run else "compressed",
    }


# ── 3. 压缩 experiences ──────────────────────────────


def compact_experiences(dry_run: bool = False, force: bool = False) -> dict:
    exp_dir = REASONIX_HOME / "memory" / "experiences"
    if not exp_dir.exists():
        return {"file": "experiences", "before": 0, "after": 0, "archived": 0}

    files = sorted(
        [f for f in exp_dir.iterdir() if f.is_file() and f.name.endswith(".md") and f.name != "README.md"],
        key=lambda f: f.stat().st_mtime,
        reverse=True,  # 最新的在前
    )

    before = len(files)
    if before <= MAX_EXPERIENCES and not force:
        return {"file": "experiences", "before": before, "after": before, "archived": 0}

    keep = files[:MAX_EXPERIENCES]
    archive = files[MAX_EXPERIENCES:]

    if not dry_run and archive:
        # 将过期的经验合并为一个摘要文件
        archive_dir = exp_dir / "_archived"
        archive_dir.mkdir(exist_ok=True)

        summary_lines = ["# Archived Experience Summary\n",
                         f"> 自动归档于 {now_iso()}\n",
                         f"> 合并 {len(archive)} 条旧经验\n\n"]

        for f in archive:
            try:
                content = f.read_text(encoding="utf-8", errors="replace")
                summary_lines.append(f"---\n## {f.stem}\n\n{content}\n")
            except Exception:
                pass
            # 删除原文件
            f.unlink()

        # 写入归档摘要
        summary_path = archive_dir / f"archived-{datetime.now().strftime('%Y%m')}.md"
        summary_path.write_text("".join(summary_lines), encoding="utf-8")

    return {
        "file": "experiences",
        "before": before,
        "after": len(keep),
        "archived": len(archive),
        "action": "dry-run" if dry_run else "compressed",
    }


# ── 4. 清理 skill_snapshot.md（只留最近 50 行）───────


def compact_snapshot(dry_run: bool = False, force: bool = False) -> dict:
    path = REASONIX_HOME / "skill_snapshot.md"
    if not path.exists():
        return {"file": "skill_snapshot.md", "before": 0, "after": 0, "archived": 0}

    content = path.read_text(encoding="utf-8", errors="replace")
    lines = content.splitlines()
    before = len(lines)

    if before <= 50 and not force:
        return {"file": "skill_snapshot.md", "before": before, "after": before, "archived": 0}

    # 保留标题行 + 最近 40 行数据
    header_lines = []
    for line in lines:
        header_lines.append(line)
        if line.startswith("| 技能 |"):
            break

    data_lines = [l for l in lines if l.startswith("|")]
    if len(data_lines) > 40:
        # 保留最近 40 条快照（去掉最早的）
        data_lines = data_lines[-40:]

    result = header_lines + [""] + data_lines
    after = len(result)

    if not dry_run:
        path.write_text("\n".join(result), encoding="utf-8")

    return {
        "file": "skill_snapshot.md",
        "before": before,
        "after": after,
        "archived": before - after,
        "action": "dry-run" if dry_run else "compressed",
    }


# ── 主入口 ────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="记忆压缩与裁剪引擎")
    parser.add_argument("--dry-run", "-n", action="store_true", help="预览但不修改")
    parser.add_argument("--force", "-f", action="store_true", help="即使未超阈值也执行")
    args = parser.parse_args()

    label = "🔍 DRY RUN" if args.dry_run else "🧹 COMPACT"
    print(f"[{label}] 开始记忆压缩\n")

    results = [
        compact_error_patterns(dry_run=args.dry_run, force=args.force),
        compact_performance(dry_run=args.dry_run, force=args.force),
        compact_experiences(dry_run=args.dry_run, force=args.force),
        compact_snapshot(dry_run=args.dry_run, force=args.force),
    ]

    total_archived = 0
    for r in results:
        action = r.get("action", "checked")
        archived = r.get("archived", 0)
        total_archived += archived
        if archived > 0:
            print(f"  {r['file']}: {r['before']} → {r['after']} 条 ({archived} 条已归档) [{action}]")
        else:
            print(f"  {r['file']}: {r['before']} 条 (无需压缩)")

    print(f"\n[{label}] 完成 — 共处理 {total_archived} 条过时记录")
    if total_archived == 0:
        print("    所有文件均在阈值内，无需压缩。")


if __name__ == "__main__":
    main()
