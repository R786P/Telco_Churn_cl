# 🏗️ Data Architecture Design

## Pipeline Overview

## Components

### 1. Data Ingestion
- **Source**: Kaggle Dataset (`WA_Fn-UseC-Telco-Customer-Churn.csv`)
- **Auto-detect path**: `os.walk('/kaggle/input')` for portability
- **Validation**: Shape check `(7043, 21)` → `(7032, 20)` after cleaning

### 2. Data Cleaning (`clean_churn_data()`)
| Step | Action | Reason |
|------|--------|--------|
| `TotalCharges` | `pd.to_numeric(errors="coerce")` | Handle string values like " " |
| Missing Values | `dropna(subset=["TotalCharges", "MonthlyCharges"])` | Remove incomplete records |
| Target Encoding | `"Yes"/"No"` → `1/0` | Model-compatible format |
| Drop `customerID` | `drop(columns=["customerID"])` | Non-predictive identifier |

### 3. Preprocessing (Version-Compatible)
- **Manual approach** (no `ColumnTransformer`) to avoid sklearn version conflicts
- Numeric: `StandardScaler`
- Categorical: `OneHotEncoder(handle_unknown="ignore")`
- Final: `np.hstack([num, cat])` for feature matrix

### 4. Model Training
- **Algorithm**: `RandomForestClassifier`
- **Tuning**: Optuna (5 trials, ROC-AUC objective)
- **Best Params**: `{'n_estimators': 166, 'max_depth': 7, 'min_samples_split': 6}`
- **Class Weight**: `"balanced"` for imbalanced churn data

### 5. Serialization
- **Format**: `joblib.dump(..., protocol=2, compress=3)`
- **Why protocol=2?**: Maximum compatibility across Python 3.8–3.12
- **Artifact Contents**:
  ```python
  {
      "model": trained_rf,
      "scaler": fitted_scaler,
      "ohe": fitted_ohe,
      "num_cols": [...],
      "cat_cols": [...],
      "feature_names": [...]
  }
