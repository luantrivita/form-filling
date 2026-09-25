import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_source_registry_unique_ids():
    rows = json.loads((ROOT / "registry/sources/source_registry.json").read_text())
    ids = [r["source_id"] for r in rows]
    assert len(ids) == len(set(ids))
    assert "MOH_15_BV_01" in ids
    assert "TTYQG_CV292_2026" in ids
