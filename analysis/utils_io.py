import os
import pandas as pd

def read_scores(path="test_scores (2).csv"):
    df = pd.read_csv(path)
    # Ensure standard column names
    rename_map = {c:c.strip() for c in df.columns}
    df = df.rename(columns=rename_map)
    assert {"id","y_true","y_score"}.issubset(df.columns), \
        f"CSV must contain id,y_true,y_score; got {df.columns.tolist()}"
    # Clean NaNs and stray unnamed cols if any
    drop_cols = [c for c in df.columns if c.lower().startswith("unnamed")]
    if drop_cols: df = df.drop(columns=drop_cols)
    return df

def write_csv(df, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    return path
