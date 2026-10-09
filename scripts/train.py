"""Build the synthetic dataset, train the Qalxan model and save it.

Usage: python scripts/train.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from qalxan.model import QalxanModel  # noqa: E402
from qalxan.synth import build_dataset  # noqa: E402

DATA = ROOT / "data"


def write_jsonl(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def main():
    rows = build_dataset()
    train = [r for r in rows if r["split"] == "train"]
    test = [r for r in rows if r["split"] == "test"]
    write_jsonl(DATA / "train.jsonl", train)
    write_jsonl(DATA / "test.jsonl", test)
    print(f"train={len(train)} test={len(test)}")

    model = QalxanModel().fit([r["text"] for r in train], [r["label"] for r in train], [r["scheme"] for r in train])
    model.save()
    print("model saved")


if __name__ == "__main__":
    main()
