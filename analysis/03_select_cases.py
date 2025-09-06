"""
Using τ* from metrics.json and test_scores (2).csv, label predictions and export TP/FP ids.
"""
import json
import pandas as pd
from utils_io import read_scores, write_csv

def main():
    scores = read_scores("test_scores (2).csv")
    with open("analysis_outputs/metrics.json","r") as f:
        m = json.load(f)
    tau_star = float(m["tau_star"])

    scores["y_pred"] = (scores["y_score"] >= tau_star).astype(int)

    # Confusion splits
    TP = scores[(scores["y_true"]==1) & (scores["y_pred"]==1)][["id","y_true","y_score"]].copy()
    FP = scores[(scores["y_true"]==0) & (scores["y_pred"]==1)][["id","y_true","y_score"]].copy()
    TN = scores[(scores["y_true"]==0) & (scores["y_pred"]==0)][["id","y_true","y_score"]].copy()
    FN = scores[(scores["y_true"]==1) & (scores["y_pred"]==0)][["id","y_true","y_score"]].copy()

    write_csv(TP, "analysis_outputs/TP_at_tau_star.csv")
    write_csv(FP, "analysis_outputs/FP_at_tau_star.csv")
    write_csv(TN, "analysis_outputs/TN_at_tau_star.csv")
    write_csv(FN, "analysis_outputs/FN_at_tau_star.csv")
    print("Wrote TP/FP/TN/FN CSVs under analysis_outputs/")

if __name__ == "__main__":
    main()
