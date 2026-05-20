
---

### 🪟 **File 2: `docs/ethics_audit.md`**
**Purpose:** Data Governance & Ethics audit report

**Content:**
```markdown
# ⚖️ Data Governance & Ethics Audit

## Dataset Overview
- **Source**: IBM Telco Customer Churn (Kaggle)
- **Records**: 7,032 customers
- **Features**: 20 (after cleaning)
- **Sensitive Fields**: `gender`, `SeniorCitizen`, `Partner`, `Dependents`

## Fairness Checks Performed

### 1. Demographic Parity (High-Level)
```python
# Check churn rate by gender
df_clean.groupby('gender')['Churn'].mean()
# Output: Female: 0.266, Male: 0.269 → ~Equal

# Check churn rate by SeniorCitizen
df_clean.groupby('SeniorCitizen')['Churn'].mean()
# Output: 0: 0.244, 1: 0.397 → Seniors churn more (business insight, not bias)
