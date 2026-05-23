"""
Reasonix Watchdog — external process monitoring ~/.reasonix/state.json
Starts at session beginning, records violations if execution goes stale.
Handles PID lifecycle: cleans up stale PIDs on start, validates PID on ping.
"""

import os, json, time, sys, signal

STATE_FILE = os.path.expanduser(r'~/.reasonix/state.json')
USAGE_FILE = os.path.expanduser(r'~/.reasonix/usage.jsonl')
USAGE_MAX_BYTES = 1 * 1024 * 1024  # 1MB
PERF_FILE = os.path.expanduser(r'~/.reasonix/skill_performance.json')
CHECK_INTERVAL = 60
STALE_THRESHOLD = 300


def check():
    if not os.path.isfile(STATE_FILE):
        return

    with open(STATE_FILE, 'r', encoding='utf-8') as f:
        state = json.load(f)

    now = time.time()
    last = state.get('_watchdog_ping', 0)
    old_pid = state.get('_watchdog_pid')

    # Stale detection
    if last and (now - last) > STALE_THRESHOLD:
        mins = int((now - last) // 60)
        violation = {
            'type': 'stale',
            'time': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'message': 'Last state update %d min ago - execution may be stalled' % mins
        }
        state.setdefault('violations', []).append(violation)
        sys.stderr.write('[Watchdog] WARN: %s\n' % violation['message'])

    state['_watchdog_ping'] = now
    state['_watchdog_pid'] = os.getpid()
    state['lastUpdated'] = time.strftime('%Y-%m-%dT%H:%M:%S')

    # skill_performance 写入验证 — Phase 完成后 5 分钟内应有新记录
    phase = state.get('phase')
    if phase and phase >= 5:
        perf_written = False
        if os.path.isfile(PERF_FILE):
            try:
                with open(PERF_FILE, 'r', encoding='utf-8') as f:
                    records = json.load(f)
                if records:
                    last_ts = records[-1].get('timestamp', '')
                    if last_ts:
                        perf_written = (now - time.mktime(time.strptime(last_ts, '%Y-%m-%dT%H:%M:%S'))) < 300  # 5 min
            except Exception:
                pass
        if not perf_written:
            violation = {
                'type': 'missing_review',
                'time': time.strftime('%Y-%m-%dT%H:%M:%S'),
                'message': 'Phase 5 completed but skill_performance.json has no recent entry — review skipped'
            }
            state.setdefault('violations', []).append(violation)
            sys.stderr.write('[Watchdog] WARN: %s\n' % violation['message'])

    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

    # usage.jsonl rotation — archive if > 1MB
    if os.path.isfile(USAGE_FILE) and os.path.getsize(USAGE_FILE) > USAGE_MAX_BYTES:
        bak = USAGE_FILE + '.bak'
        if os.path.isfile(bak):
            os.remove(bak)
        os.rename(USAGE_FILE, bak)
        sys.stderr.write('[Watchdog] usage.jsonl archived (>1MB, rotated to usage.jsonl.bak)\n')

    # sessions/ rotation — rotate large files, delete old subagent logs
    SESSION_DIR = os.path.expanduser(r'~/.reasonix/sessions')
    if os.path.isdir(SESSION_DIR):
        now_ts = time.time()
        THREE_DAYS = 3 * 86400
        MAX_FILE_SIZE = 512 * 1024  # 512KB
        for fname in os.listdir(SESSION_DIR):
            fpath = os.path.join(SESSION_DIR, fname)
            if not os.path.isfile(fpath):
                continue
            # Delete subagent logs older than 3 days
            if fname.startswith('subagent-') and fname.endswith('.jsonl'):
                if (now_ts - os.path.getmtime(fpath)) > THREE_DAYS:
                    os.remove(fpath)
                    sys.stderr.write('[Watchdog] removed old session: %s\n' % fname)
                    continue
            # Rotate main session files > 512KB
            if fname.endswith('.jsonl') and not fname.startswith('subagent-'):
                if os.path.getsize(fpath) > MAX_FILE_SIZE:
                    bak = fpath + '.bak'
                    if os.path.isfile(bak):
                        os.remove(bak)
                    os.rename(fpath, bak)
                    sys.stderr.write('[Watchdog] rotated large session: %s (%dKB)\n' % (fname, os.path.getsize(bak)//1024))


if __name__ == '__main__':
    # Graceful shutdown of old watchdog
    def stop_old_watchdog(old_pid):
        """Try graceful stop first, force kill after 3s timeout."""
        if not old_pid:
            return
        try:
            # Step 1: graceful
            if sys.platform == 'win32':
                os.kill(old_pid, signal.SIGTERM)
            else:
                os.kill(old_pid, signal.SIGTERM)
        except (OSError, ProcessLookupError):
            return  # Already dead
        # Step 2: wait up to 3 seconds
        for _ in range(3):
            try:
                os.kill(old_pid, 0)
                time.sleep(1)
            except (OSError, ProcessLookupError):
                return  # Exited gracefully
        # Step 3: force kill
        try:
            os.kill(old_pid, 9)
        except (OSError, ProcessLookupError):
            pass

    # Ensure state.json has valid initial values
    def ensure_state_initialized():
        """Auto-init state.json so model doesn't need to manually write it."""
        now = time.time()
        default = {
            "phase": 0,
            "step": "0.1",
            "skill": "full-autonomous",
            "startedAt": time.strftime('%Y-%m-%dT%H:%M:%S'),
            "completedSteps": [],
            "violations": [],
            "lastUpdated": time.strftime('%Y-%m-%dT%H:%M:%S'),
            "_watchdog_ping": now,
            "_watchdog_pid": os.getpid()
        }
        if not os.path.isfile(STATE_FILE):
            with open(STATE_FILE, 'w', encoding='utf-8') as f:
                json.dump(default, f, indent=2, ensure_ascii=False)
            return
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            state = json.load(f)
        changed = False
        if state.get('phase') is None:
            state['phase'] = 0; changed = True
        if state.get('startedAt') is None:
            state['startedAt'] = time.strftime('%Y-%m-%dT%H:%M:%S'); changed = True
        if state.get('lastUpdated') is None:
            state['lastUpdated'] = time.strftime('%Y-%m-%dT%H:%M:%S'); changed = True
        if state.get('_watchdog_ping') is None:
            state['_watchdog_ping'] = now; changed = True
        if changed:
            with open(STATE_FILE, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2, ensure_ascii=False)

    # Run on startup
    if os.path.isfile(STATE_FILE):
        try:
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                state = json.load(f)
            stop_old_watchdog(state.get('_watchdog_pid'))
        except Exception:
            pass
    ensure_state_initialized()

    sys.stderr.write('[Watchdog] started, PID=%d, interval=%ds\n' % (os.getpid(), CHECK_INTERVAL))
    while True:
        try:
            check()
        except Exception as e:
            sys.stderr.write('[Watchdog] ERROR: %s\n' % e)
        time.sleep(CHECK_INTERVAL)
