# Constraints Essay — CareFlow: AI-Powered Hospital Operations and Resource Planning Platform

**Team members:** Nurik Najmiddinov, Vaish Koduri\
**Course:** CS5001 Senior Design, University of Cincinnati\
**Advisor:** Dr. Yu Zhao

## Economic

CareFlow has no funding beyond our own pockets, so the stack is limited to free and open-source tools (React, FastAPI, PostgreSQL, scikit-learn, XGBoost, Docker) plus Azure for Students, which gives each of us $100 of credit for 12 months. That cap rules out GPU training and always-on premium cloud tiers, so we will train the forecasting models locally and deploy only the dashboard, API, and database on the smallest Azure tiers, shutting them down between demos.

## Legal

MIMIC-IV can only be used after each team member completes CITI human-subjects and HIPAA training and signs the PhysioNet Credentialed Health Data Use Agreement, which forbids sharing the data with anyone not covered by it. PhysioNet's guidance also prohibits sending MIMIC data through third-party APIs or online chat tools, so no restricted record may ever be pasted into the AI assistants we use for coding and writing help. For this reason, CareFlow's first version runs on a Python-generated synthetic dataset of daily admissions, discharges, and bed occupancy for three departments (Emergency, Medical-Surgical, ICU), with MIMIC-IV treated as an optional later upgrade. Real MIMIC-IV data would make our forecasts more credible but would require training for both members and separate locked-down storage, so we have deferred that decision until Dr. Zhao helps us judge whether the added realism is worth the cost in time.

## Security

Even with synthetic data, CareFlow is designed as if it held protected health information: the database stores only department-level daily counts and never patient names, dates of birth, or record numbers. Every API endpoint will require login with role-based access for our two user groups, hospital administrators and department managers, with all traffic over HTTPS and database credentials stored in GitHub Actions secrets rather than in the repository. Security and cost pull against each other here: a private network and managed key vault would exhaust the $100 credit, so we chose a single PostgreSQL instance with firewall rules allowing only our backend's address, a balance that is acceptable only because the data contains no real patients.

## Ethical

Because a wrong forecast could lead a bed manager to under-staff the ICU, CareFlow is limited to operational planning and never recommends diagnoses, treatments, or decisions about individual patients. Every prediction will display its measured error (MAE) beside a simple baseline forecast, and every staffing alert is labeled as an estimate that a human must review before acting on it.
