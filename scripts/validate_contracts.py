from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"


def load(name: str):
    return json.loads((SCHEMAS / name).read_text(encoding="utf-8"))


def make_validator():
    schemas = {p.name: json.loads(p.read_text(encoding="utf-8")) for p in SCHEMAS.glob("*.json")}
    registry = Registry()
    for name, contents in schemas.items():
        registry = registry.with_resource(name, Resource.from_contents(contents))
    return Draft202012Validator(schemas["generation_case.schema.json"], registry=registry)


def validate_case(path: Path) -> list[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    errors = sorted(make_validator().iter_errors(data), key=lambda e: list(e.path))
    return [f"{list(e.path)}: {e.message}" for e in errors]


def main():
    targets = [ROOT / "data_generation/examples/example_case_001.json"]
    targets.extend(sorted((ROOT / "data/reviewed/regression_cases").glob("*.json")))
    failed = False
    for p in targets:
        errors = validate_case(p)
        if errors:
            failed = True
            print(f"FAIL {p}")
            for e in errors:
                print("  -", e)
        else:
            print(f"PASS {p}")
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
