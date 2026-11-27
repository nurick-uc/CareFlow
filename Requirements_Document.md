# CareFlow
# Requirements Document
 
**Team Members:** Vaishnavi Koduri, Nurik Najmiddinov, Gunnar Heiert  
**Advisor:** Dr. Yu Zhao  
**Version:** 1.0 – Team-Approved Draft  
**Date:** November 27, 2026  
**Status:** Team Approved; Advisor Review Pending

---

## 1. Document Control

### 1.1 Version History

| Version | Date | Author | Description |
|---|---|---|---|
| 0.1 | November 27, 2026 | CareFlow Team | Initial requirements draft based on user stories, D0, D1, Week 3 constraints, and Assignment 8 planning. |
| 0.2 | November 27, 2026 | CareFlow Team | Updated using Design D2, including component responsibilities, role-based access, API behavior, CSV validation, and error handling. |
| 1.0 | November 27, 2026 | CareFlow Team | Team-approved baseline. All three listed team members confirmed that they were comfortable with the proposed requirements and decisions. Advisor review remains pending. |

### 1.2 Approval Record

The CareFlow team reviewed the requirements and confirmed that they were comfortable with the proposed scope, priorities, and decisions.

| Team Member | Review Result | Date |
|---|---|---|
| Vaishnavi Koduri | Approved | November 27, 2026 |
| Nurik Najmiddinov | Approved | November 27, 2026 |
| Gunnar Heiert | Approved | November 27, 2026 |

Advisor review by Dr. Yu Zhao has not yet been recorded. No advisor approval is claimed.

## 2. Purpose and Scope

### 2.1 Purpose

This document defines the functional and non-functional requirements for CareFlow. It identifies what the system must do, who it is intended to support, the constraints governing development, and the measurable conditions used to verify system behavior.

The requirements are based on the CareFlow user stories, Design D0, Design D1, Design D2, the Week 3 Constraints Essay, and the Assignment 8 implementation plan.

This document serves as the requirements baseline for the Technical Specification and subsequent implementation and testing activities.

### 2.2 System Purpose

CareFlow is an AI-powered hospital operations and resource planning platform designed to help hospital administrators anticipate patient demand by forecasting admissions and bed occupancy for the next seven days and identifying potential capacity and staffing shortages.

The system receives historical, aggregated hospital operational data through CSV uploads. It validates the uploaded information, stores valid observations, generates forecasts, calculates staffing estimates, and displays operational summaries and planning alerts through a web dashboard.

The initial system uses synthetic operational data representing three hospital departments:

- Emergency
- Medical-Surgical
- Intensive Care Unit (ICU)

CareFlow supports operational planning and human decision-making. It does not provide clinical diagnoses, treatment recommendations, automatic bed assignments, or automatic staff scheduling.

### 2.3 In-Scope Functionality

The initial CareFlow release includes:

- User authentication using email and password.
- Role-based access control for Administrator, Bed Manager, Charge Nurse, and Data Manager.
- CSV uploads containing aggregated daily operational information.
- CSV file validation, including required headers, field formats, and value constraints.
- Upload results containing accepted-row counts, rejected-row counts, and validation errors.
- Storage of valid daily department-level observations.
- Current operational summaries and department-level information.
- Seven-day admissions and occupied-bed forecasts.
- Forecast status tracking using QUEUED, RUNNING, SUCCESS, and FAILED.
- Capacity warnings based on configured occupancy thresholds.
- Department staffing estimates and staffing-gap information.
- Accessible charts, data tables, labeled controls, and error messages.
- Error handling for invalid requests, insufficient data, authentication failures, database failures, and forecast failures.

### 2.4 Out-of-Scope Functionality

The following functionality is excluded from the initial release:

- Patient diagnosis or treatment recommendations.
- Patient-level clinical records or patient-identifiable information.
- Automatic bed assignment.
- Automatic staffing assignments or schedule changes.
- Live EHR integration.
- Real-time hospital information-system feeds.
- Sensor or medical-device integration.
- Autonomous clinical or operational decisions.

These exclusions preserve the project's privacy, budget, and safety boundaries.

## 3. Stakeholders and User Goals

CareFlow supports hospital operations personnel who need to understand current capacity and anticipate future resource requirements.

| Stakeholder | Role in the System | Goal | Source |
|---|---|---|---|
| Hospital Administrator | Primary user | View predicted admissions and bed occupancy for the next seven days to plan hospital resources. | US-01 |
| Bed Manager | Primary user | Monitor current and predicted bed occupancy across departments and identify potential capacity problems. | US-02 |
| Charge Nurse | Primary user | Compare estimated staffing requirements with available staffing levels in a department. | US-03 |
| Hospital Data Manager | Supporting user | Upload and validate operational data so that forecasts use accurate information. | US-04 |
| Hospital staff member using assistive technology | Accessibility stakeholder | Access operational reports and forecast information independently. | US-05 |

### 3.1 User Stories

**US-01 – Forecast Hospital Demand**

As a hospital administrator, I want to view predicted hospital admissions and bed occupancy for the upcoming seven days, so that I can prepare for changes in patient demand and plan hospital resources.

**US-02 – Monitor Bed Availability**

As a bed manager, I want to view current and predicted bed occupancy across hospital departments, so that I can identify departments approaching capacity and prepare for possible bed shortages.

**US-03 – Estimate Staffing Requirements**

As a charge nurse, I want to compare estimated staffing requirements with available staffing levels in my department, so that I can identify possible staffing shortages and inform the appropriate personnel.

**US-04 – Provide Operational Data**

As a hospital data manager, I want to upload and validate hospital operational data, so that CareFlow uses accurate information when generating forecasts and reports.

**US-05 – Access Information Using Assistive Technology**

As a hospital staff member who uses a screen reader, I want to access operational reports and forecast information in an accessible format, so that I can independently understand information needed for my work.

## 4. Glossary

| Term | Definition |
|---|---|
| Administrator | A CareFlow user authorized to review hospital-wide operational information and forecasts and manage planning settings. |
| Bed Manager | A CareFlow user who monitors bed occupancy and capacity information. |
| Charge Nurse | A CareFlow user who reviews department-level staffing estimates and possible staffing gaps. |
| Data Manager | A CareFlow user responsible for uploading operational CSV files. |
| Department | A hospital unit represented in CareFlow, initially Emergency, Medical-Surgical, or ICU. |
| Daily Observation | An aggregated record for one department and date containing admissions, discharges, occupied beds, bed capacity, and staff on shift. |
| Forecast | An estimate of future admissions and occupied beds generated from historical observations. |
| Forecast Run | One execution of the forecasting process, identified by a unique run ID and processing status. |
| Forecast Horizon | The number of future days covered by a forecast. The primary CareFlow forecast horizon is seven days. |
| Capacity Flag | A warning produced when predicted occupancy reaches or exceeds the configured capacity threshold. |
| Staffing Estimate | An estimate of required staff compared with available staff for a department and date. |
| Staffing Gap | The difference between estimated required staff and available staff. |
| Planning Setting | A department-level configuration containing planning assumptions such as the capacity threshold and patients-per-staff ratio. |
| Synthetic Data | Artificially generated operational data that does not identify real patients. |
| JWT | A signed JSON Web Token used to authenticate protected API requests. |
| RBAC | Role-Based Access Control, which restricts actions according to a user's assigned role. |
| CSV | Comma-Separated Values file used for operational-data import. |
| MAE | Mean Absolute Error, a measure of average absolute prediction error. |
| Baseline Forecast | A simple reference forecast used to compare forecasting-model performance. |
| D0 | CareFlow high-level architecture and interface design. |
| D1 | CareFlow detailed database, forecasting, and planning design. |
| D2 | CareFlow detailed dashboard, API, authentication, data ingestion, and edge-case design. |
| C1–C7 | The seven logical CareFlow software components defined in D0. |
| I1–I13 | The thirteen numbered interfaces established in D0. |
| MoSCoW | A prioritization method that classifies requirements as Must, Should, Could, or Won't Have. |

## 5. Functional Requirements

Each requirement has a unique identifier, priority, source user story, and verification method.

| ID | Functional Requirement | Priority | Source Story | Verification Method |
|---|---|---|---|---|
| REQ-01 | The system shall authenticate users using email and password and restrict protected operations according to the user's assigned CareFlow role. | Must | US-01, US-02, US-03, US-04 | Test valid and invalid credentials and attempt protected actions using each of the four roles. Verify that authorized actions succeed and unauthorized actions are rejected. |
| REQ-02 | The system shall accept UTF-8 CSV files no larger than 10 MB containing the required fields: date, department, admissions, discharges, occupied_beds, bed_capacity, and staff_on_shift. | Must | US-04 | Upload valid files, files at the size limit, files exceeding the size limit, and files with missing required headers. |
| REQ-03 | The system shall provide a validation report for each CSV upload containing accepted-row count, rejected-row count, and row-level errors identifying the row number, field, and reason for rejection. | Should | US-04 | Upload files containing invalid dates, negative values, invalid departments, duplicate department/date records, and occupied beds greater than capacity. Verify the report. |
| REQ-04 | The system shall generate admissions and occupied-bed forecasts for up to seven consecutive future days for a hospital-wide or selected-department scope when at least 60 days of valid historical observations are available. | Must | US-01, US-02 | Generate forecasts for hospital-wide and individual-department scopes using at least 60 valid historical days. Verify the forecast dates and predicted values. |
| REQ-05 | The system shall reject a forecast request when fewer than 60 days of valid historical observations are available for the requested scope and return an insufficient-data error. | Should | US-01 | Submit a forecast request with fewer than 60 valid historical days and verify that no new successful forecast is published. |
| REQ-06 | The system shall display current and predicted bed occupancy by department and identify dates when predicted occupancy reaches or exceeds the configured capacity threshold. The default capacity threshold shall be 90%. | Should | US-02 | Test predicted occupancy below, equal to, and above the configured threshold. Verify that the correct capacity flags are displayed. |
| REQ-07 | The system shall calculate and display department staffing estimates using the configured patients-per-staff assumption and available staff count, including the resulting staffing gap. | Should | US-03 | Configure a department staffing ratio and compare the system's result against an independently calculated expected staffing estimate. |
| REQ-08 | The system shall provide accessible alternatives to graphical information, including equivalent data tables, labeled controls, and accessible error messages. | Should | US-05 | Inspect every dashboard chart for an equivalent table and complete primary user tasks using keyboard navigation and assistive technology. |

### 5.1 Functional Requirement Clarifications

- The primary forecast horizon is seven days. D2 also specifies that supported request values may range from one through seven days.
- A forecast requires at least 60 days of valid historical observations for the requested scope.
- A missing required CSV header causes the entire file to be rejected.
- Invalid individual rows are rejected and identified in the validation report while valid rows may continue through the import process.
- Duplicate department/date observations are not silently combined or double-counted.
- If a new forecast fails, the most recent successful forecast remains available.
- A successful CSV import is not undone if the subsequent forecast operation fails.
- Staffing estimates must not be generated using an invented staffing ratio when the required department configuration is missing.

## 6. Non-Functional Requirements

| ID | Non-Functional Requirement | Priority | Source Story | Verification Method |
|---|---|---|---|---|
| NFR-01 | The system shall return stored operational information and previously generated forecast results within 3 seconds under the planned workload of three departments and one year of daily records. | Must | US-01, US-02 | Measure API and database response times using the defined dataset and record the results. |
| NFR-02 | The system shall complete a new seven-day forecast within 120 seconds under the planned workload of three departments and one year of daily records. | Must | US-01 | Measure forecast execution time from request acceptance to successful completion. |
| NFR-03 | The system shall complete CSV validation and return the validation report within 30 seconds for the planned 90-day, three-department sample file, provided the file is no larger than 10 MB. | Should | US-04 | Upload the defined sample file and measure the time until the validation report is returned. |
| NFR-04 | The system shall protect all non-login API endpoints using signed JWT access tokens that expire no later than 60 minutes after issue, enforce role authorization on the server, and use HTTPS for browser/API communication. | Must | US-01, US-02, US-03, US-04 | Test missing, invalid, and expired tokens; test role permissions; verify HTTPS configuration and token expiration. |
| NFR-05 | The system shall provide an equivalent data-table view for 100% of dashboard charts and allow keyboard access to all primary dashboard tasks without requiring a mouse. | Should | US-05 | Inspect each chart and complete login, navigation, filtering, upload, and report-viewing tasks using keyboard navigation. |
| NFR-06 | The system shall preserve the most recent successful forecast when a new forecast fails and shall not publish an incomplete or failed forecast as a successful result. | Must | US-01, US-02 | Simulate forecast-processing and database-write failures. Verify the FAILED status and continued availability of the previous successful forecast. |
| NFR-07 | The system shall use a relational database with primary keys, foreign keys, unique constraints, and transaction handling to preserve operational data integrity. | Must | US-04 | Test duplicate department/date records, invalid department references, and transaction rollback behavior. |
| NFR-08 | The system shall not store patient-identifiable information in the initial implementation. | Must | US-04 | Inspect the CSV contract, database schema, and uploaded test data for patient names, dates of birth, medical record numbers, or other patient identifiers. |
| NFR-09 | The system shall support containerized deployment in the selected Azure for Students environment. | Should | All | Deploy the application using the documented container configuration and record deployment results and resource consumption. |

### 6.1 Performance Test Workload

To make performance requirements measurable, the team will use the following planned test profile:

- Three departments: Emergency, Medical-Surgical, and ICU.
- One year of daily operational records for dashboard and forecast performance tests.
- A 90-day, three-department sample CSV for the initial validation timing test.
- CSV uploads must remain within the 10 MB file-size limit.

The 3-second, 30-second, and 120-second targets are design targets. They must be demonstrated through testing before being marked as verified.

### 6.2 Security and Reliability Clarifications

- Passwords must never be stored in plaintext.
- Authentication uses signed JWTs with a 60-minute expiration.
- C2 must enforce authorization even if C1 hides an unavailable action.
- Authentication fails safely if the user database is unavailable.
- Passwords, plaintext credentials, tokens, and patient-identifiable information must not appear in logs.
- A failed import transaction must roll back rather than leave partially committed data.
- A failed forecast must not replace the most recent successful forecast.
- A successful import remains committed even if the forecast triggered afterward fails.

## 7. MoSCoW Prioritization

### 7.1 Must Have

The following requirements are essential to the initial CareFlow release:

- REQ-01 — User authentication and role-based access.
- REQ-02 — Required CSV upload format and 10 MB file-size limit.
- REQ-04 — Seven-day admissions and occupied-bed forecasting.
- NFR-01 — Stored information returned within 3 seconds under the defined workload.
- NFR-02 — Forecast completed within 120 seconds under the defined workload.
- NFR-04 — HTTPS, signed JWT authentication, and server-side role authorization.
- NFR-06 — Preserve the previous successful forecast when a new forecast fails.
- NFR-07 — Relational database integrity and transaction handling.
- NFR-08 — No patient-identifiable information in the initial implementation.

### 7.2 Should Have

The following requirements are important and should be implemented if time and resources permit:

- REQ-03 — Detailed CSV validation reports.
- REQ-05 — Explicit insufficient-history rejection.
- REQ-06 — Occupancy display and capacity warnings.
- REQ-07 — Staffing estimates and staffing-gap information.
- REQ-08 — Accessible chart alternatives and controls.
- NFR-03 — CSV validation report within 30 seconds.
- NFR-05 — Keyboard accessibility for primary dashboard tasks.
- NFR-09 — Containerized Azure deployment.

### 7.3 Could Have

No separate Could Have requirement is assigned in this baseline. A new Could Have item may be added if the team identifies a useful enhancement that does not displace Must Have or Should Have functionality.

### 7.4 Won't Have for This Release

The following functionality is intentionally excluded:

- Patient diagnosis or treatment recommendations.
- Patient-level clinical records.
- Automatic bed assignment.
- Automatic staff scheduling or schedule changes.
- Live EHR integration.
- Real-time hospital information-system feeds.
- Sensor or medical-device integration.
- Autonomous clinical or operational decisions.

Any change to these exclusions requires a documented scope change and team/advisor review.

## 8. Constraints

The following constraints are inherited from the Week 3 Constraints Essay.

| ID | Constraint | Category | Design Consequence |
|---|---|---|---|
| CON-01 | The project has no funding beyond team resources and the Azure for Students allowance described in the Week 3 essay: $100 in credit for 12 months. The project must use free/open-source tools and the student Azure environment. | Economic | Use small Azure deployment tiers, free/open-source software, and local model training. Avoid paid GPU training and premium always-on services. |
| CON-02 | Access to restricted real hospital data requires appropriate training, institutional approval, and a data-use agreement. | Legal | Use synthetic data for the initial implementation. Do not use restricted hospital records without required approval. |
| CON-03 | The initial system uses synthetic, aggregated department-level operational data. Patient names, dates of birth, medical record numbers, and other patient identifiers are excluded. | Privacy | Keep the CSV contract and database schema at department/day level. Do not introduce patient-level entities or identifiers. |
| CON-04 | Browser/API communication must use HTTPS, and protected application functionality must require authentication and role-based access. | Security | Enforce authentication and authorization on the backend. Frontend visibility alone is not an access-control mechanism. |
| CON-05 | Database credentials must be stored in GitHub Actions secrets rather than committed to the repository. Database firewall rules must restrict access to the backend address. | Security | Keep credentials outside source control and restrict database ingress. Private networking and managed key vault services were considered too expensive for the stated project budget. |
| CON-06 | Forecasts must be presented as estimates with measured error compared with a baseline. Staffing alerts are estimates that require human review. | Ethical | Clearly label forecasts and alerts as decision-support information. Do not implement autonomous clinical decisions, automatic bed assignments, or automatic staffing changes. |

### 8.1 Stakeholder Terminology

The Week 3 Constraints Essay describes two broad user groups: hospital administrators and department managers. D0 and D2 define four specific application roles: Administrator, Bed Manager, Charge Nurse, and Data Manager.

This document uses the four application roles when specifying system access while retaining the two broad stakeholder categories from the earlier project description.

The role-to-endpoint permissions are based on the proposed D2 matrix. The team has accepted the proposed matrix as the working design baseline; implementation and testing must still verify that the system enforces it correctly.

## 9. Assumptions and Open Questions

| ID | Assumption or Open Question | Owner | Target Date | Status |
|---|---|---|---|---|
| AQ-01 | The initial dataset will remain synthetic and represent Emergency, Medical-Surgical, and ICU departments. | Nurik Najmiddinov | November 30, 2026 | Supported by D0, D1, and D2. Verify final data generator and sample dataset. |
| AQ-02 | Forecast generation requires at least 60 days of valid historical observations for the requested scope. | Nurik Najmiddinov | November 30, 2026 | Defined in D0/D1/D2. Verify implementation behavior. |
| AQ-03 | The default capacity threshold remains 90%, with department-specific planning settings supported. | Vaishnavi Koduri | November 30, 2026 | Defined in D1/D2. Verify configuration behavior. |
| AQ-04 | The four application roles are Administrator, Bed Manager, Charge Nurse, and Data Manager. | Nurik Najmiddinov | November 30, 2026 | Defined in D0/D2. Verify endpoint permissions during implementation. |
| AQ-05 | Performance tests will use three departments and one year of daily records; CSV validation tests will use the planned 90-day sample. | Vaishnavi Koduri | November 30, 2026 | Proposed test profile. Confirm dataset and execution environment. |
| AQ-06 | Real hospital data will not be introduced unless required institutional approvals and a data-use agreement are obtained. | Active project members | November 30, 2026 | Consistent with CON-02. |
| AQ-07 | The project team consists of Vaishnavi Koduri, Nurik Najmiddinov, and Gunnar Heiert. | CareFlow Team | November 27, 2026 | Team review completed. |
| AQ-08 | The proposed D2 role-permission matrix is the working authorization baseline. | CareFlow Team | November 27, 2026 | Team accepted the proposed matrix for the project baseline. |
| AQ-09 | The system must retain or otherwise retrieve upload-batch status and validation results for GET `/api/v1/uploads/{batch_id}`. | Nurik Najmiddinov | November 30, 2026 | D2 requires status retrieval; persistence details must remain consistent with D1 and the implementation. |
| AQ-10 | The team must confirm how partial CSV imports are represented when valid rows are committed and invalid rows are rejected. | Vaishnavi Koduri | November 30, 2026 | D2 describes accepted/rejected rows and transactional insertion; final batch-status vocabulary must be consistent with the implementation. |
| AQ-11 | The system must display staffing estimates as unavailable when the required department staffing configuration is missing. | Vaishnavi Koduri | November 30, 2026 | Defined in D2; implementation must preserve this behavior. |

## 10. Review and Approval Record

**Document version:** 1.0  
**Team review status:** Approved  
**Advisor review status:** Pending

### 10.1 Team Review

All three listed CareFlow team members confirmed that they were comfortable with the proposed requirements, priorities, scope, and technical decisions.

| Reviewer | Review Result | Date | Notes |
|---|---|---|---|
| Vaishnavi Koduri | Approved | November 27, 2026 | Team-approved requirements baseline. |
| Nurik Najmiddinov | Approved | November 27, 2026 | Team-approved requirements baseline. |
| Gunnar Heiert | Approved | November 27, 2026 | Team-approved requirements baseline. |

### 10.2 Advisor Review

