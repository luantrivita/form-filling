import pandas as pd

from esf.datasets.mts_dialog import PREVISIT_SECTIONS, load_csv
from esf.datasets.synur import normalize_row, parse_observations


def test_synur_observations_json_string():
    obs = parse_observations('[{"id":"67","value_type":"SINGLE_SELECT","name":"Dyspnea","value":"Mild"}]')
    assert obs[0]["id"] == "67"
    assert obs[0]["value"] == "Mild"


def test_synur_normalize_row():
    row = normalize_row({"id": 1, "transcript": "x", "observations": "[]"})
    assert row["id"] == "1"
    assert row["source_dataset"] == "microsoft/SYNUR"


def test_mts_previsit_filter(tmp_path):
    p = tmp_path / "mts.csv"
    pd.DataFrame([
        {"ID": 1, "section_header": "GENHX", "section_text": "a", "dialogue": "d"},
        {"ID": 2, "section_header": "PLAN", "section_text": "b", "dialogue": "e"},
        {"ID": 3, "section_header": "ALLERGY", "section_text": "c", "dialogue": "f"},
    ]).to_csv(p, index=False)
    df = load_csv(p, previsit_only=True)
    assert [int(r["ID"]) for r in df] == [1, 3]
    assert {r["section_header_norm"] for r in df} <= PREVISIT_SECTIONS
