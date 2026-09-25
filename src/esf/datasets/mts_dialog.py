"""Adapter for MTS-Dialog.

MTS-Dialog is an auxiliary doctor-patient dialogue/history benchmark.
Original labels are section headers and summaries, not ESF atomic-fact gold.
Uses Python stdlib CSV only so the core research repo stays lightweight.
"""
from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable

PREVISIT_SECTIONS = {
    "cc", "genhx", "pastmedicalhx", "pastsurgical", "allergy",
    "medications", "fam/sochx", "gynhx", "other_history", "ros",
}


def normalize_header(value: str) -> str:
    return str(value).strip().lower()


def load_csv(path: str | Path, *, previsit_only: bool = True) -> list[dict[str, str]]:
    with Path(path).open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        required = {"ID", "section_header", "section_text", "dialogue"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"MTS-Dialog missing columns: {sorted(missing)}")
        rows = []
        for row in reader:
            row = dict(row)
            row["section_header_norm"] = normalize_header(row["section_header"])
            if previsit_only and row["section_header_norm"] not in PREVISIT_SECTIONS:
                continue
            rows.append(row)
        return rows


def section_counts(rows: Iterable[dict[str, str]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        key = row.get("section_header_norm") or normalize_header(row["section_header"])
        counts[key] = counts.get(key, 0) + 1
    return dict(sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])))
