#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
import time
import urllib.request


def ready(base: str) -> bool:
    try:
        with urllib.request.urlopen(base.rstrip('/') + '/v1/models', timeout=5) as r:
            obj = json.loads(r.read().decode('utf-8'))
        return isinstance(obj, dict) and 'data' in obj
    except Exception:
        return False


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--timeout', type=int, default=1800)
    ap.add_argument('endpoints', nargs='*', default=[
        'http://localhost:8001', 'http://localhost:8002', 'http://localhost:8003'
    ])
    args = ap.parse_args()
    deadline = time.time() + args.timeout
    pending = set(args.endpoints)
    while pending and time.time() < deadline:
        for ep in list(pending):
            if ready(ep):
                print(f'ready {ep}', flush=True)
                pending.remove(ep)
        if pending:
            print('waiting: ' + ', '.join(sorted(pending)), flush=True)
            time.sleep(10)
    if pending:
        raise SystemExit('timeout waiting for: ' + ', '.join(sorted(pending)))

if __name__ == '__main__':
    main()
