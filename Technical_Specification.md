# CareFlow
# Technical Specification

**Team Members:** Vaishnavi Koduri, Nurik Najmiddinov, Gunnar Heiert  
**Advisor:** Dr. Yu Zhao  
**Version:** 1.0 – Team-Approved Draft  
**Date:** November 27, 2026  
**Requirements Baseline:** Requirements Document v1.0  
**Status:** Team Approved; Advisor Review Pending

---

## 1. Document Control and Purpose

### 1.1 Version History

| Version | Date | Author | Description |
|---|---|---|---|
| 0.1 | November 27, 2026 | CareFlow Team | Initial technical specification based on D0, D1, and the initial requirements draft. |
| 0.2 | November 27, 2026 | CareFlow Team | Updated using D2 and the Requirements Document. Added detailed role behavior, interfaces, upload rules, endpoint behavior, and D2 edge cases. |
| 1.0 | November 27, 2026 | CareFlow Team | Team-approved technical baseline. All three listed team members confirmed that they were comfortable with the proposed technical decisions. Advisor review remains pending. |

### 1.2 Purpose

This document describes the technical architecture and implementation behavior of CareFlow. It defines the responsibilities of the system components, their interfaces, data formats, API endpoints, error behavior, technology stack, constraints, and traceability between requirements and design elements.

This specification is based on:

- Design D0 – High-Level System Architecture.
- Design D1 – Detailed Database, Forecasting, and Planning Design.
- Design D2 – Detailed Dashboard, Backend API, Authentication, Data Ingestion, and Edge-Case Design.
- Requirements Document v1.0.

The Technical Specification remains consistent with Requirements Document v1.0. Changes to a requirement must be reflected in the affected technical sections and traceability rows.

## 2. System Architecture

### 2.1 Architecture Overview

CareFlow uses a layered client-server architecture with a data-ingestion and forecasting pipeline. The initial implementation uses a modular monolithic backend rather than independently deployed microservices.

The browser dashboard communicates with the Backend API through HTTPS. The Backend API coordinates authentication, data ingestion, database operations, forecasting, and planning functions.

The Operations Database is the persistent source of truth for operational observations, user accounts, forecast runs, forecast values, planning settings, staffing estimates, and planning flags.

The architecture contains seven logical components:

| Component | Name | Responsibility | Design Source |
|---|---|---|---|
| C1 | Web Dashboard | Displays operational summaries, forecasts, staffing estimates, alerts, upload results, and accessible data tables. | D0, D2 |
| C2 | Backend API | Receives requests from the dashboard, validates them, checks authorization, and routes them to internal components. | D0, D2 |
| C3 | Authentication Module | Verifies credentials, validates JWTs, and evaluates role-based permissions. | D0, D2 |
| C4 | Data Ingestion | Receives CSV files, validates their contents, and imports valid records into the database. | D0, D2 |
| C5 | Operations Database | Stores operational observations, user accounts, forecast data, and planning information. | D0, D1 |
| C6 | Forecasting Service | Generates seven-day admissions and occupied-bed forecasts. | D0, D1 |
| C7 | Planning and Alerts | Evaluates forecast results and generates capacity flags and staffing estimates. | D0, D1 |

### 2.2 Architecture Diagram References

The following existing diagrams should be referenced rather than recreated:

| Diagram | Repository File or Source | Purpose |
|---|---|---|
| D0 Block Diagram | `Design_Diagrams/D0_Block_Diagram.png` | Shows the seven system components and their interfaces. |
| D0 Data Flow | `Design_Diagrams/D0_Data_Flow.png` | Shows how information moves through the system. |
| D1 Entity Relationship Diagram | `Design_Diagrams/D1_ERD_1.png` | Shows the relational database entities and relationships. |
| D2 Overall Architecture | Figure 1 in D2 | Shows the overall architecture and numbered interfaces. |
| D2 Dashboard Mockup | Figure 2 in D2 | Shows the proposed dashboard layout. |
| D2 Authentication Flow | Figure 3 in D2 | Shows login, JWT verification, and authorization. |
| D2 CSV Upload Flow | Figure 4 in D2 | Shows CSV validation, transaction handling, and forecast triggering. |
| D2 Forecast State Machine | Figure 5 in D2 | Shows QUEUED, RUNNING, SUCCESS, and FAILED states. |

The D2 document is maintained as a separate design artifact in the CareFlow repository.

### 2.3 Component Interaction

The normal system workflow is:

1. A user opens the CareFlow web dashboard.
2. C1 checks whether a valid authentication session is available.
3. If the user is not authenticated, C1 displays the login page.
4. C1 sends login information to C2.
5. C2 requests authentication from C3.
6. C3 retrieves account information from C5 through I13 and verifies the password.
7. C3 issues a signed JWT after successful authentication.
8. C1 uses the authenticated session to request authorized operational information.
9. C2 verifies the token and authorization through C3.
10. C2 retrieves operational data and planning information from C5 or routes the request to the appropriate component.
11. C1 displays operational summaries, forecasts, staffing estimates, and planning flags.
12. An authorized Data Manager can submit a CSV file through C1 and C2.
13. C4 validates the file and submits valid observations to C5 through I6.
14. After a successful import commit, C4 triggers C6 through I10.
15. C6 creates and manages a ForecastRun record and generates forecast values.
16. C7 evaluates successful forecast results and produces planning flags and staffing estimates.
17. C1 retrieves and displays the resulting information through C2.

A successful data import is not undone if a subsequent forecast fails.

## 3. Component Specifications

### 3.1 C1 – Web Dashboard

**Purpose:** C1 provides the browser interface through which users interact with CareFlow.

**Responsibilities:**

- Display current operational information.
- Display seven-day admissions and bed-occupancy forecasts.
- Allow hospital-wide or department-specific selection.
- Display staffing estimates and possible shortages.
- Allow authorized Data Managers to upload CSV files.
- Display upload-validation results.
- Display forecast status and system errors.
- Provide accessible equivalents for charts and visual information.

**Communication:** C1 communicates with C2 through I2. It does not communicate directly with the database.

**Frontend data objects:**

| Object | Attributes | Purpose |
|---|---|---|
| UserSession | access_token, user_role, expires_at | Represents the current authenticated session. |
| DashboardFilter | scope, from_date, to_date | Stores selected dashboard filters. |
| ForecastView | run_id, forecast_dates, forecast_values, generated_at | Holds forecast information for display. |
| OperationsView | department, admissions, discharges, occupied_beds, bed_capacity | Holds operational summary information. |
| UploadView | filename, upload_status, rows_accepted, rows_rejected | Holds CSV upload results. |
| ErrorView | error_code, message, request_id | Holds user-visible error information. |
| UIState | selected_page, loading, selected_department | Controls the current interface state. |

These objects represent temporary frontend state. They do not create additional persistent database entities.

**Behavior:**

1. The application starts in the user's browser.
2. C1 checks for a valid authentication session.
3. If the user is not authenticated, C1 displays the login page.
4. After successful authentication, C1 loads the dashboard.
5. C1 requests authorized operational information through C2.
6. C1 displays operational summaries.
7. The user selects a department or hospital-wide scope.
8. C1 submits the selected filters to C2.
9. C2 returns operational information and available forecast results.
10. C1 displays information through KPI cards, charts, and accessible tables.
11. If a user uploads a CSV, C1 checks the file type and size before submission.
12. C1 submits the file through C2.
13. C1 displays the validation report returned by the backend.
14. If an error occurs, C1 displays an accessible error message and an appropriate retry or correction option.
15. The user can log out or return to the login page when the authentication token expires.

**Error handling:**

- Invalid inputs are displayed next to the relevant field.
- Expired sessions return the user to the login page.
- Temporary network failures display a retry option.
- Previously retrieved information may remain visible during a temporary failure, with an indication that it may be outdated.
- Errors must be accessible to users relying on assistive technology.

### 3.2 C2 – Backend API

**Purpose:** C2 is the central communication layer between C1 and the internal CareFlow components.

**Responsibilities:**

- Receive HTTPS requests from C1.
- Validate request parameters and data formats.
- Verify authentication and authorization through C3.
- Route requests to C4, C5, C6, or C7.
- Format results into standardized JSON responses.
- Assign or propagate request identifiers.
- Log unexpected errors without exposing sensitive information.

**Technology:** Python and FastAPI.

**Data objects:**

| Object | Attributes | Purpose |
|---|---|---|
| APIRequest | request_id, endpoint, method, user_id | Represents an incoming API request. |
| APIResponse | request_id, status_code, response_body | Represents an API response. |
| APIError | error_code, message, details, request_id | Represents an application error. |
| ForecastRequest | scope, horizon_days | Contains forecast request parameters. |
| PlanningRequest | scope, from_date, to_date | Contains planning-information filters. |
| UploadRequest | filename, file_content, uploader_id | Contains upload information. |

These are temporary request/response structures and do not create additional persistent database entities.

**Request behavior:**

1. C2 receives an HTTPS request from C1.
2. C2 identifies the endpoint and HTTP method.
3. C2 validates the request parameters and data formats.
4. C2 extracts the authorization token when required.
5. C2 sends the token to C3 for authentication and authorization verification.
6. If authentication fails, C2 returns HTTP 401.
7. If authorization fails, C2 returns HTTP 403.
8. If the request is valid, C2 routes it to the appropriate internal component.
9. C4 processes CSV upload requests.
10. C5 handles database operations.
11. C6 processes forecast requests.
12. C7 provides staffing estimates and capacity flags.
13. C2 receives the result from the internal component.
14. C2 formats the result into a standardized JSON response.
15. C2 returns the response to C1.

**Error behavior:**

| Condition | HTTP Status | Behavior |
|---|---:|---|
| Invalid request parameters | 400 | Return a validation error. |
| Missing or invalid authentication | 401 | Reject the request. |
| Insufficient permissions | 403 | Reject the request. |
| Requested resource not found | 404 | Return a not-found error. |
| Uploaded file exceeds maximum size | 413 | Reject the upload. |
| Invalid or insufficient operational data | 422 | Return a data-validation error. |
| Rate limit exceeded, if rate limiting is enabled | 429 | Reject or defer the request. |
| Unexpected internal error | 500 | Return a standardized server error. |
| Required service or database unavailable | 503 | Return a service-unavailable error. |

If C5 or another required dependency becomes unavailable, C2 returns HTTP 503 instead of returning incomplete or misleading information.

Unexpected exceptions are logged with a request identifier. Passwords and access tokens must not be written to logs.

### 3.3 C3 – Authentication Module

**Purpose:** C3 verifies the identity and access permissions of CareFlow users.

**Supported roles:**

1. Administrator
2. Bed Manager
3. Charge Nurse
4. Data Manager

**Technology:** Signed JSON Web Tokens (JWTs), with a 60-minute expiration.

**Data objects:**

| Object | Attributes | Persistence |
|---|---|---|
| User | user_id, email, password_hash, role, active | Stored in C5. |
| AuthenticationToken | token_id, user_id, issued_at, expires_at | Logical token representation; a separate persistent session table is not required by D2. |
| AuthorizationResult | user_id, role, authorized, reason | Temporary authorization result. |

**Login behavior:**

1. C3 receives login credentials from C2.
2. C3 checks that the email and password fields are present.
3. C3 retrieves the corresponding user account from C5.
4. C3 checks whether the account exists and is active.
5. C3 verifies the submitted password against the stored password hash.
6. If the credentials are invalid, C3 returns a generic authentication error.
7. If the credentials are valid, C3 generates a signed JWT.
8. The token includes the user ID, assigned role, and expiration information.
9. C3 returns the token and associated user information to C2.

**Protected-request behavior:**

1. C2 receives a protected request.
2. C2 sends the token to C3.
3. C3 verifies the token signature and expiration.
4. C3 checks the user's role against the requested operation.
5. C3 returns an authentication and authorization result to C2.
6. C2 either allows the operation or returns HTTP 401/403.

**Team-approved working role-access matrix:**

| Function | Administrator | Bed Manager | Charge Nurse | Data Manager |
|---|---|---|---|---|
| View hospital-wide dashboard | Yes | Yes | No | No |
| View department dashboard | Yes | Yes | Yes | No |
| View forecasts | Yes | Yes | Yes | No |
| Request new forecast | Yes | No | No | No |
| View staffing estimates | Yes | Yes | Yes | No |
| Upload CSV data | No | No | No | Yes |
| Modify planning settings | Yes | No | No | No |

This is the proposed access-control matrix from D2, accepted by the team as the working design baseline. The implementation must enforce the matrix on the backend. Hiding a dashboard feature does not replace server-side authorization.

**Security and error handling:**

- Passwords are never stored in plaintext.
- Only secure password hashes are stored in C5.
- Expired, invalid, or incorrectly signed tokens are rejected.
- Invalid credentials produce the same general login error to prevent disclosure of whether an account exists.
- If C5 is unavailable, authentication fails safely.
- Authentication tokens are never written to application logs.

### 3.4 C4 – Data Ingestion

**Purpose:** C4 receives operational CSV files, validates their structure and contents, and transfers valid records to C5.

**Supported data fields:**

- Date
- Department
- Admissions
- Discharges
- Occupied beds
- Bed capacity
- Staff on shift

**Data objects:**

| Object | Attributes | Persistence |
|---|---|---|
| ImportBatch | import_batch_id, uploader_id, filename, status, created_at | Persistent only if supported by the C5 schema or another approved mechanism. |
| ValidatedRecord | observation_date, department, admissions, discharges, occupied_beds, bed_capacity, staff_on_shift | Temporary before insertion into C5. |
| ValidationError | row_number, field_name, reason | Temporary validation object. |
| ValidationReport | import_batch_id, rows_accepted, rows_rejected, errors | Returned to C2/C1; persistent storage only if specified in the implemented design. |

C4 must not introduce a second operational database or duplicate the persistent data model owned by C5.

**CSV validation rules:**

| Field | Validation Rule |
|---|---|
| date | Must be a valid date in YYYY-MM-DD format. |
| department | Must match an existing department. |
| admissions | Must be a nonnegative integer. |
| discharges | Must be a nonnegative integer. |
| occupied_beds | Must be a nonnegative integer. |
| bed_capacity | Must be a positive integer. |
| staff_on_shift | Must be a nonnegative integer. |
| Occupied beds and capacity | Occupied beds cannot exceed bed capacity. |
| CSV structure | All required column headers must be present. |

**Duplicate-record policy:**

- Duplicate department/date observations within the same uploaded file are not silently combined or double-counted.
- Conflicting rows are rejected and identified in the validation report.
- If an uploaded observation conflicts with an existing stored department/date record, the existing observation is preserved and the conflicting uploaded row is rejected.
- The validation report identifies the affected row and explains the conflict.

**Upload behavior:**

1. C4 receives an uploaded CSV file from C2.
2. C4 checks the file format and maximum permitted size.
3. C4 checks that all required column headers are present.
4. C4 parses the file into individual records.
5. Each row is checked for valid dates and department identifiers.
6. Numerical values are checked for valid formats and ranges.
7. Occupied beds are checked against bed capacity.
8. Valid and invalid rows are separated.
9. If required column headers are missing, the entire file is rejected.
10. If individual rows contain invalid values, those rows are rejected and listed in the validation report.
11. C4 submits valid records to C5 through I6 using a database transaction.
12. If a database constraint or connection failure occurs, C5 rolls back the transaction.
13. C4 marks the import as failed and does not report the batch as successfully committed.
14. If the transaction succeeds, C5 commits the valid records.
15. C4 generates a validation report with accepted-row count, rejected-row count, and validation errors.
16. After a successful import, C4 sends a one-way forecast trigger to C6 through I10.
17. C4 returns the import result and validation report to C2.

A forecasting failure does not undo a successful database import.

### 3.5 C5 – Operations Database

**Purpose:** C5 provides persistent relational storage for operational observations, user accounts, forecast results, and planning information.

The seven entities established in D1 are:

| Entity | Key Attributes | Purpose |
|---|---|---|
| Department | department_id (PK), department_code, department_name, active | Identifies hospital departments. |
| DailyObservation | observation_id (PK), department_id (FK), observation_date, admissions, discharges, occupied_beds, bed_capacity, staff_on_shift, import_batch_id | Stores daily aggregated operational information. |
| ForecastRun | run_id (UUID PK), scope, horizon_days, generated_at, status, model_version, data_through_date | Records forecasting operations and their status. |
| ForecastValue | forecast_value_id (PK), run_id (FK), department_id (FK), target_date, predicted_admissions, predicted_occupied_beds | Stores predicted values by department, date, and run. |
| PlanningSetting | setting_id (PK), department_id (FK), capacity_threshold_pct, patients_per_staff, updated_at | Stores department-level planning assumptions. |
| StaffingEstimate | estimate_id (PK), run_id (FK), department_id (FK), target_date, required_staff, available_staff, staffing_gap | Stores staffing calculations. |
| PlanningFlag | flag_id (PK), run_id (FK), department_id (FK), target_date, flag_type, severity, threshold_used, message | Stores capacity and staffing warnings. |

**Relationships:**

- A Department has many DailyObservation records.
- A Department has many ForecastValue records.
- A ForecastRun can produce multiple ForecastValue records.
- A ForecastRun can produce multiple StaffingEstimate records.
- A ForecastRun can produce multiple PlanningFlag records.
- Each PlanningSetting belongs to one Department.
- D1 specifies at most one current PlanningSetting per department.

The database does not include a patient-level entity.

**Database integrity:**

- Primary keys uniquely identify records.
- Foreign keys maintain relationships between records.
- Unique constraints prevent duplicate department/date observations.
- Database transactions protect CSV imports from partial commits.
- Database constraints reject invalid observations, including occupied-bed counts exceeding bed capacity.

### 3.6 C6 – Forecasting Service

**Purpose:** C6 generates admissions and occupied-bed forecasts using historical operational observations.

**Forecast inputs:**

- Historical observation date.
- Department.
- Admissions.
- Discharges.
- Occupied beds.
- Bed capacity.
- Staff on shift, where required by the forecasting/planning workflow.

D1 establishes that the system requires at least 60 days of valid historical observations for the requested scope.

**Forecast behavior:**

1. C6 receives a forecast request from C2 through I11 or a one-way trigger from C4 through I10.
2. C6 identifies the requested scope and forecast horizon.
3. C6 retrieves the required historical data from C5.
4. C6 validates that at least 60 days of valid historical observations are available.
5. C6 creates or updates the ForecastRun record.
6. C6 transitions the run from QUEUED to RUNNING.
7. C6 generates admissions and occupied-bed predictions.
8. C6 stores successful forecast values in C5.
9. C6 marks the run SUCCESS.
10. C6 makes successful forecast results available to C7 and C2.
11. If processing fails, C6 marks the run FAILED and records the failure.

**Forecast state machine:**

`QUEUED → RUNNING → SUCCESS`

or

`QUEUED → RUNNING → FAILED`

Only a successful run publishes forecast values. A failed run must not replace the most recent successful forecast.

**Forecast request behavior:**

- The primary forecast horizon is seven days.
- D2 specifies supported request values from one through seven days.
- Fewer than 60 valid historical days means no forecast is generated for that scope.
- Matching requests for the same department scope and forecast horizon must reuse an existing run identifier if a matching run is already QUEUED or RUNNING.
- A subsequent request or successful import may initiate a new run with a unique run identifier.

### 3.7 C7 – Planning and Alerts

**Purpose:** C7 evaluates forecast results and generates capacity flags and staffing estimates.

**Inputs:**

- Forecast values from C6.
- Department capacity settings.
- Department patients-per-staff settings.
- Available staff counts.
- Department information.

**Responsibilities:**

- Compare predicted occupancy against the configured capacity threshold.
- Generate capacity flags.
- Calculate required staff using the configured department staffing assumption.
- Compare required staff with available staff.
- Calculate staffing gaps.
- Store PlanningFlag and StaffingEstimate records in C5.
- Make planning results available to C2.

**Configuration rules:**

- The default capacity threshold is 90% when a valid stored threshold is unavailable.
- Department-specific staffing ratios are configuration values.
- The system must not invent a staffing ratio when the required configuration is missing.
- If required staffing configuration is missing, C7 marks the staffing estimate as unavailable.
- The dashboard displays a configuration warning for the affected department.

**Notification behavior:**

Notifications are displayed inside the CareFlow dashboard. They are generated from PlanningFlag records stored in C5.

Each notification identifies:

- Affected department.
- Date.
- Flag type.
- Severity.
- Relevant planning information.

Notifications are informational decision-support messages. They do not automatically modify staffing assignments or bed allocations.

## 4. Supporting Functionality

### 4.1 Authentication and Authorization

C3 performs authentication and C2 enforces authorization. All protected operations require a valid authenticated identity and an appropriate role.

The team-approved working role-permission matrix is defined in Section 3.3. C2 must enforce these permissions on the server.

### 4.2 Notifications

Notifications are derived from PlanningFlag records generated by C7 and stored in C5. C1 maintains temporary notification display state.

If planning information cannot be retrieved, C1 displays an error and retains previously retrieved information when possible, indicating that it may be outdated.

### 4.3 Configuration Management

Planning thresholds are stored in the PlanningSetting entity in C5. Application and deployment settings are maintained through environment configuration.

The following configuration values are defined in D2:

| Setting | Value or Rule |
|---|---|
| Forecast horizon | Seven days by default; supported values from one through seven days. |
| Minimum historical data | 60 valid days. |
| Maximum CSV size | 10 MB. |
| JWT expiration | 60 minutes. |
| Default capacity threshold | 90%. |
| Staffing ratios | Department-specific configuration; no invented default. |

Invalid configuration values are rejected. The last valid value may be retained only when doing so is safe and consistent with the affected operation.

### 4.4 Logging and Monitoring

The initial implementation uses application-level structured logging and does not introduce a separate operational database for logs.

**Log objects:**

| Object | Attributes |
|---|---|
| LogEvent | timestamp, severity, component, event_type, request_id, message |
| ErrorEvent | timestamp, component, error_code, request_id, recoverable |
| AuditEvent | timestamp, user_id, action, resource_id, outcome |

Important operations and failures are logged, including:

- Authentication outcomes.
- CSV import results.
- Validation failures.
- Forecast requests.
- Database failures.
- API errors.

Passwords, plaintext credentials, authentication tokens, and patient-identifiable information must be excluded from logs.

Logging is an internal supporting function. It does not introduce a new numbered D0 interface or a separate independently deployed microservice.

## 5. Interface Specifications

The numbered interfaces I1–I13 are established in D0 and elaborated in D1/D2. Interface identifiers must remain consistent across the design documents.

| Interface | Connection | Input | Output | Format / Protocol | Error Behavior |
|---|---|---|---|---|---|
| I1 | User ↔ C1 | Login information, department selection, date filters, file selection | Dashboard pages, charts, tables, warnings, validation results | Browser interface over HTTPS | C1 displays accessible input and API errors. |
| I2 | C1 ↔ C2 | API requests, authorization token, filters, upload requests | JSON responses, forecasts, operational summaries, error messages | REST over HTTPS | 400 for invalid parameters, 401 for authentication failure, 403 for authorization failure, 500/503 for server/dependency failure. |
| I3 | C2 ↔ C3 | Email/password for login; JWT for protected requests | Access token, user ID, role, authorization result | In-process Python objects/dictionary | Invalid credentials or tokens result in authentication errors; C2 returns 401 or 403. |
| I4 | External file source E1 → C1 | User-selected operational CSV | File-selection result | Browser file interface; UTF-8 CSV | C1 rejects unsupported file types and oversized files. |
| I5 | C2 ↔ C4 | File bytes and uploader ID | Accepted/rejected row counts, validation errors, import batch ID | In-process Python objects/dictionary | Missing required columns reject the whole file; invalid rows are identified and rejected while valid rows may continue. |
| I6 | C4 → C5 | Validated operational records and import metadata | Database insert result and transaction outcome | SQL rows over PostgreSQL protocol/TCP | Constraint or connection failure rolls back the transaction and marks the batch failed. |
| I7 | C2 ↔ C5 | Read queries with scope/date range; planning-setting updates | Occupancy, forecasts, staffing estimates, flags, settings | SQL rows over database connection | Query over two seconds or connection error returns 503 to C1. |
| I8 | C6 ↔ C5 | Historical rows for the last 365 days | Forecast rows containing run ID, scope, target date, predicted admissions, predicted occupied beds, generated time, and model name | SQL rows over database connection | Fewer than 60 valid days means no forecast for that scope. A write failure marks the run failed and preserves the previous successful forecast. |
| I9 | C7 ↔ C5 | Forecast rows, department capacity threshold, patients-per-staff settings, and staff-on-shift information | Capacity/staffing flags and staffing-estimate rows | SQL rows over database connection | Missing settings use the 90% capacity default where applicable; a missing staffing ratio must not be invented. Write failures are logged and retried according to the planning policy. |
| I10 | C4 → C6 | Import batch ID and affected department identifiers | One-way trigger; no direct response | In-process Python object/dictionary | Forecast failure does not undo the import. C6 manages the ForecastRun record and status. |
| I11 | C2 ↔ C6 | Scope and horizon_days | Run ID, status, and data errors | In-process Python object/dictionary | Missing or invalid data produces no forecast and a data-validation error. |
| I12 | C6 → C7 | Forecast run ID | Number of flags created | In-process Python object/dictionary | C7 failure does not invalidate forecast results; the error is logged and flags may be reevaluated later. |
| I13 | C3 ↔ C5 | User email lookup | User ID, password hash, and role | SQL query/row | Unknown email returns the same generic login error as an incorrect password. |

### 5.1 Interface Clarifications

**I5 – Upload Processing**

The validation report contains the import batch identifier, accepted-row count, rejected-row count, and row-level errors.

**I6 – Database Import**

Validated operational records are submitted through a database transaction. If insertion fails, the transaction is rolled back.

**I7 – Operations and Planning Queries**

D2 specifies that a database query exceeding two seconds or a database connection error returns HTTP 503 to C1 through C2.

**I8 – Forecast Data**

C6 retrieves historical records from C5 and stores forecast results. A successful run publishes forecast values. A failed run does not replace the previous successful forecast.

**I9 – Planning Data**

The 90% default applies only to the capacity threshold. It must not be used as a default staffing ratio.

**I10 – Import-Triggered Forecasting**

I10 is a one-way trigger. C4 sends the import batch identifier and affected department identifiers to C6 after a successful import commit. C6 creates and manages the ForecastRun record. C2 retrieves forecast status separately through the forecast-status endpoint.

**I11 – Forecast Requests**

C2 sends the requested scope and forecast horizon to C6. The response includes the run identifier, status, and any data errors.

## 6. REST API Specification

D2 defines the following versioned REST API endpoints under `/api/v1/`.

| Method | Endpoint | Purpose | Input | Successful Result |
|---|---|---|---|---|
| POST | `/api/v1/auth/login` | Authenticate a user. | Email and password JSON. | Access token, user ID, and role. |
| POST | `/api/v1/auth/logout` | End the current client session. | Current authenticated token. | Logout/session confirmation. |
| GET | `/api/v1/operations` | Retrieve current operational information. | Scope and date-range query parameters. | Operational summaries and records. |
| POST | `/api/v1/uploads` | Submit a CSV file for validation and import. | Multipart CSV file. | Import result and validation report. |
| GET | `/api/v1/uploads/{batch_id}` | Retrieve upload status and validation results. | Import batch UUID. | Upload status and validation report. |
| POST | `/api/v1/forecasts` | Request a new forecast. | Scope and horizon_days JSON. | HTTP 202, run ID, QUEUED status, and submitted timestamp. |
| GET | `/api/v1/forecasts/{run_id}` | Retrieve forecast status and results. | Forecast run UUID. | Run status and available forecast results. |
| GET | `/api/v1/planning` | Retrieve staffing estimates and planning flags. | Scope and date-range filters. | Staffing estimates and planning flags. |

### 6.1 Authentication Endpoint

**POST `/api/v1/auth/login`**

The endpoint receives email and password credentials. C3 retrieves the user account from C5 and verifies the submitted password against the stored password hash.

Successful authentication returns a signed JWT with a maximum lifetime of 60 minutes, the user ID, and the user's assigned role.

Invalid credentials return a generic authentication error.

### 6.2 Upload Endpoint

**POST `/api/v1/uploads`**

The endpoint accepts a CSV file submitted by an authorized Data Manager.

The file must:

- Be UTF-8 encoded.
- Contain all required column headers.
- Be no larger than 10 MB.
- Contain valid department/date observations.
- Follow the numerical validation rules defined in Section 3.4.

The endpoint returns an import batch identifier and validation results.

**GET `/api/v1/uploads/{batch_id}`**

The endpoint retrieves the status and validation results associated with an upload batch.

The implementation must retain or otherwise retrieve the corresponding batch status and report. The persistence mechanism must remain consistent with the C5/D1 database design.

### 6.3 Forecast Endpoint

**POST `/api/v1/forecasts`**

Example request:

```json
{
  "scope": "ICU",
  "horizon_days": 7
}
```

Example successful response:

```json
{
  "run_id": "example-run-id",
  "status": "QUEUED",
  "submitted_at": "2026-11-20T18:15:00Z"
}
```

The endpoint returns HTTP 202 Accepted when a valid forecast request is queued.

Forecast processing is asynchronous. The client retrieves status and available results through:

`GET /api/v1/forecasts/{run_id}`

The valid run states are:

- QUEUED
- RUNNING
- SUCCESS
- FAILED

If a matching forecast request for the same scope and horizon is already QUEUED or RUNNING, the system reuses the existing run identifier rather than creating a duplicate active run.

### 6.4 Standard API Error Response

Example:

```json
{
  "error_code": "INVALID_SCOPE",
  "message": "The requested department does not exist.",
  "request_id": "example-request-id"
}
```

The example values are illustrative and do not represent an actual system record.

### 6.5 HTTP Error Statuses

| Status | Meaning |
|---|---|
| 400 | Invalid request parameters. |
| 401 | Missing or invalid authentication. |
| 403 | User does not have permission. |
| 404 | Requested resource not found. |
| 413 | Uploaded file exceeds the maximum size. |
| 422 | Invalid or insufficient operational data. |
| 429 | Request rate limit exceeded, if rate limiting is enabled. |
| 500 | Unexpected internal server error. |
| 503 | Required service or database unavailable. |

### 6.6 Authorization Requirements

Protected endpoints require a valid authentication token and an authorized role.

C2 performs server-side authorization checks before forwarding requests to internal components.

The dashboard may hide unavailable actions, but interface visibility does not replace backend authorization.

The endpoint-to-role mapping follows the team-approved working D2 role-access matrix in Section 3.3.

## 7. Technology Stack

The following table records the technologies selected or named in the CareFlow design.

| Layer | Technology | Purpose and Justification |
|---|---|---|
| Frontend framework | React | Provides reusable dashboard components and interactive filters. |
| Frontend language | TypeScript | Provides typed frontend code and API interactions. |
| Visualization | Plotly.js | Displays admissions, occupancy, and department comparisons. |
| Backend language | Python | Supports the API, data processing, ingestion, and forecasting workflow. |
| Backend framework | FastAPI | Provides REST endpoints and request validation. |
| Authentication | Signed JWT | Supports token-based authentication with a 60-minute expiration. |
| Database | PostgreSQL | Provides relational storage, transactions, keys, and constraints. |
| ORM/data access | SQLAlchemy | Provides structured Python database access. |
| Schema migrations | Alembic | Supports repeatable database schema changes. |
| Data processing | pandas and NumPy | Supports CSV parsing, cleaning, and numerical processing. |
| Forecasting | scikit-learn and XGBoost | Supports forecasting-model development and evaluation. |
| Request validation | Pydantic | Supports typed request and data validation. |
| Containerization | Docker | Provides a consistent application environment. |
| CI/CD | GitHub Actions | Supports automated checks and deployment workflows. |
| Hosting | Microsoft Azure for Students | Provides the initial student-budget hosting environment. |

### 7.1 Technology Selection Rationale

The modular monolithic backend is appropriate for the initial project because it reduces deployment complexity, infrastructure costs, and configuration overhead.

React and TypeScript support the interactive dashboard. FastAPI and Python allow the backend, data-processing, and forecasting functions to share a primary language.

PostgreSQL provides relational integrity and transactional behavior. Docker provides a consistent application environment, while Azure for Students supports deployment within the project's available budget.

The design names these technologies but the supplied repository ZIP did not contain dependency manifests or lockfiles. Therefore, exact package versions must be copied from the actual implementation manifests when they are available. No package versions are invented in this specification.

## 8. Constraints and Technical Consequences

| Constraint ID | Constraint | Technical Consequence |
|---|---|---|
| CON-01 | Limited project funding and Azure for Students credits; use free/open-source tools and the student Azure environment. | Use small deployment tiers, local model training, and free/open-source packages. Avoid paid GPU training and premium always-on services. |
| CON-02 | Restricted real hospital data requires appropriate training, institutional approval, and a data-use agreement. | Use synthetic data unless the required approvals are obtained. |
| CON-03 | Initial data is synthetic and aggregated by department/day without patient identifiers. | Keep the CSV and database schema aggregate-only. Do not introduce patient-level records. |
| CON-04 | Browser/API communication must use HTTPS, and protected operations require authentication and role-based access. | Enforce HTTPS, signed JWT validation, and server-side role checks. |
| CON-05 | Database credentials must remain in GitHub Actions secrets, and the database firewall must allow only the backend address. | Keep secrets outside source control and restrict database ingress. Private networking and a managed key vault were considered too costly for the project budget. |
| CON-06 | Forecasts are estimates that must be compared with a baseline, and staffing alerts require human review. | Present estimates with appropriate context. Do not automate clinical decisions, bed assignments, or staffing changes. |

## 9. Edge Cases and Error Handling

The following edge cases are inherited from D2. They must be considered during implementation and testing.

| ID | Component | Condition | Expected Handling |
|---|---|---|---|
| EC-01 | C1 | User selects an invalid date range. | C1 displays a correction message before submitting the request. |
| EC-02 | C1 | User repeatedly submits forecast requests. | C1 disables duplicate submission while a request is pending. |
| EC-03 | C1 | User selects an unsupported file type. | C1 rejects the file and displays an explanation. |
| EC-04 | C1 | Backend API does not respond. | C1 preserves existing displayed data where possible, displays a connection error, and offers retry. |
| EC-05 | C2 | Forecast horizon exceeds seven days. | C2 rejects the request with HTTP 400. |
| EC-06 | C2 | Multiple identical forecast requests arrive simultaneously. | C2 returns the existing run ID if a matching request is already QUEUED or RUNNING. |
| EC-07 | C2 | Department code does not exist. | C2 returns a standardized validation error. |
| EC-08 | C2 | PostgreSQL becomes unavailable. | C2 returns HTTP 503 and logs the request identifier. |
| EC-09 | C3 | JWT has expired. | C3 rejects the token and requires the user to authenticate again. |
| EC-10 | C3 | Multiple login requests occur simultaneously. | C3 verifies each request independently. |
| EC-11 | C3 | Email or password field is missing. | C3 rejects the request without attempting password verification. |
| EC-12 | C3 | User database is unavailable. | C3 fails closed and does not grant access. |
| EC-13 | C4 | Uploaded CSV exceeds 10 MB. | C4 rejects the upload and requests a smaller file. |
| EC-14 | C4 | Two data files are uploaded simultaneously. | Each upload receives a unique batch identifier and uses its own transaction. |
| EC-15 | C4/C6 | Required CSV headers are missing. | C4 rejects the entire file. |
| EC-16 | C4 | Database fails during record insertion. | C5 rolls back the transaction and C4 marks the import failed. |
| EC-17 | C5 | Occupied beds exceed bed capacity. | Database constraints reject the invalid observation. |
| EC-18 | C5 | Two uploads attempt to insert the same department/date observation. | Unique constraints and transaction handling prevent duplicate records. |
| EC-19 | C5 | Observation references a nonexistent department. | Foreign-key constraint rejects the record. |
| EC-20 | C5 | Database connection is unavailable. | Dependent components return an appropriate service-unavailable response. |
| EC-21 | C6 | Fewer than 60 valid historical days are available. | Forecast generation stops for the affected scope and returns a data error. |
| EC-22 | C6 | Multiple forecast runs overlap. | Runs are tracked by unique IDs and processed according to the documented execution policy. |
| EC-23 | C6 | Required historical features are missing. | Forecast generation stops and records the missing fields. |
| EC-24 | C6 | Forecast model or execution environment fails. | Run status becomes FAILED; previous successful forecast remains available. |
| EC-25 | C7 | Predicted occupancy reaches or exceeds 100%. | C7 generates a critical capacity flag. |
| EC-26 | C7 | Repeated forecast runs generate duplicate flags. | C7 applies deduplication using department, date, and flag type. |
| EC-27 | C7 | Required staffing settings are missing. | C7 does not invent a staffing ratio. The estimate is marked unavailable and the dashboard displays a configuration warning. |
| EC-28 | C7 | Database write for planning flags fails. | C7 logs the failure and retries evaluation during the next processing cycle. |
| EC-29 | Supporting function | Configuration contains an invalid threshold. | Configuration is rejected and the last valid value is retained where safe. |
| EC-30 | Supporting function | Multiple components write logs simultaneously. | Logging uses a thread-safe or process-safe mechanism. |
| EC-31 | Supporting function | A malformed logging event is generated. | The malformed event is rejected without interrupting normal application processing. |
| EC-32 | Supporting function | Logging destination becomes unavailable. | The system uses an available local fallback and surfaces critical monitoring failures. |

### 9.1 Import and Forecast Failure Separation

The CSV import and forecasting processes are separate operations.

- A missing required CSV header rejects the entire file.
- Invalid individual rows are reported and excluded from insertion.
- Valid rows are committed using a database transaction.
- A transaction failure causes rollback and prevents a partial import.
- After a successful commit, C4 triggers C6 through I10.
- A subsequent forecast failure does not undo the committed import.
- A failed forecast does not replace the previous successful forecast.

## 10. Requirements Traceability Matrix

This matrix maps each requirement and constraint in Requirements Document v1.0 to the corresponding design elements in D0, D1, or D2.

**Status definitions:**

- **Designed:** The corresponding behavior or design element is documented. This does not mean it has been implemented or tested.
- **In Progress:** Implementation or verification has begun but is not complete.
- **Planned:** The design or implementation work remains to be completed.
- **ORPHANED:** No supporting design element has been identified. An explanation and corrective action must be added.

The test case identifiers are proposed identifiers for the implementation test plan. They do not indicate completed testing.

| Req ID | Description | Design Component (D0/D1/D2) | Status | Test Case |
|---|---|---|---|---|
| REQ-01 | Authenticate users and enforce role-based access. | D0 I3/I13; D2 C2/C3, login flow, role-access matrix. | Designed | TC-01 |
| REQ-02 | Accept required UTF-8 CSV fields and enforce 10 MB maximum size. | D0 I4/I5; D2 C1/C2/C4, CSV validation rules. | Designed | TC-02 |
| REQ-03 | Return accepted/rejected counts and row-level validation errors. | D0 I5/I6; D2 C4 ValidationReport and upload workflow. | Designed | TC-03 |
| REQ-04 | Generate seven-day hospital-wide or department-level admissions and occupancy forecasts. | D0 I8/I10/I11; D1 C5/C6; D2 C2/C6. | Designed | TC-04 |
| REQ-05 | Reject forecasts when fewer than 60 valid historical days are available. | D0 I8/I11; D1 C6; D2 C6 and EC-21. | Designed | TC-05 |
| REQ-06 | Display occupancy and capacity flags using the 90% default threshold. | D0 I7/I9; D1 C5/C7; D2 C1/C7 and configuration rules. | Designed | TC-06 |
| REQ-07 | Calculate staffing estimates and staffing gaps using department configuration. | D0 I9/I12; D1 StaffingEstimate; D2 C7 and EC-27. | Designed | TC-07 |
| REQ-08 | Provide accessible chart alternatives, labeled controls, and accessible errors. | D0 I1; D2 C1 dashboard and accessibility behavior. | Designed | TC-08 |
| NFR-01 | Return stored operational information within 3 seconds under the defined workload. | D0 I2/I7; D1 C5; D2 C2 and I7 error behavior. | Designed | TC-09 |
| NFR-02 | Complete a seven-day forecast within 120 seconds under the defined workload. | D0 I8/I10/I11; D1 C6; D2 C6 forecast lifecycle. | Designed | TC-10 |
| NFR-03 | Return CSV validation report within 30 seconds for the defined sample workload. | D0 I5/I6; D2 C4 validation pipeline. | Designed | TC-11 |
| NFR-04 | Enforce HTTPS, signed JWT expiry, and server-side role authorization. | D0 I2/I3/I13; D2 C2/C3 and authentication flow. | Designed | TC-12 |
| NFR-05 | Provide table equivalents for all charts and keyboard access to primary tasks. | D0 I1; D2 C1 dashboard and accessibility behavior. | Designed | TC-13 |
| NFR-06 | Preserve the previous successful forecast during defined forecast failures. | D0 I8/I10/I12; D1 ForecastRun; D2 C6 and EC-24. | Designed | TC-14 |
| NFR-07 | Use relational constraints and transaction handling to preserve data integrity. | D1 C5 ERD; D2 C4/C5, I6, EC-16 to EC-20. | Designed | TC-15 |
| NFR-08 | Exclude patient-identifiable information from the initial implementation. | D0 data-flow constraints; D1 C5; D2 C4/C5. | Designed | TC-16 |
| NFR-09 | Support containerized deployment in the selected Azure environment. | D0 architecture rationale; Assignment 8 plan; technology stack. | Planned | TC-17 |
| CON-01 | Limited student budget and free/open-source technology requirement. | D0 architecture rationale; Assignment 8 implementation plan. | Designed | TC-18 |
| CON-02 | Restricted real data requires approval and a data-use agreement. | Week 3 Constraints Essay; D0 data-source boundary; D2 scope. | Designed | TC-19 |
| CON-03 | Synthetic aggregated data only; no patient identifiers. | D0 data flow; D1 C5; D2 C4/C5. | Designed | TC-20 |
| CON-04 | HTTPS and backend authentication/role authorization. | D0 I2/I3/I13; D2 C2/C3. | Designed | TC-12 |
| CON-05 | Secrets outside source control and database ingress restricted to backend. | Week 3 Constraints Essay; D0 deployment boundary; Assignment 8 plan. | Planned | TC-21 |
| CON-06 | Forecasts and staffing alerts are estimates requiring human review. | D1 C6/C7; D2 C1/C7 and scope boundaries. | Designed | TC-22 |

### 10.1 Relationship to D2 Requirement Identifiers

D2 uses the identifiers FR-01 through FR-05 for its five original functional requirements and NFR-01 through NFR-09 for its non-functional requirements.

This Assignment 9 requirements baseline uses REQ-01 through REQ-08 for the expanded functional requirements and NFR-01 through NFR-09 for the non-functional requirements. The expanded requirements preserve the original D2 user goals while separating detailed behaviors into independently verifiable requirements.

The original D2 functional requirement mapping is:

| Original D2 Requirement | Assignment 9 Requirement |
|---|---|
| FR-01 – Seven-day admissions and bed-occupancy forecasts | REQ-04 |
| FR-02 – Monitor current and predicted bed occupancy by department | REQ-06 |
| FR-03 – Estimate staffing requirements and identify possible shortages | REQ-07 |
| FR-04 – Upload and validate operational CSV files | REQ-02, REQ-03 |
| FR-05 – Accessible operational reports and forecast information | REQ-08 |

The NFR identifiers in the Assignment 9 requirements baseline are independently defined and must not be confused with D2's original NFR descriptions. The descriptions in Requirements Document v1.0 are the authoritative definitions for this matrix.

### 10.2 Orphaned Requirements Review

No requirement is intentionally marked ORPHANED in this draft because D0, D1, and D2 provide corresponding design elements for each listed requirement.

If implementation or team review identifies a requirement without an adequate design element:

1. Mark its Design Component cell as ORPHANED.
2. Explain the missing design decision in this section.
3. Assign an owner and target date.
4. Identify the design document that must be updated.
5. Do not claim the requirement is fully designed until the missing element is addressed.

### 10.3 Proposed Test Case Descriptions

| Test ID | Test Description |
|---|---|
| TC-01 | Test valid and invalid login, JWT verification, token expiration, and allowed/denied role access. |
| TC-02 | Test required CSV headers, UTF-8 format, a file at the 10 MB limit, and a file exceeding the limit. |
| TC-03 | Test missing headers, invalid dates, negative values, occupied beds exceeding capacity, duplicate department/date records, and validation-report contents. |
| TC-04 | Generate seven-day admissions and occupancy forecasts for hospital-wide and individual-department scopes. |
| TC-05 | Submit a forecast request with fewer than 60 valid historical days and verify that no new successful forecast is published. |
| TC-06 | Test predicted occupancy below, equal to, and above the 90% capacity threshold. |
| TC-07 | Calculate staffing estimates using configured patients-per-staff values and known available-staff counts. Also test missing staffing configuration. |
| TC-08 | Verify chart data-table alternatives, labeled controls, accessible errors, and keyboard navigation. |
| TC-09 | Time operational queries under the three-department, one-year workload. |
| TC-10 | Time forecast execution under the three-department, one-year workload. |
| TC-11 | Time validation of the planned 90-day, three-department CSV sample. |
| TC-12 | Test HTTPS, missing/invalid/expired JWTs, 60-minute expiration, and server-side role authorization. |
| TC-13 | Perform keyboard-only walkthroughs and inspect every chart for an equivalent data table. |
| TC-14 | Simulate forecast-processing and forecast-write failures. Verify FAILED state and continued availability of the previous successful forecast. |
| TC-15 | Test primary keys, foreign keys, unique constraints, invalid observations, and transaction rollback. |
| TC-16 | Inspect CSV files, database schema, and test data for patient-identifiable information. |
| TC-17 | Deploy the application using Docker in the selected Azure for Students environment and record resource consumption. |
| TC-18 | Review selected technologies and hosting resources against the student budget and free/open-source constraint. |
| TC-19 | Verify that no restricted real hospital dataset is used without required approval and a data-use agreement. |
| TC-20 | Inspect the CSV contract, database schema, and generated test data for patient names, dates of birth, medical record numbers, and other patient identifiers. |
| TC-21 | Inspect repository contents and history for committed credentials. Verify that deployment secrets are configured outside source control and database ingress is restricted to the backend address. |
| TC-22 | Inspect dashboard wording and system behavior to verify that forecasts and alerts are presented as estimates requiring human review. |

## 11. Team and Advisor Review Record

**Requirements baseline:** Requirements Document v1.0  
**Technical Specification version:** 1.0  
**Team review status:** Approved  
**Advisor review status:** Pending

### 11.1 Team Review

All three listed CareFlow team members confirmed that they were comfortable with the proposed technical architecture, interfaces, role-access matrix, API behavior, and implementation decisions.

| Reviewer | Review Result | Date |
|---|---|---|
| Vaishnavi Koduri | Approved | November 27, 2026 |
| Nurik Najmiddinov | Approved | November 27, 2026 |
| Gunnar Heiert | Approved | November 27, 2026 |

### 11.2 Advisor Review


## 12. Conclusion

The Technical Specification defines the architecture and technical behavior of CareFlow across the seven system components, their numbered interfaces, the relational database, the CSV ingestion process, authentication and authorization, forecasting, planning, and error handling.

Together with D0, D1, D2, and Requirements Document v1.0, this specification provides the technical baseline for implementation and verification.

The team has approved the documented technical decisions as the working project baseline. Implementation, performance testing, accessibility verification, deployment validation, and advisor review remain separate activities and must be recorded according to their actual completion status.

---


