# Reproducibility Guide

## Code Pin
- Repo: https://github.com/DEMON110/anomaly-multi-sig-protocol
- Commit: <PIN AFTER YOU COMMIT THESE FILES>
- Release tag (recommended): v0.1.0

## Environments
- Hardhat: see `package.json`, `hardhat.config.js`
- ML: `analysis/requirements-ml.txt`

## Steps
1) **ML side**
   ```bash
   pip install -r analysis/requirements-ml.txt
   python analysis/01_make_X_test.py
   python analysis/02_eval_threshold.py
   python analysis/03_select_cases.py

import random
import numpy as np

# Define seed values
training_seed = 42
evaluation_seed = 123
bootstrap_seed = 456

# Set seeds for reproducibility
random.seed(training_seed)
np.random.seed(training_seed)
