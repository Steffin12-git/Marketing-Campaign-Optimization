# 📘 **Portuguese Bank Marketing Campaign Optimization – End-to-End Data Science Project**

*A Statistical, Predictive & BI Solution for Outbound Banking Campaigns*

---

# ⭐ **Executive Summary**

This project analyzes over **45,000+ customer interactions** from a Portuguese bank’s marketing campaigns to understand why customers subscribe to term deposits — and how the bank can significantly improve campaign ROI.

### 🔥 TL;DR (30-Second Summary)

**Prioritize high-balance, tertiary-educated customers contacted via cellular channels.
Expected uplift: +12–26% in conversions based on statistical and predictive insights.
Use the XGBoost lead-scoring model to identify and target the customers with the highest likelihood of subscription.**

### 🧩 Key Findings

* **Cellular contact is significantly more effective** than telephone (+3pp uplift, p=0.015).
* **Higher account balance strongly predicts subscription** (~35% difference).
* **Education influences conversion** — tertiary customers are most receptive.
* **Retired & unemployed groups engage longest**, improving success likelihood.
* **Leak-free XGBoost model** identifies top 10% high-potential customers with ~2× likelihood.

### 🛠 Deliverables

* ✔ Statistical testing (A/B, Chi-Square, t-Test, ANOVA)
* ✔ Predictive modeling pipeline
* ✔ Champion model (XGBoost, no leakage)
* ✔ FastAPI deployment
* ✔ Power BI storytelling dashboard
* ✔ Economic impact analysis

---

# 🧩 **Business Problem**

The bank invests heavily in outbound calling campaigns, but conversion rates remain **~12%**.
The bank struggles with:

* Inefficient targeting
* No prioritization of high-likelihood customers
* High agent workload with low ROI
* Lack of insight into influential customer characteristics
* No deployable predictive system

---

# 🎯 **Business Requirements**

The project must deliver:

1. **Drivers of subscription** (demographics, financial behavior, past engagement).
2. **Optimal channel strategy** (telephone vs cellular).
3. **Lead scoring to prioritize customers** before calling.
4. **Statistically validated recommendations** (confidence intervals, uplift).
5. **Actionable business insights** for non-technical stakeholders.
6. **Deployed prediction engine** (FastAPI).
7. **Integration-ready outputs** for Power BI, CRM tools, and marketing teams.
8. **Data governance alignment** (fairness, privacy, compliance).

---

# 📁 **Repository Structure (Actual File System)**

This project is organized using a **production-style structure**:

```
📁 Marketing-Campaign-Optimization
│
├── artifacts/
├── Dataset/
├── Images/
├── model/
│   └── champion_pipeline.joblib      ← Final selected model
│
├── Notebook/
│   ├── 01_Bank_Marketing_Data_Understanding_and_Setup.ipynb
│   ├── 02_Bank_Marketing_Statistical_Tests.ipynb
│   └── 03_Bank_Marketing_Predictive_modeling.ipynb
│
├── Report/
│
├── src/
│   ├── api.py
│   └── run_api_setup_commands.txt
│
├── Visualisation/
│   ├── Bank Marketting campaing visualisation.pbix
│
└── README.md
```
---

# 📂 **Phase 1 — Data Understanding & Profiling**

### Key insights:

* **duration** removed due to data leakage.
* **balance** heavily right-skewed → `balance_log` created.
* **pdays, poutcome, previous** highly correlated → engineered into `was_contacted_before`.
* Categorical features encoded properly for modeling.

---

# 🧪 **Phase 2 — Statistical Testing (Business-Driven)**

### 1. **A/B Test — Contact Type**

**Cellular = 15%**, **Telephone = 12%**
Lift = +3pp, p-value = 0.015

**Conclusion:** Cellular contact significantly improves subscriptions.

---

### 2. **Chi-Square — Education**

p ≈ 1.63e-51 → Education strongly influences subscription.

**Tertiary > Secondary > Primary**

---

### 3. **t-Test — Balance Difference**

Subscribers maintain **~35% higher balances** (p < 0.001).

**High financial capacity = higher conversion likelihood.**

---

### 4. **ANOVA — Job Type & Call Duration**

Retired & unemployed groups → longest engagement.

**Guidance:**

* Longer scripts for engaged segments
* Short scripts for busy segments (technicians, students)

---

# 🤖 **Phase 3 — Predictive Modeling**

### Models:

* Logistic Regression (baseline)
* Random Forest (without leakage)
* **XGBoost (Champion)**

### 🏆 **Champion Model: XGBoost (No Duration)**

| Metric   | Validation | Test  |
| -------- | ---------- | ----- |
| AUC      | 0.807      | 0.805 |
| Accuracy | ~83%       | ~83%  |

### Top Predictors:

* Previous campaign success
* Balance_log
* Contact type
* Education
* Housing loan

---

# 📊 **Phase 4 — Power BI Dashboard**

### Page 1 — Campaign Overview

Customer profiles, reach, conversions, seasonality.

### Page 2 — Key Drivers

All statistical test insights visualized.

### Page 3 — Predictive Insights

* Probability distribution
* Segment opportunity matrix
* Key driver charts
* Recommendations panel

---

# 💰 **Phase 5 — Economic Impact (For 10,000 Contacts)**

| Scenario        | Conv Rate | Incremental Conversions | Revenue @ €150 each |
| --------------- | --------- | ----------------------- | ------------------- |
| Baseline        | 12%       | –                       | –                   |
| Model Targeting | 15%       | +300                    | €45,000             |
| Cellular-First  | 14%       | +200                    | €30,000             |

**Total potential uplift (combined strategy): +€75,000 per 10k calls**

---

# 🚀 **FastAPI Deployment**

### Endpoints Overview

| Endpoint                  | Method | Description                                       |
| ------------------------- | ------ | ------------------------------------------------- |
| `/predict`                | POST   | Score a single customer (JSON → probability)      |
| `/predict_batch`          | POST   | Upload CSV, return filename in predictions folder |
| `/predictions/{filename}` | GET    | Download prediction CSV                           |

### Notes:

* `/predict` uses **Pydantic** for strict validation.
* CORS wide open for dev → restrict in production.
* Add **API authentication** (OAuth2/API keys) before deployment.
* Designed for seamless integration with Power BI or CRM.

---

# ⚙️ **Setup & Run Instructions (FastAPI)**

```bash
# 1. Create virtual environment
python -m venv .venv

# 2. Activate (PowerShell)
.venv\Scripts\activate.bat

# 3. Install dependencies
pip install -r artifacts/requirements_clean.txt
# or use full:
pip install -r artifacts/requirements_orginal_backup.txt

# 4. Upgrade pip
python -m pip install --upgrade pip

# 5. Verify installation
python - <<'PY'
import fastapi, uvicorn, pandas, sklearn, joblib, streamlit, xgboost
print("Imports OK")
PY

# 6. Run FastAPI app
uvicorn src.api:app --reload --host 0.0.0.0 --port 8000
```

Open the API docs:
👉 [http://localhost:8000/docs](http://localhost:8000/docs)

---

# 🛡 **Fairness, Governance & Privacy**

* No protected attributes modeled directly (pro-compliance).
* Education-based targeting reviewed for ethical impact.
* GDPR-aligned: prior consent required for outreach.
* Recommended quarterly **model drift monitoring**.

---

# 🔄 **Reproducibility Guarantees**

* Pinned dependency files
* `champion_pipeline.joblib` saved
* Constant seeds for reproducibility
* Sequential Jupyter workflow
* Metadata + comparison results included
* API tested via sample payloads