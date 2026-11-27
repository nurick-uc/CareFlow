# CareFlow Task List

CS 5001/5002 Senior Design · Team: Nurik Najmiddinov, Vaishnavi Koduri, Gunnar Heiert

Module names match Project-Description.md and Design D0 to D2. Full plan: [Planning/Plan.md](Planning/Plan.md).

T1. Develop the C5 Operations Database schema, migrations, and seed accounts from the D1 ERD (7 entities, UUID run_id). Module: C5 Operations Database. Owner: Nurik.

T2. Develop the C3 Auth Module: password hashing, 60-minute JWT issue and verification (I3), user lookup over I13, and role checks for the four roles. Module: C3 Auth Module. Owner: Gunnar.

T3. Develop the C2 Backend API skeleton, the OpenAPI contract for I2, and the database access layer for I7. Module: C2 Backend API. Owner: Vaish.

T4. Develop the C4 Data Ingestion upload path: header and row validation, transactional import into C5 (I5, I6), and the rejected-row validation report. Module: C4 Data Ingestion. Owner: Nurik.

T5. Develop the C1 Web Dashboard shell: sign-in page, navigation, department filter, and current-operations views over I1 and I2. Module: C1 Web Dashboard. Owner: Vaish.

T6. Obtain and validate the Python-generated synthetic dataset for the three departments and build the feature set used by the C6 Forecasting Service. Module: C6 Forecasting Service. Owner: Nurik.

T7. Develop the C6 Forecasting Service: 7-day admission and bed occupancy models, the baseline, and the ForecastRun states QUEUED, RUNNING, SUCCESS, FAILED (I8, I10, I11). Module: C6 Forecasting Service. Owner: Nurik.

T8. Develop the C7 Planning & Alerts rules that compare forecasts with capacity settings and staffing ratios and write flags to C5 (I9, I12). Module: C7 Planning & Alerts. Owner: Gunnar.

T9. Develop the C1 Web Dashboard forecast, alert, and upload pages with Plotly charts, the 90% threshold line, and data-table alternatives. Module: C1 Web Dashboard. Owner: Vaish.

T10. Develop the deployment pipeline: Docker images for C1, C2, and C6, GitHub Actions CI, and an Azure staging environment. Module: Microsoft Azure (deployment). Owner: Gunnar.

T11. Test the integrated system: integration tests for I1 to I13, role-access tests, and timing tests for the 3 s, 2 min, and 30 s budgets. Module: C1 to C7 (system). Owner: Gunnar.

T12. Validate and refine the C6 Forecasting Service models against the baseline using MAE, RMSE, WAPE, and forecast bias. Module: C6 Forecasting Service. Owner: Nurik.

T13. Document the user guide, deployment guide, and final design report, and update README.md and Design_Diagrams to match the built system. Module: All modules (documentation). Owner: Gunnar.

T14. Refine C1 and C2 by fixing defects found in T11 and applying accessibility and usability fixes before release v1.0. Module: C1 Web Dashboard, C2 Backend API. Owner: Vaish.

T15. Develop the C1 Web Dashboard settings and administration pages: capacity thresholds, staffing ratios, and user role management for the admin role. Module: C1 Web Dashboard. Owner: Vaish.

