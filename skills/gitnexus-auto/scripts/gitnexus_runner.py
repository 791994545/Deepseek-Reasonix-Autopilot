"""GitNexus 自动分析辅助脚本 - 供 CodeBuddy AI 调用"""

import json
import subprocess
import sys
from pathlib import Path

GITNEXUS = str(Path(r"D:\npm-global\gitnexus.cmd"))


def run_cmd(cmd: list[str], cwd: str | None = None) -> dict:
    """运行 gitnexus 命令并返回结构化结果"""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=120,
            encoding="utf-8",
            errors="replace",
        )
        stdout = result.stdout
        json_start = stdout.find("{")
        if json_start == -1:
            json_start = stdout.find("[")
        if json_start >= 0:
            json_end = stdout.rfind("}")
            if json_end == -1:
                json_end = stdout.rfind("]")
            if json_end > json_start:
                stdout = stdout[json_start : json_end + 1]

        return {
            "success": result.returncode == 0,
            "stdout": stdout.strip(),
            "stderr": result.stderr.strip(),
            "exit_code": result.returncode,
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "stdout": "", "stderr": "命令超时", "exit_code": -1}
    except Exception as e:
        return {"success": False, "stdout": "", "stderr": str(e), "exit_code": -1}


def check_status(project_path: str) -> dict:
    return run_cmd([GITNEXUS, "status"], cwd=project_path)


def analyze(project_path: str) -> dict:
    cmd = [
        GITNEXUS, "analyze",
        project_path,
        "--name", Path(project_path).name,
        "--skip-agents-md",
        "--no-stats",
        "--max-file-size", "1024",
    ]
    return run_cmd(cmd)


def query(project_path: str, keyword: str) -> dict:
    return run_cmd([GITNEXUS, "query", keyword], cwd=project_path)


def context(project_path: str, symbol: str) -> dict:
    return run_cmd([GITNEXUS, "context", symbol], cwd=project_path)


def impact(project_path: str, symbol: str) -> dict:
    return run_cmd([GITNEXUS, "impact", symbol], cwd=project_path)


def detect_changes(project_path: str) -> dict:
    return run_cmd([GITNEXUS, "detect-changes"], cwd=project_path)


if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "help"
    project = sys.argv[2] if len(sys.argv) > 2 else str(Path.cwd())

    if action == "status":
        print(json.dumps(check_status(str(project)), ensure_ascii=False))
    elif action == "analyze":
        print(json.dumps(analyze(str(project)), ensure_ascii=False))
    elif action == "query" and len(sys.argv) > 3:
        print(json.dumps(query(str(project), sys.argv[3]), ensure_ascii=False))
    elif action == "context" and len(sys.argv) > 3:
        print(json.dumps(context(str(project), sys.argv[3]), ensure_ascii=False))
    elif action == "impact" and len(sys.argv) > 3:
        print(json.dumps(impact(str(project), sys.argv[3]), ensure_ascii=False))
    elif action == "detect-changes":
        print(json.dumps(detect_changes(str(project)), ensure_ascii=False))
    else:
        print(json.dumps({
            "usage": "python gitnexus_runner.py <action> [project_path] [args]",
            "actions": ["status", "analyze", "query", "context", "impact", "detect-changes"],
        }, ensure_ascii=False))
