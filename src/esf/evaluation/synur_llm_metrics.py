from __future__ import annotations
from collections import Counter
from typing import Any


def _norm_scalar(v: Any) -> Any:
    if isinstance(v, str):
        return " ".join(v.strip().lower().split())
    if isinstance(v, float) and v.is_integer():
        return int(v)
    return v


def _norm_value(v: Any) -> Any:
    if isinstance(v, list):
        return tuple(sorted(_norm_scalar(x) for x in v))
    return _norm_scalar(v)


def _obs_map(obs: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(x.get("id")): x for x in obs if x.get("id") is not None}


def score_example(pred: list[dict[str, Any]], gold: list[dict[str, Any]]) -> dict[str, Any]:
    pm, gm = _obs_map(pred), _obs_map(gold)
    ps, gs = set(pm), set(gm)
    tp = len(ps & gs)
    precision = tp / len(ps) if ps else (1.0 if not gs else 0.0)
    recall = tp / len(gs) if gs else (1.0 if not ps else 0.0)
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    matched = sorted(ps & gs)
    typed_value_correct = 0
    typed_value_type_correct = 0
    for cid in matched:
        po, go = pm[cid], gm[cid]
        if str(po.get("value_type")) == str(go.get("value_type")):
            typed_value_type_correct += 1
            if _norm_value(po.get("value")) == _norm_value(go.get("value")):
                typed_value_correct += 1
    pred_counter = Counter((cid, str(o.get("value_type")), _norm_value(o.get("value"))) for cid, o in pm.items())
    gold_counter = Counter((cid, str(o.get("value_type")), _norm_value(o.get("value"))) for cid, o in gm.items())
    unsupported = len(ps - gs)
    return {
        "concept_precision": precision,
        "concept_recall": recall,
        "concept_f1": f1,
        "concept_tp": tp,
        "concept_fp": len(ps - gs),
        "concept_fn": len(gs - ps),
        "exact_concept_set": ps == gs,
        "typed_value_type_correct": typed_value_type_correct,
        "typed_value_correct": typed_value_correct,
        "matched_concepts": len(matched),
        "exact_observation_match": pred_counter == gold_counter,
        "unsupported_fill_count": unsupported,
        "predicted_count": len(ps),
        "gold_count": len(gs),
    }


def aggregate(records: list[dict[str, Any]]) -> dict[str, Any]:
    valid = [r for r in records if r.get("parse_ok")]
    scored = [r["score"] for r in valid if "score" in r]
    n = len(records)
    if not n:
        return {"n": 0}
    tp = sum(s["concept_tp"] for s in scored)
    fp = sum(s["concept_fp"] for s in scored)
    fn = sum(s["concept_fn"] for s in scored)
    micro_p = tp / (tp + fp) if tp + fp else 0.0
    micro_r = tp / (tp + fn) if tp + fn else 0.0
    micro_f1 = 2 * micro_p * micro_r / (micro_p + micro_r) if micro_p + micro_r else 0.0
    matched = sum(s["matched_concepts"] for s in scored)
    type_correct = sum(s["typed_value_type_correct"] for s in scored)
    value_correct = sum(s["typed_value_correct"] for s in scored)
    predicted = sum(s["predicted_count"] for s in scored)
    unsupported = sum(s["unsupported_fill_count"] for s in scored)
    latencies = sorted(float(r.get("latency_seconds", 0)) for r in records if r.get("latency_seconds") is not None)
    def pct(q: float) -> float | None:
        if not latencies: return None
        i = min(len(latencies)-1, max(0, round((len(latencies)-1)*q)))
        return latencies[i]
    return {
        "n": n,
        "parse_ok_rate": len(valid) / n,
        "schema_valid_rate": sum(bool(r.get("schema_valid")) for r in records) / n,
        "micro_concept_precision": micro_p,
        "micro_concept_recall": micro_r,
        "micro_concept_f1": micro_f1,
        "macro_concept_f1": sum(s["concept_f1"] for s in scored) / len(scored) if scored else 0.0,
        "exact_concept_set_rate": sum(bool(s["exact_concept_set"]) for s in scored) / len(scored) if scored else 0.0,
        "typed_value_type_accuracy_on_matched": type_correct / matched if matched else 0.0,
        "typed_value_accuracy_on_matched": value_correct / matched if matched else 0.0,
        "exact_observation_match_rate": sum(bool(s["exact_observation_match"]) for s in scored) / len(scored) if scored else 0.0,
        "unsupported_fill_rate": unsupported / predicted if predicted else 0.0,
        "latency_p50_seconds": pct(0.50),
        "latency_p95_seconds": pct(0.95),
        "output_tokens_mean": sum((r.get("usage") or {}).get("completion_tokens", 0) for r in records) / n,
    }
