# Analysis Pipeline (Supervisor Deliverables)

## Files produced
- `analysis_outputs/X_test.csv` — aligned to `test_scores (2).csv` by `id`
- `analysis_outputs/metrics.json` — contains τ* and metrics (F1, precision, recall, AUC), plus score-alignment checks
- `analysis_outputs/*_at_tau_star.csv` — TP/FP/TN/FN splits with ids
- `analysis_outputs/precision_recall.png`, `score_hist.png` — figures for the paper or Q1 supplementary

## How to run
```bash
pip install -r analysis/requirements-ml.txt

# 1) build X_test.csv (edit paths and MODEL_FEATURE_COLUMNS inside)
python analysis/01_make_X_test.py

# 2) compute τ* and verify model vs scores
python analysis/02_eval_threshold.py

# 3) export TP/FP/TN/FN at τ*
python analysis/03_select_cases.py
