"""
Compute τ* (F1-maximizing threshold) using test_scores (2).csv.
Also verifies model inference on X_test.csv to cross-check authenticity.
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import f1_score, precision_recall_curve, roc_curve, roc_auc_score

from utils_io import read_scores

np.random.seed(0)

MODEL_PATHS = ["model.joblib", "model.pkl"]  # one of these must exist
XTEST_PATH  = "analysis_outputs/X_test.csv"

def load_model():
    for p in MODEL_PATHS:
        if os.path.exists(p):
            return joblib.load(p), p
    raise FileNotFoundError("Place your trained model at model.joblib or model.pkl in repo root.")

def main():
    scores = read_scores("test_scores (2).csv")
    y_true  = scores["y_true"].astype(int).values
    y_score = scores["y_score"].astype(float).values

    # ----- τ* by maximizing F1 over PR thresholds
    prec, rec, thr = precision_recall_curve(y_true, y_score)
    # precision_recall_curve returns thresholds of length n-1
    f1s = (2 * prec[:-1] * rec[:-1] / (prec[:-1] + rec[:-1] + 1e-12))
    idx = int(np.nanargmax(f1s))
    tau_star = float(thr[idx])
    best_f1  = float(f1s[idx])
    best_prec = float(prec[idx])
    best_rec  = float(rec[idx])

    # Extra metrics
    auc = float(roc_auc_score(y_true, y_score))

    # Sanity: verify model predicts the same scores on X_test (if possible)
    model, model_path = load_model()
    X_test = pd.read_csv(XTEST_PATH)

    # Remove id, keep features
    feature_cols = [c for c in X_test.columns if c != "id"]
    # If your model is a Pipeline it should accept the raw columns directly.
    model_scores = model.predict_proba(X_test[feature_cols])[:, 1]
    if len(model_scores) != len(y_score):
        raise ValueError("Pred length mismatch vs test_scores; check X_test alignment.")

    # Check correlation / closeness to provided scores
    corr = float(np.corrcoef(model_scores, y_score)[0,1])
    mse  = float(np.mean((model_scores - y_score)**2))

    # Save metrics
    os.makedirs("analysis_outputs", exist_ok=True)
    with open("analysis_outputs/metrics.json", "w") as f:
        json.dump({
            "tau_star": tau_star,
            "f1_at_tau_star": best_f1,
            "precision_at_tau_star": best_prec,
            "recall_at_tau_star": best_rec,
            "roc_auc": auc,
            "model_path": model_path,
            "score_alignment": {"pearson_r": corr, "mse": mse}
        }, f, indent=2)

    # Plot PR curve and mark τ*
    plt.figure()
    plt.plot(rec, prec, label="PR curve")
    plt.scatter(rec[idx], prec[idx], s=40, label=f"τ*={tau_star:.6f}")
    plt.xlabel("Recall"); plt.ylabel("Precision"); plt.title("Precision-Recall")
    plt.legend()
    plt.tight_layout()
    plt.savefig("analysis_outputs/precision_recall.png", dpi=160)

    # Plot score histogram with τ*
    plt.figure()
    plt.hist(y_score, bins=50)
    plt.axvline(tau_star, linestyle="--")
    plt.xlabel("y_score"); plt.ylabel("count"); plt.title("Score distribution with τ*")
    plt.tight_layout()
    plt.savefig("analysis_outputs/score_hist.png", dpi=160)

    print("Saved: analysis_outputs/metrics.json, precision_recall.png, score_hist.png")
    print(f"τ* = {tau_star:.6f}, F1 = {best_f1:.4f}, AUC = {auc:.4f}")
    print(f"Score alignment vs model: r={corr:.6f}, mse={mse:.6e}")

if __name__ == "__main__":
    main()
