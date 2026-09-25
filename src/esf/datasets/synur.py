"""Adapter for microsoft/SYNUR.

SYNUR is an external schema-constrained extraction benchmark. It is not a
Vietnamese MOH-form benchmark and must not be reported as such.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable


def parse_observations(value: Any) -> list[dict[str, Any]]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        parsed = json.loads(value)
        if not isinstance(parsed, list):
            raise ValueError("SYNUR observations must decode to a list")
        return parsed
    raise TypeError(f"Unsupported observations type: {type(value)!r}")


def normalize_row(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": str(row["id"]),
        "transcript": row["transcript"],
        "observations": parse_observations(row.get("observations")),
        "source_dataset": "microsoft/SYNUR",
    }


def iter_jsonl(path: str | Path) -> Iterable[dict[str, Any]]:
    with Path(path).open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                yield normalize_row(json.loads(line))


def load_huggingface(split: str):
    """Load SYNUR through `datasets` when network/cache is available.

    Expected splits visible in the public repository include:
    mediqa_synur_train, mediqa_synur_dev, mediqa_synur_test, original.
    """
    try:
        from datasets import load_dataset
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("Install optional dependency: pip install '.[hf]'") from exc
    ds = load_dataset("microsoft/SYNUR", split=split)
    return [normalize_row(dict(r)) for r in ds]


def observation_type_counts(rows: Iterable[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        for obs in row["observations"]:
            key = obs.get("value_type", "UNKNOWN")
            counts[key] = counts.get(key, 0) + 1
    return counts
