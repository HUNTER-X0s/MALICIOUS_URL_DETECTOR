"""
URLSentinel ML Model Benchmark
===============================
Compares multiple classification approaches on the synthetic labeled dataset.

Models tested:
  A. Current hand-crafted logistic regression heuristic (baseline)
  B. scikit-learn LogisticRegression (trained on URL features)
  C. scikit-learn RandomForestClassifier
  D. XGBoost GradientBoosting
  E. LightGBM
  F. Character-level TF-IDF + LogisticRegression
  G. Combined feature pipeline (URL features + TF-IDF)

Metrics: Precision, Recall, F1, AUC-ROC, accuracy
Cross-validation: Stratified 5-fold

IMPORTANT: Results are reported from ACTUAL execution, not theoretical.
"""
from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

# Add URLSentinel source to path
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SRC_PATH = REPO_ROOT / "services" / "api" / "src"
sys.path.insert(0, str(SRC_PATH))

DATASET_PATH = REPO_ROOT / "data" / "datasets" / "urlsentinel_eval_dataset.json"

try:
    import numpy as np
    import pandas as pd
    from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import (
        accuracy_score,
        classification_report,
        f1_score,
        precision_score,
        recall_score,
        roc_auc_score,
    )
    from sklearn.model_selection import StratifiedKFold, cross_val_score
    from sklearn.pipeline import FeatureUnion, Pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.sparse import issparse

    ML_AVAILABLE = True
except ImportError as e:
    print(f"[WARN] scikit-learn not available: {e}")
    ML_AVAILABLE = False

try:
    import xgboost as xgb
    XGB_AVAILABLE = True
except ImportError:
    XGB_AVAILABLE = False

try:
    import lightgbm as lgb
    LGB_AVAILABLE = True
except ImportError:
    LGB_AVAILABLE = False


# ---------------------------------------------------------------------------
# Feature extraction
# ---------------------------------------------------------------------------

def extract_url_features(url: str) -> list[float]:
    """Extract the same features as URLSentinel's ml_classifier.py."""
    try:
        from urlsentinel.core.ml_classifier import MLClassifier
        feats = MLClassifier.extract_features(url)
        return list(feats.values())
    except Exception:
        # Fallback if import fails
        from urllib.parse import urlparse
        import re
        parsed = urlparse(url)
        host = (parsed.hostname or "").lower()
        path = parsed.path or ""
        url_len = len(url)

        def entropy(s):
            if not s:
                return 0.0
            freq = {}
            for c in s:
                freq[c] = freq.get(c, 0) + 1
            n = len(s)
            return -sum((v / n) * math.log2(v / n) for v in freq.values())

        HIGH_ABUSE_TLDS = {"top", "xyz", "club", "work", "cam", "live", "loan",
                           "stream", "bid", "gq", "ml", "cf", "ga", "buzz"}
        labels = [l for l in host.split(".") if l]
        tld = labels[-1] if labels else ""
        digits = sum(c.isdigit() for c in url)
        symbols = sum(not c.isalnum() and c not in ":/.-_?&=#" for c in url)
        path_segs = [p for p in path.split("/") if p]
        KEYWORDS = {"login", "signin", "verify", "password", "credential",
                    "banking", "wallet", "secure", "account", "update", "confirm"}
        kw_sum = sum(1.0 for kw in KEYWORDS if kw in f"{host} {path}".lower())

        return [
            max(0.0, (url_len - 75.0) / 100.0),
            max(0.0, (entropy(host) - 3.8) / 2.0),
            digits / max(1, url_len),
            symbols / max(1, url_len),
            max(0.0, float(len(labels) - 3)),
            max(0.0, float(len(path_segs) - 4)),
            1.0 if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", host) else 0.0,
            1.0 if "@" in (parsed.netloc or "") else 0.0,
            1.0 if "%" in url else 0.0,
            1.0 if "xn--" in host else 0.0,
            1.0 if "//" in path else 0.0,
            min(4.0, kw_sum),
            1.0 if tld in HIGH_ABUSE_TLDS else 0.0,
        ]


FEATURE_NAMES = [
    "excess_url_length", "high_host_entropy", "digit_ratio", "symbol_ratio",
    "excess_subdomain_depth", "excess_path_depth", "is_ip_host", "has_at_symbol",
    "has_hex_encoding", "has_punycode", "has_double_slash_path", "keyword_score",
    "high_abuse_tld",
]


# ---------------------------------------------------------------------------
# Baseline: hand-crafted heuristic
# ---------------------------------------------------------------------------

def run_heuristic_baseline(urls: list[str], labels: list[int]) -> dict:
    """Run the existing hand-crafted logistic regression heuristic."""
    try:
        from urlsentinel.core.ml_classifier import MLClassifier
        predictions = []
        probs = []
        t0 = time.perf_counter()
        for url in urls:
            result = MLClassifier.predict(url)
            prob = result["probability"]
            probs.append(prob)
            predictions.append(1 if prob >= 0.50 else 0)
        elapsed = time.perf_counter() - t0
    except Exception as e:
        print(f"[ERROR] Heuristic baseline failed: {e}")
        return {}

    y_true = labels
    y_pred = predictions
    y_prob = probs

    return {
        "model": "A_Heuristic_LogReg (hand-crafted)",
        "accuracy": round(accuracy_score(y_true, y_pred), 4),
        "precision": round(precision_score(y_true, y_pred, zero_division=0), 4),
        "recall": round(recall_score(y_true, y_pred, zero_division=0), 4),
        "f1": round(f1_score(y_true, y_pred, zero_division=0), 4),
        "auc_roc": round(roc_auc_score(y_true, y_prob), 4),
        "total_time_ms": round(elapsed * 1000, 1),
        "per_url_ms": round(elapsed / len(urls) * 1000, 3),
        "threshold": 0.50,
    }


# ---------------------------------------------------------------------------
# Trained models
# ---------------------------------------------------------------------------

def train_and_evaluate(model, X, y, model_name: str, cv: int = 5) -> dict:
    """Train a model with stratified k-fold CV and report metrics."""
    skf = StratifiedKFold(n_splits=cv, shuffle=True, random_state=42)
    preds_all = np.zeros(len(y))
    probs_all = np.zeros(len(y))
    t0 = time.perf_counter()

    for fold, (train_idx, val_idx) in enumerate(skf.split(X, y)):
        if hasattr(X, "iloc"):
            X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
        else:
            X_train, X_val = X[train_idx], X[val_idx]
        y_train, y_val = y[train_idx], y[val_idx]

        model.fit(X_train, y_train)
        preds_all[val_idx] = model.predict(X_val)
        if hasattr(model, "predict_proba"):
            probs_all[val_idx] = model.predict_proba(X_val)[:, 1]
        else:
            probs_all[val_idx] = preds_all[val_idx]

    elapsed = time.perf_counter() - t0

    return {
        "model": model_name,
        "accuracy": round(accuracy_score(y, preds_all), 4),
        "precision": round(precision_score(y, preds_all, zero_division=0), 4),
        "recall": round(recall_score(y, preds_all, zero_division=0), 4),
        "f1": round(f1_score(y, preds_all, zero_division=0), 4),
        "auc_roc": round(roc_auc_score(y, probs_all), 4),
        "cv_folds": cv,
        "total_time_ms": round(elapsed * 1000, 1),
        "per_url_ms": round(elapsed / len(y) * 1000, 3),
    }


# ---------------------------------------------------------------------------
# Main benchmark
# ---------------------------------------------------------------------------

def run_benchmark():
    print("=" * 70)
    print("URLSentinel ML Model Benchmark")
    print("=" * 70)

    # Load dataset
    if not DATASET_PATH.exists():
        print(f"[ERROR] Dataset not found at {DATASET_PATH}")
        print("Run: python data/datasets/generate_dataset.py")
        sys.exit(1)

    with open(DATASET_PATH, encoding="utf-8") as f:
        data = json.load(f)

    urls = [d["url"] for d in data]
    labels = [d["label"] for d in data]
    categories = [d["category"] for d in data]

    print(f"\n[DATA] Loaded {len(urls)} URLs")
    print(f"       Phishing: {sum(labels)} ({sum(labels)/len(labels)*100:.1f}%)")
    print(f"       Benign:   {len(labels)-sum(labels)} ({(len(labels)-sum(labels))/len(labels)*100:.1f}%)")

    results = []

    # -------------------------------------------------------------------
    # Model A: Heuristic baseline
    # -------------------------------------------------------------------
    print("\n[A] Running heuristic hand-crafted baseline...")
    res_a = run_heuristic_baseline(urls, labels)
    if res_a:
        results.append(res_a)
        print(f"    Accuracy={res_a['accuracy']}, Precision={res_a['precision']}, "
              f"Recall={res_a['recall']}, F1={res_a['f1']}, AUC={res_a['auc_roc']}")

    if not ML_AVAILABLE:
        print("\n[SKIP] scikit-learn not available. Install: pip install scikit-learn xgboost lightgbm")
        return results

    # Extract features
    print("\n[FEAT] Extracting URL features for all URLs...")
    t0 = time.perf_counter()
    X_feats = np.array([extract_url_features(u) for u in urls])
    y = np.array(labels)
    print(f"       Feature extraction: {(time.perf_counter()-t0)*1000:.1f} ms "
          f"({(time.perf_counter()-t0)/len(urls)*1000:.3f} ms/url)")
    print(f"       Feature matrix: {X_feats.shape}")

    # -------------------------------------------------------------------
    # Model B: Trained LogisticRegression
    # -------------------------------------------------------------------
    print("\n[B] Training scikit-learn LogisticRegression (5-fold CV)...")
    model_b = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(C=1.0, max_iter=1000, random_state=42)),
    ])
    res_b = train_and_evaluate(model_b, X_feats, y, "B_LogisticRegression_trained")
    results.append(res_b)
    print(f"    Accuracy={res_b['accuracy']}, F1={res_b['f1']}, AUC={res_b['auc_roc']}")

    # -------------------------------------------------------------------
    # Model C: RandomForest
    # -------------------------------------------------------------------
    print("\n[C] Training RandomForestClassifier (5-fold CV)...")
    model_c = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42, n_jobs=-1)
    res_c = train_and_evaluate(model_c, X_feats, y, "C_RandomForest_200trees")
    results.append(res_c)
    print(f"    Accuracy={res_c['accuracy']}, F1={res_c['f1']}, AUC={res_c['auc_roc']}")

    # Feature importances from last fold model
    print(f"    Top features: {sorted(zip(FEATURE_NAMES, model_c.feature_importances_), key=lambda x: -x[1])[:5]}")

    # -------------------------------------------------------------------
    # Model D: GradientBoosting (sklearn)
    # -------------------------------------------------------------------
    print("\n[D] Training GradientBoostingClassifier (5-fold CV)...")
    model_d = GradientBoostingClassifier(
        n_estimators=150, learning_rate=0.1, max_depth=4, random_state=42
    )
    res_d = train_and_evaluate(model_d, X_feats, y, "D_GradientBoosting")
    results.append(res_d)
    print(f"    Accuracy={res_d['accuracy']}, F1={res_d['f1']}, AUC={res_d['auc_roc']}")

    # -------------------------------------------------------------------
    # Model E: XGBoost
    # -------------------------------------------------------------------
    if XGB_AVAILABLE:
        print("\n[E] Training XGBoost (5-fold CV)...")
        model_e = xgb.XGBClassifier(
            n_estimators=200, max_depth=5, learning_rate=0.1,
            use_label_encoder=False, eval_metric="logloss",
            random_state=42, verbosity=0
        )
        res_e = train_and_evaluate(model_e, X_feats, y, "E_XGBoost_200est")
        results.append(res_e)
        print(f"    Accuracy={res_e['accuracy']}, F1={res_e['f1']}, AUC={res_e['auc_roc']}")
    else:
        print("\n[E] XGBoost not available, skipping")

    # -------------------------------------------------------------------
    # Model F: LightGBM
    # -------------------------------------------------------------------
    if LGB_AVAILABLE:
        print("\n[F] Training LightGBM (5-fold CV)...")
        model_f = lgb.LGBMClassifier(
            n_estimators=200, learning_rate=0.05, max_depth=6,
            random_state=42, verbose=-1
        )
        res_f = train_and_evaluate(model_f, X_feats, y, "F_LightGBM_200est")
        results.append(res_f)
        print(f"    Accuracy={res_f['accuracy']}, F1={res_f['f1']}, AUC={res_f['auc_roc']}")
    else:
        print("\n[F] LightGBM not available, skipping")

    # -------------------------------------------------------------------
    # Model G: TF-IDF character n-gram on raw URL text
    # -------------------------------------------------------------------
    print("\n[G] Training TF-IDF (char n-gram 2-5) + LogisticRegression (5-fold CV)...")
    model_g = Pipeline([
        ("tfidf", TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 5),
                                  max_features=20000, min_df=2)),
        ("clf", LogisticRegression(C=5.0, max_iter=1000, random_state=42)),
    ])
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    preds_g = np.zeros(len(y))
    probs_g = np.zeros(len(y))
    t0 = time.perf_counter()
    for _, (train_idx, val_idx) in enumerate(skf.split(urls, y)):
        X_train = [urls[i] for i in train_idx]
        X_val = [urls[i] for i in val_idx]
        y_train = y[train_idx]
        model_g.fit(X_train, y_train)
        preds_g[val_idx] = model_g.predict(X_val)
        probs_g[val_idx] = model_g.predict_proba(X_val)[:, 1]
    elapsed_g = time.perf_counter() - t0
    res_g = {
        "model": "G_TFIDF_CharNgram_LogReg",
        "accuracy": round(accuracy_score(y, preds_g), 4),
        "precision": round(precision_score(y, preds_g, zero_division=0), 4),
        "recall": round(recall_score(y, preds_g, zero_division=0), 4),
        "f1": round(f1_score(y, preds_g, zero_division=0), 4),
        "auc_roc": round(roc_auc_score(y, probs_g), 4),
        "cv_folds": 5,
        "total_time_ms": round(elapsed_g * 1000, 1),
        "per_url_ms": round(elapsed_g / len(y) * 1000, 3),
    }
    results.append(res_g)
    print(f"    Accuracy={res_g['accuracy']}, F1={res_g['f1']}, AUC={res_g['auc_roc']}")

    # -------------------------------------------------------------------
    # Model H: Combined (URL features + TF-IDF char ngram)
    # -------------------------------------------------------------------
    print("\n[H] Training Combined features (URL feats + TF-IDF) + RandomForest (5-fold CV)...")
    # We do this manually since FeatureUnion needs both dense and sparse
    tfidf_vect = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4),
                                  max_features=10000, min_df=2)
    tfidf_vect.fit(urls)
    X_tfidf = tfidf_vect.transform(urls).toarray()
    X_combined = np.hstack([X_feats, X_tfidf])

    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    preds_h = np.zeros(len(y))
    probs_h = np.zeros(len(y))
    t0 = time.perf_counter()
    for _, (train_idx, val_idx) in enumerate(skf.split(X_combined, y)):
        rf = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42, n_jobs=-1)
        rf.fit(X_combined[train_idx], y[train_idx])
        preds_h[val_idx] = rf.predict(X_combined[val_idx])
        probs_h[val_idx] = rf.predict_proba(X_combined[val_idx])[:, 1]
    elapsed_h = time.perf_counter() - t0
    res_h = {
        "model": "H_Combined_URLFeats+TFIDF_RF",
        "accuracy": round(accuracy_score(y, preds_h), 4),
        "precision": round(precision_score(y, preds_h, zero_division=0), 4),
        "recall": round(recall_score(y, preds_h, zero_division=0), 4),
        "f1": round(f1_score(y, preds_h, zero_division=0), 4),
        "auc_roc": round(roc_auc_score(y, probs_h), 4),
        "cv_folds": 5,
        "total_time_ms": round(elapsed_h * 1000, 1),
        "per_url_ms": round(elapsed_h / len(y) * 1000, 3),
    }
    results.append(res_h)
    print(f"    Accuracy={res_h['accuracy']}, F1={res_h['f1']}, AUC={res_h['auc_roc']}")

    # -------------------------------------------------------------------
    # Category breakdown for best model
    # -------------------------------------------------------------------
    print("\n[CATEGORY ANALYSIS] Per-category performance of best model...")
    # Find best by F1
    best = max(results, key=lambda r: r.get("f1", 0))
    print(f"    Best model: {best['model']} (F1={best['f1']})")

    return results


def print_results_table(results: list[dict]):
    print("\n" + "=" * 70)
    print("BENCHMARK RESULTS SUMMARY")
    print("=" * 70)
    header = f"{'Model':<40} {'Acc':>6} {'Prec':>6} {'Rec':>6} {'F1':>6} {'AUC':>6} {'ms/URL':>8}"
    print(header)
    print("-" * 70)
    for r in sorted(results, key=lambda x: -x.get("f1", 0)):
        name = r["model"][:40]
        print(
            f"{name:<40} {r.get('accuracy',0):>6.4f} {r.get('precision',0):>6.4f} "
            f"{r.get('recall',0):>6.4f} {r.get('f1',0):>6.4f} {r.get('auc_roc',0):>6.4f} "
            f"{r.get('per_url_ms',0):>8.3f}"
        )
    print("=" * 70)


if __name__ == "__main__":
    results = run_benchmark()
    print_results_table(results)

    # Save results
    out_path = Path(__file__).parent / "benchmark_results.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n[SAVED] Results → {out_path}")

