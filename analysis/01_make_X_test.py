"""
Build X_test.csv aligned to test_scores (2).csv by `id`.

This script demonstrates two strategies:
A) If you have the original raw test frame (features_raw.csv), we left-join on `id` and export only the model features.
B) If you only have a saved pipeline that can accept the raw frame, ensure the raw columns match training schema.

Edit marked TODOs to point to your real raw test features source or generator.
"""

import pandas as pd
from utils_io import read_scores, write_csv

# === TODO: set one of these paths/sources ===
RAW_FEATURES_CSV = "features_raw.csv"   # (A) preferred: your raw test features with an `id` column
# OR: if you must reconstruct features from another file, point to it here.

# === TODO: define the columns your model expects (raw feature names if you used a Pipeline) ===
MODEL_FEATURE_COLUMNS = [
    # e.g. "amount","hour","sender_country","receiver_country","device_type","txn_type", ...
]

def main():
    scores = read_scores("test_scores (2).csv")[["id"]]  # alignment backbone

    # --- Load raw features
    raw = pd.read_csv(RAW_FEATURES_CSV)
    assert "id" in raw.columns, "RAW_FEATURES_CSV must include an `id` column"

    # --- Subset to required features (plus id)
    missing = [c for c in MODEL_FEATURE_COLUMNS if c not in raw.columns]
    if missing:
        raise ValueError(f"Missing required feature columns in RAW_FEATURES_CSV: {missing}")

    X = raw[["id"] + MODEL_FEATURE_COLUMNS].copy()

    # --- Align the row order to test_scores
    X = scores.merge(X, on="id", how="left")
    if X.isnull().any().any():
        nnull = int(X.isnull().any(axis=1).sum())
        raise ValueError(f"{nnull} rows in X_test have missing feature values after align. Fill or fix source.")

    write_csv(X, "analysis_outputs/X_test.csv")
    print("Wrote analysis_outputs/X_test.csv with shape:", X.shape)

if __name__ == "__main__":
    main()
