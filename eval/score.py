"""Compare agent runs against the human-graded label set."""
import argparse
import json
from pathlib import Path


def load_jsonl(path):
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]


def score_liquidation_distance(gold, runs, tolerance_pp=5):
    """Binary: did the agent flag liquidation risk where the human did?"""
    gold_by_addr = {g["wallet"]: g for g in gold}
    tp = fp = fn = tn = 0
    for r in runs:
        g = gold_by_addr.get(r["wallet"])
        if not g:
            continue
        gold_flag = g["liquidation_concern"]
        agent_flag = "liquidation" in (r.get("flags") or [])
        if gold_flag and agent_flag: tp += 1
        elif not gold_flag and agent_flag: fp += 1
        elif gold_flag and not agent_flag: fn += 1
        else: tn += 1
    return {"tp": tp, "fp": fp, "fn": fn, "tn": tn,
            "precision": tp / max(1, tp + fp),
            "recall": tp / max(1, tp + fn)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", required=True)
    ap.add_argument("--gold", required=True)
    args = ap.parse_args()

    runs = load_jsonl(args.runs)
    gold = load_jsonl(args.gold)

    print("liquidation:", score_liquidation_distance(gold, runs))


if __name__ == "__main__":
    main()
