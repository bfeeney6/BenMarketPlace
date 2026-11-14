#!/usr/bin/env python3
"""Quickly find which Gemini models can watch video right now, best first.

Sends every video-capable model your key can see a tiny request (a 19-second public YouTube video, one-word answer), all at once, so
the whole check takes about as long as the slowest single model (<= --timeout).
Each test costs roughly a thousand or so tokens of free-tier usage.

Usage:
  python check_models.py            # report only
  python check_models.py --apply    # also save the working models, best first,
                                    # as WATCH_GEMINI_MODEL in ~/.config/watch/.env
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import CONFIG_FILE, load_gemini_key  # noqa: E402
import gemini  # noqa: E402

TEST_VIDEO = 'https://www.youtube.com/watch?v=jNQXAC9IVRw'  # "Me at the zoo", 19s, public
SKIP = re.compile(r'tts|image|embedding|lyria|banana|research|customtools|robotics|computer-use|transcribe|audio|live|latest|aqa|gemma', re.I)
TIER = {'pro': 0, 'flash': 1, 'flash-lite': 2}


def rank(name: str):
    """Sort key, best first: newest version, then pro > flash > flash-lite, then stable > preview."""
    m = re.match(r'gemini-(?:omni-)?(\d+(?:\.\d+)?)-(pro|flash-lite|flash)', name)
    if not m:
        return (1, 0, 9, 1, name)
    return (0, -float(m.group(1)), TIER[m.group(2)], 'preview' in name, name)


def list_models(key: str) -> list[str]:
    _, _, body = gemini._call('GET', f'{gemini.API}/v1beta/models?pageSize=200', key, timeout=30)
    names = [m['name'].split('/')[-1] for m in json.loads(body).get('models', [])
             if 'generateContent' in m.get('supportedGenerationMethods', [])]
    return sorted((n for n in names if n.startswith('gemini') and not SKIP.search(n)), key=rank)


def test(model: str, key: str, timeout: float):
    start = time.time()
    try:
        r = gemini.ask({'uri': TEST_VIDEO}, 'In one word, what animal is shown?', model=model, key=key,
                       clip=None, timeout=timeout)  # full-video (agentic) mode, as real runs use
        return model, True, time.time() - start, f"answered {r['text'][:30]!r}"
    except SystemExit as exc:
        msg = str(exc).split('. Detail:')
        reason = msg[0].replace('Gemini ', '')
        detail = msg[1] if len(msg) > 1 else ''
        code = re.search(r'HTTP (\d+)', detail)
        return model, False, time.time() - start, f"{reason.split(':')[0]}{' ' + code.group(1) if code else ''}"


def apply(working: list[str]) -> None:
    lines = CONFIG_FILE.read_text().splitlines() if CONFIG_FILE.exists() else []
    lines = [ln for ln in lines if not ln.startswith('WATCH_GEMINI_MODEL=')]
    lines.append('WATCH_GEMINI_MODEL=' + ','.join(working))
    CONFIG_FILE.write_text('\n'.join(lines) + '\n')


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--timeout', type=float, default=30, help='seconds to wait per model (default 30)')
    ap.add_argument('--apply', action='store_true', help='save working models, best first, to the watch config')
    ap.add_argument('--top', type=int, default=3, help='with --apply, how many working models to keep (default 3)')
    args = ap.parse_args()

    key = load_gemini_key()
    if not key:
        print('No GEMINI_API_KEY found.', file=sys.stderr)
        return 2
    models = list_models(key)
    print(f'Testing {len(models)} models in parallel (up to {args.timeout:.0f}s)...\n', file=sys.stderr)
    with ThreadPoolExecutor(max_workers=len(models) or 1) as pool:
        results = list(pool.map(lambda m: test(m, key, args.timeout), models))  # map keeps best-first order

    for model, ok, secs, note in results:
        print(f"{'OK  ' if ok else 'FAIL'}  {model:<34} {secs:5.1f}s  {note}")
    working = [m for m, ok, _, _ in results if ok]
    print(f"\nBest working model: {working[0] if working else 'none right now'}")
    if args.apply and working:
        apply(working[:args.top])
        print(f"Saved WATCH_GEMINI_MODEL={','.join(working[:args.top])}")
    return 0 if working else 1


if __name__ == '__main__':
    raise SystemExit(main())
