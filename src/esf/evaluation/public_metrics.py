"""Minimal metrics for public ESF-adjacent benchmarks."""
from __future__ import annotations
from collections import Counter
from typing import Any, Iterable


def observation_key(obs: dict[str, Any]) -> tuple[str, str]:
    return str(obs.get("id")), str(obs.get("value_type"))


def concept_set(observations: Iterable[dict[str, Any]]) -> set[str]:
    return {str(o["id"]) for o in observations}


def precision_recall_f1(pred: set[str], gold: set[str]) -> dict[str, float]:
    tp = len(pred & gold)
    p = tp / len(pred) if pred else (1.0 if not gold else 0.0)
    r = tp / len(gold) if gold else (1.0 if not pred else 0.0)
    f1 = 2*p*r/(p+r) if (p+r) else 0.0
    return {"precision": p, "recall": r, "f1": f1}


def exact_observation_match(pred: list[dict[str, Any]], gold: list[dict[str, Any]]) -> bool:
    def canon(o: dict[str, Any]):
        value=o.get("value")
        if isinstance(value,list): value=tuple(value)
        return (str(o.get("id")), str(o.get("value_type")), value)
    return Counter(map(canon,pred)) == Counter(map(canon,gold))


def macro_concept_f1(predictions: list[list[dict[str, Any]]], golds: list[list[dict[str, Any]]]) -> float:
    if len(predictions) != len(golds):
        raise ValueError("prediction/gold length mismatch")
    if not golds: return 0.0
    return sum(precision_recall_f1(concept_set(p),concept_set(g))["f1"] for p,g in zip(predictions,golds))/len(golds)
