# Project Description — CareFlow

**Team:** Nurik Najmiddinov, Vaish Koduri\
**Advisor:** Dr. Yu Zhao\
**Course:** CS5001 Senior Design I, University of Cincinnati

## Problem

Hospitals constantly deal with patients being admitted and discharged, beds becoming occupied or free, departments with different levels of demand, staff scheduling, and sudden increases in patient volume (for example, emergency department admissions often rise over weekends, pushing other departments toward capacity). Administrators often rely on spreadsheets, reports, and manual estimates. A traditional dashboard shows what is happening now; it does not show what is likely to happen next.

## Solution

CareFlow brings hospital operational data into one place and uses machine learning to forecast upcoming demand, so administrators can plan beds and staffing before shortages occur. It is an operational planning tool only and does not diagnose patients or make clinical decisions.

## Main Components

1. **Operations dashboard:** admissions, discharges, occupied and available beds, department-level occupancy, staffing, historical trends, and alerts.
2. **Admission forecasting (ML):** seven-day forecasts of patient admissions, comparing models such as Linear Regression, Random Forest, and XGBoost.
3. **Bed occupancy forecasting (ML):** forecasts of department occupancy based on current occupancy, admissions, and discharges, compared against a simple baseline calculation.
4. **Staffing and resource planning:** estimates staffing requirements from the forecasts and highlights possible gaps.
5. **Alerts:** rule-based warnings when forecasts cross capacity thresholds.

## Data

CareFlow uses a Python-generated synthetic dataset (daily admissions, discharges, and occupancy for Emergency, Medical-Surgical, and ICU departments). Whether to add any real-world dataset will be decided with our advisor after the synthetic version works. No real patient data is used without the required training and data use agreements.

## Research Question

How effectively can machine learning models forecast hospital admissions and bed occupancy from historical operational data, and how can those forecasts support resource planning? Models will be evaluated with MAE, RMSE, WAPE, and forecast bias against simple baseline methods.

## Planned Technology

| Area | Technology |
|---|---|
| Frontend | React + TypeScript |
| Backend | Python + FastAPI |
| Database | PostgreSQL |
| Data / ML | Pandas, NumPy, scikit-learn, XGBoost |
| Visualization | Plotly |
| Deployment | Docker, Microsoft Azure, GitHub Actions |

## Out of Scope

Electronic health record integration, patient diagnosis or treatment recommendations, a mobile app, a medical chatbot, and real-time integration with hospital equipment.
