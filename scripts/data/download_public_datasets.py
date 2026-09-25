#!/usr/bin/env python3
"""Download the exact public files used by the ESF benchmark.

No third-party HTTP dependency is required. Existing files are left untouched
unless --force is supplied.
"""
from __future__ import annotations
import argparse
import hashlib
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FILES = {
    "data/external/synur/synur_schema.json": "https://huggingface.co/datasets/microsoft/SYNUR/resolve/main/data/synur_schema.json",
    "data/external/synur/mediqa_synur_train-00000-of-00001.jsonl": "https://huggingface.co/datasets/microsoft/SYNUR/resolve/main/data/mediqa_synur_train-00000-of-00001.jsonl",
    "data/external/synur/mediqa_synur_dev-00000-of-00001.jsonl": "https://huggingface.co/datasets/microsoft/SYNUR/resolve/main/data/mediqa_synur_dev-00000-of-00001.jsonl",
    "data/external/synur/mediqa_synur_test-00000-of-00001.jsonl": "https://huggingface.co/datasets/microsoft/SYNUR/resolve/main/data/mediqa_synur_test-00000-of-00001.jsonl",
    "data/external/mts_dialog/MTS-Dialog-TrainingSet.csv": "https://raw.githubusercontent.com/abachaa/MTS-Dialog/main/Main-Dataset/MTS-Dialog-TrainingSet.csv",
    "data/external/mts_dialog/MTS-Dialog-ValidationSet.csv": "https://raw.githubusercontent.com/abachaa/MTS-Dialog/main/Main-Dataset/MTS-Dialog-ValidationSet.csv",
    "data/external/mts_dialog/MTS-Dialog-TestSet-1-MEDIQA-Chat-2023.csv": "https://raw.githubusercontent.com/abachaa/MTS-Dialog/main/Main-Dataset/MTS-Dialog-TestSet-1-MEDIQA-Chat-2023.csv",
    "data/external/mts_dialog/MTS-Dialog-TestSet-2-MEDIQA-Sum-2023.csv": "https://raw.githubusercontent.com/abachaa/MTS-Dialog/main/Main-Dataset/MTS-Dialog-TestSet-2-MEDIQA-Sum-2023.csv",
}

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    for rel, url in FILES.items():
        dest = ROOT / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists() and not args.force:
            print(f"skip {rel} sha256={sha256(dest)}")
            continue
        print(f"download {rel}")
        req = urllib.request.Request(url, headers={"User-Agent": "esf-previsit-benchmark/0.2"})
        with urllib.request.urlopen(req, timeout=120) as resp, dest.open("wb") as out:
            out.write(resp.read())
        print(f"  sha256={sha256(dest)}")

if __name__ == "__main__":
    main()
