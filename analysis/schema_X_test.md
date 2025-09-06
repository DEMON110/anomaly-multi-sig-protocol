# X_test.csv Schema (Aligned by `id`)

- **id**: integer or string identifier (must match `test_scores (2).csv` id values 1:1)
- Remaining columns: **exact feature set** used by your trained model *in the same order* the model expects.
  - If you trained with a scikit-learn `Pipeline` that includes preprocessing (OneHotEncoder, etc.), you can store the **raw feature columns** here (pre-transform). The pipeline will handle transforms at inference.
  - If you bypassed a pipeline and fed already-transformed arrays, you must export that exact transformed matrix with stable column names (e.g., using `ColumnTransformer.get_feature_names_out()` at train time).

**Authenticity Note:** The `analysis/02_eval_threshold.py` script cross-checks that `model.joblib` can predict on `X_test.csv` **in-place** and that predictions line up with `test_scores (2).csv` by `id`.
