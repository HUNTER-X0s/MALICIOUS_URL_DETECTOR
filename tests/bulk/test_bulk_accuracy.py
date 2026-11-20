"""
URLSentinel Bulk Accuracy Test
================================
Tests the full URLSentinel verdict engine against 1000+ labeled URLs.
Measures real-world classifier performance on mixed phishing and benign samples.

Reports:
  - True Positive Rate (TPR / Recall) for phishing
  - False Positive Rate (FPR) — legitimate URLs incorrectly flagged
  - Precision, F1
  - Latency per URL
  - Failure modes (by category)

DO NOT state tests passed unless they were actually executed and passed.
This script enforces that by computing and printing REAL metrics.
"""
from __future__ import annotations

import json
import sys
import time
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SRC_PATH = REPO_ROOT / "services" / "api" / "src"
sys.path.insert(0, str(SRC_PATH))

DATASET_PATH = REPO_ROOT / "data" / "datasets" / "urlsentinel_eval_dataset.json"


def sigmoid(z: float) -> float:
    return 1.0 / (1.0 + (2.718281828 ** (-max(-20.0, min(20.0, z)))))


def run_bulk_test(threshold: float = 0.50):
    print("=" * 70)
    print("URLSentinel Bulk Accuracy Test — REAL EXECUTION")
    print("=" * 70)

    # Load dataset
    if not DATASET_PATH.exists():
        print(f"[ERROR] Dataset not found: {DATASET_PATH}")
        print("Run: python data/datasets/generate_dataset.py")
        sys.exit(1)

    with open(DATASET_PATH, encoding="utf-8") as f:
        data = json.load(f)

    print(f"\n[DATA] {len(data)} URLs loaded from {DATASET_PATH.name}")

    # Import classifier
    try:
        from urlsentinel.core.ml_classifier import MLClassifier
        print("[OK]  MLClassifier imported from urlsentinel.core")
    except ImportError as e:
        print(f"[ERROR] Cannot import MLClassifier: {e}")
        sys.exit(1)

    # Run predictions
    print(f"\n[RUN] Classifying all {len(data)} URLs (threshold={threshold})...")
    t_start = time.perf_counter()

    results = []
    errors = []
    for item in data:
        url = item["url"]
        true_label = item["label"]
        category = item["category"]
        try:
            pred = MLClassifier.predict(url)
            prob = pred["probability"]
            predicted_label = 1 if prob >= threshold else 0
            results.append({
                "url": url,
                "true_label": true_label,
                "predicted_label": predicted_label,
                "probability": prob,
                "category": category,
                "correct": predicted_label == true_label,
            })
        except Exception as e:
            errors.append({"url": url, "error": str(e)})

    t_end = time.perf_counter()
    elapsed = t_end - t_start

    if errors:
        print(f"[WARN] {len(errors)} URLs failed to classify")
        for e in errors[:5]:
            print(f"       {e['url'][:60]} → {e['error']}")

    # Compute metrics
    total = len(results)
    correct = sum(1 for r in results if r["correct"])
    accuracy = correct / total

    # Confusion matrix
    tp = sum(1 for r in results if r["true_label"] == 1 and r["predicted_label"] == 1)
    fp = sum(1 for r in results if r["true_label"] == 0 and r["predicted_label"] == 1)
    tn = sum(1 for r in results if r["true_label"] == 0 and r["predicted_label"] == 0)
    fn = sum(1 for r in results if r["true_label"] == 1 and r["predicted_label"] == 0)

    total_phishing = tp + fn
    total_benign = tn + fp

    tpr = tp / total_phishing if total_phishing > 0 else 0  # recall
    fpr = fp / total_benign if total_benign > 0 else 0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    f1 = 2 * precision * tpr / (precision + tpr) if (precision + tpr) > 0 else 0
    tnr = tn / total_benign if total_benign > 0 else 0  # specificity

    print(f"\n{'='*70}")
    print(f"RESULTS (threshold={threshold})")
    print(f"{'='*70}")
    print(f"  Total URLs tested:  {total}")
    print(f"  Phishing samples:   {total_phishing}")
    print(f"  Benign samples:     {total_benign}")
    print(f"  Errors:             {len(errors)}")
    print(f"\n  Confusion Matrix:")
    print(f"    True Positives  (TP): {tp:4d}  — phishing correctly detected")
    print(f"    False Positives (FP): {fp:4d}  — benign URL wrongly flagged")
    print(f"    True Negatives  (TN): {tn:4d}  — benign URL correctly passed")
    print(f"    False Negatives (FN): {fn:4d}  — phishing URL MISSED")
    print(f"\n  Metrics:")
    print(f"    Accuracy:         {accuracy*100:6.2f}%")
    print(f"    Precision:        {precision*100:6.2f}%  (of flagged, how many real phishing?)")
    print(f"    Recall (TPR):     {tpr*100:6.2f}%  (of phishing, how many caught?)")
    print(f"    False Positive:   {fpr*100:6.2f}%  (of benign, how many wrongly flagged?)")
    print(f"    Specificity:      {tnr*100:6.2f}%  (of benign, how many passed?)")
    print(f"    F1 Score:         {f1:.4f}")
    print(f"\n  Latency:")
    print(f"    Total elapsed:    {elapsed*1000:.1f} ms")
    print(f"    Per-URL avg:      {elapsed/total*1000:.3f} ms")
    print(f"    Throughput:       {total/elapsed:.0f} URLs/sec")

    # Per-category breakdown
    print(f"\n{'='*70}")
    print("PER-CATEGORY PERFORMANCE")
    print(f"{'='*70}")
    cat_stats = defaultdict(lambda: {"total": 0, "correct": 0, "tp": 0, "fp": 0, "tn": 0, "fn": 0})
    for r in results:
        cat = r["category"]
        cat_stats[cat]["total"] += 1
        if r["correct"]:
            cat_stats[cat]["correct"] += 1
        if r["true_label"] == 1 and r["predicted_label"] == 1:
            cat_stats[cat]["tp"] += 1
        elif r["true_label"] == 0 and r["predicted_label"] == 1:
            cat_stats[cat]["fp"] += 1
        elif r["true_label"] == 0 and r["predicted_label"] == 0:
            cat_stats[cat]["tn"] += 1
        else:
            cat_stats[cat]["fn"] += 1

    print(f"  {'Category':<40} {'Total':>6} {'Correct':>8} {'Acc%':>6}")
    print(f"  {'-'*62}")
    for cat, stats in sorted(cat_stats.items()):
        acc = stats["correct"] / stats["total"] * 100 if stats["total"] > 0 else 0
        flag = "⚠️" if acc < 70 else "✅"
        print(f"  {cat:<40} {stats['total']:>6} {stats['correct']:>8} {acc:>5.1f}% {flag}")

    # Worst misses (false negatives — phishing missed)
    print(f"\n{'='*70}")
    print("FALSE NEGATIVES — Phishing URLs Missed (sample)")
    print(f"{'='*70}")
    fn_examples = [r for r in results if r["true_label"] == 1 and r["predicted_label"] == 0]
    fn_examples.sort(key=lambda x: x["probability"])
    for r in fn_examples[:15]:
        print(f"  prob={r['probability']:.3f} cat={r['category']:30s} {r['url'][:70]}")

    # Worst false positives (benign wrongly flagged)
    print(f"\n{'='*70}")
    print("FALSE POSITIVES — Benign URLs Wrongly Flagged (sample)")
    print(f"{'='*70}")
    fp_examples = [r for r in results if r["true_label"] == 0 and r["predicted_label"] == 1]
    fp_examples.sort(key=lambda x: -x["probability"])
    for r in fp_examples[:15]:
        print(f"  prob={r['probability']:.3f} cat={r['category']:30s} {r['url'][:70]}")

    # Overall verdict
    print(f"\n{'='*70}")
    print("VERDICT")
    print(f"{'='*70}")
    if f1 >= 0.90:
        verdict = "EXCELLENT — Production-grade detection"
    elif f1 >= 0.80:
        verdict = "GOOD — Needs improvement in edge cases"
    elif f1 >= 0.70:
        verdict = "ACCEPTABLE — Significant gaps, needs ML upgrade"
    else:
        verdict = "POOR — Major detection gaps, requires overhaul"

    print(f"  F1={f1:.4f} Precision={precision*100:.1f}% Recall={tpr*100:.1f}% FPR={fpr*100:.1f}%")
    print(f"  → {verdict}")

    # Save full results
    out = {
        "summary": {
            "total": total, "phishing": total_phishing, "benign": total_benign,
            "tp": tp, "fp": fp, "tn": tn, "fn": fn,
            "accuracy": round(accuracy, 4), "precision": round(precision, 4),
            "recall_tpr": round(tpr, 4), "fpr": round(fpr, 4),
            "f1": round(f1, 4), "threshold": threshold,
            "per_url_ms": round(elapsed / total * 1000, 3),
        },
        "per_category": {k: v for k, v in cat_stats.items()},
        "false_negatives": fn_examples[:50],
        "false_positives": fp_examples[:50],
    }
    out_path = Path(__file__).parent / "bulk_test_results.json"
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"\n[SAVED] Full results → {out_path}")

    return out["summary"]


if __name__ == "__main__":
    summary = run_bulk_test(threshold=0.50)

