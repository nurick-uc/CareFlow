# CareFlow: Hospital Operations and Resource Planning Platform


**Team Members:**
- Vaishnavi Koduri
- Nurik Najmiddinov

# 1. Stakeholder Map

CareFlow is designed to help hospitals forecast patient demand, monitor bed occupancy, estimate staffing requirements, and support hospital resource planning.

The project considers people who directly use the system, people who support its operation, and people whose needs might otherwise be overlooked.

### Primary Stakeholders

**1. Hospital Administrator**

Main Need: Predict hospital demand and plan hospital resources before capacity problems occur.

**2. Bed Manager**

Main Need: Monitor bed availability and anticipate capacity problems across hospital departments.

**3. Charge Nurse**

Main Need: Identify possible staffing shortages and communicate resource requirements.

### Secondary Stakeholder

**4. Hospital Data Manager**

Main Need: Provide accurate and properly formatted operational data for generating forecasts and reports.

### Hidden Stakeholder

**5. Hospital Staff Member Using a Screen Reader**

Main Need: Access operational reports and forecasts using assistive technology.

# 2. User Stories

## US-01: Forecast Hospital Demand

**Stakeholder Category:** Primary, Hospital Administrator

As a hospital administrator, I want to view predicted hospital admissions and bed occupancy for the upcoming seven days, so that I can prepare for changes in patient demand and plan hospital resources.

## US-02: Monitor Bed Availability

**Stakeholder Category:** Primary, Bed Manager

As a bed manager, I want to view current and predicted bed occupancy across hospital departments, so that I can identify departments approaching capacity and prepare for possible bed shortages.

## US-03: Estimate Staffing Requirements

**Stakeholder Category:** Primary, Charge Nurse

As a charge nurse, I want to compare estimated staffing requirements with available staffing levels in my department, so that I can identify possible staffing shortages and inform the appropriate personnel.

## US-04: Provide Operational Data

**Stakeholder Category:** Secondary, Hospital Data Manager

As a hospital data manager, I want to upload and validate hospital operational data, so that CareFlow uses accurate information when generating forecasts and reports.

## US-05: Access Information Using Assistive Technology

**Stakeholder Category:** Hidden, Hospital Staff Member Using a Screen Reader

As a hospital staff member who uses a screen reader, I want to access operational reports and forecast information with properly labeled content and accessible navigation, so that I can independently understand and use the same important information available to other staff members.

# 3. Use Cases

## UC-01: Generate Hospital Demand Forecast

**Related User Story:** US-01, Forecast Hospital Demand

**Primary Actor:** Hospital Administrator

**Secondary Actors:** None identified for the initial version of this use case.

### Preconditions

1. The administrator has a registered CareFlow account and is logged in.
2. The administrator has permission to access hospital forecasts.
3. Historical hospital operational data has been uploaded.
4. Required data fields are available and valid.
5. A forecasting model is available.

### Main Success Flow

1. **Administrator:** Requests a hospital-wide forecast for the next seven days.
2. **System:** Checks the administrator's permissions and retrieves the required historical operational data.
3. **Administrator:** Confirms the forecast request after the system verifies that the required data is available and valid.
4. **System:** Processes the data, generates predictions for hospital admissions and bed occupancy for the next seven days, and displays the predicted values, forecast dates, and generation time.
5. **Administrator:** Reviews the predictions to identify possible changes in hospital demand and plan resources.

### Alternate Flow: Department-Specific Forecast

1. Administrator requests a forecast for a specific hospital department instead of the entire hospital.
2. System retrieves historical operational data for the selected department.
3. System validates the department's data.
4. System generates admission and bed occupancy predictions for the next seven days.
5. System displays the department-specific forecast with the forecast dates and generation time.
6. Administrator reviews the results.

### Exception Flow: Missing or Invalid Data

1. Administrator requests a seven-day hospital demand forecast.
2. System checks the required historical operational data.
3. System detects missing required fields or invalid data values.
4. System stops the forecasting process.
5. System displays an error identifying the missing or invalid information.
6. Administrator reviews the error and is informed that the data must be corrected before another forecast can be generated.

### Postconditions

**Successful Outcome:**

- A seven-day forecast is generated.
- Predicted hospital admissions and bed occupancy are displayed.
- The authorized administrator can review the results for resource planning.

**Unsuccessful Outcome:**

- No forecast is generated using invalid or insufficient data.
- The system displays an error explaining the data problem.
- The administrator is informed that the data must be corrected before trying again.

# 4. Given, When, and Then Acceptance Criteria

The following acceptance criteria correspond to UC-01. Each criterion describes an outcome that can be checked during testing.

## Main Success Flow

### AC-01.1: Hospital-Wide Forecast

**Given:** An authorized hospital administrator is logged in, valid historical operational data is available, and a forecasting model is ready.

**When:** The administrator requests a hospital-wide forecast for the next seven days.

**Then:** CareFlow generates and displays predicted hospital admissions and bed occupancy for seven consecutive days, including the forecast dates and generation time.

### AC-01.2: Department-Specific Forecast

**Given:** The administrator is logged in and valid historical operational data is available for a selected hospital department.

**When:** The administrator requests a seven-day forecast for that department.

**Then:** CareFlow displays predicted admissions and bed occupancy for the selected department for seven consecutive days, including the forecast dates.

## Exception Flow

### AC-01.3: Missing or Invalid Data

**Given:** The uploaded historical operational data is missing required fields or contains invalid values.

**When:** The administrator requests a hospital demand forecast.

**Then:** CareFlow does not generate a forecast and displays an error identifying the missing or invalid information that must be corrected.

# 5. INVEST Self-Check

INVEST is used to evaluate whether each user story is suitable for development and testing.

The six INVEST criteria are explained below.

**Independent:** The story describes a distinct stakeholder need.

**Negotiable:** The story describes a goal rather than requiring a specific design or implementation.

**Valuable:** The story provides a clear benefit to the stakeholder.

**Estimable:** The development team can understand the work well enough to estimate it.

**Small:** The story focuses on one main goal and can be completed as a manageable piece of work.

**Testable:** The story has an outcome that can be checked.

### US-01: Forecast Hospital Demand

- **Independent:** Yes. It addresses the administrator's need to predict hospital demand.
- **Negotiable:** Yes. It describes the desired outcome without requiring a specific design.
- **Valuable:** Yes. It helps administrators plan hospital resources.
- **Estimable:** Yes. The forecasting goal is clearly defined.
- **Small:** Yes. It focuses on generating a seven-day hospital demand forecast.
- **Testable:** Yes. The system's seven-day predictions can be checked.

### US-02: Monitor Bed Availability

- **Independent:** Yes. It addresses the bed manager's need to monitor capacity.
- **Negotiable:** Yes. It does not prescribe a specific interface or implementation.
- **Valuable:** Yes. It helps identify departments approaching capacity.
- **Estimable:** Yes. The monitoring goal is clearly defined.
- **Small:** Yes. It focuses on bed occupancy monitoring.
- **Testable:** Yes. Current and predicted occupancy information can be checked.

### US-03: Estimate Staffing Requirements

- **Independent:** Yes. It addresses the charge nurse's staffing needs.
- **Negotiable:** Yes. It describes the goal without requiring a specific design.
- **Valuable:** Yes. It helps identify possible staffing shortages.
- **Estimable:** Yes. Comparing staffing requirements with availability is clearly defined.
- **Small:** Yes. It focuses on identifying staffing gaps.
- **Testable:** Yes. Estimated and available staffing values can be compared.

### US-04: Provide Operational Data

- **Independent:** Yes. It addresses the data manager's responsibility for operational data.
- **Negotiable:** Yes. It describes the data management goal without prescribing a particular interface.
- **Valuable:** Yes. It helps ensure that forecasts use accurate information.
- **Estimable:** Yes. Uploading and validating operational data are defined tasks.
- **Small:** Yes. It focuses on providing and validating data.
- **Testable:** Yes. Data uploads and validation results can be checked.

### US-05: Access Information Using Assistive Technology

- **Independent:** Yes. It addresses the accessibility needs of staff members using screen readers.
- **Negotiable:** Yes. It describes an accessibility goal without requiring a specific implementation.
- **Valuable:** Yes. It allows staff members to independently access important information.
- **Estimable:** Yes. Accessibility requirements can be identified and evaluated.
- **Small:** Yes. It focuses on accessing operational information.
- **Testable:** Yes. Screen-reader accessibility can be checked through testing.

### Overall INVEST Review

The five user stories represent different stakeholder needs and provide clear benefits. They avoid prescribing specific user interface designs and describe outcomes that can be evaluated.

Some stories may share underlying data and system services, but each represents a separate stakeholder goal. The team will review the INVEST evaluation again as stakeholder feedback and development work provide more information.

# 6. Requirements Elicitation Plan

The team plans to use multiple requirements elicitation techniques to understand stakeholder needs and make sure CareFlow addresses real hospital operational problems.

The goal is to understand how stakeholders currently perform their work, what challenges they face, and what information they need for resource planning.

The team will use stakeholder interviews, workflow observation, and an accessibility review.

## 6.1 Stakeholder Interviews

**Method:** Interviews

**Stakeholder Categories:**

- **Primary:** Hospital administrators, bed managers, and charge nurses.
- **Secondary:** Hospital data managers.
- **Hidden:** Hospital staff members who use screen readers or accessibility representatives.

**Purpose:**

The team plans to conduct short interviews with at least one representative from each stakeholder category. The interviews will focus on responsibilities, current workflows, operational challenges, and information needs.

### Interview Questions for Primary Stakeholders

1. How do you currently monitor hospital admissions and bed occupancy?
2. What challenges do you face when planning hospital resources?
3. How do you identify departments that may be approaching capacity?
4. How do you identify and communicate possible staffing shortages?
5. How far ahead do you usually plan for changes in patient demand?
6. What information would help you make better resource-planning decisions?

### Interview Questions for Secondary Stakeholders

1. How is hospital operational data currently collected and maintained?
2. What problems occur when preparing data for reports or analysis?
3. How do you identify missing, incomplete, or incorrect data?
4. What information is most important when preparing operational data?
5. What difficulties occur when data comes from different sources or formats?

### Interview Questions for Hidden Stakeholders

1. What difficulties do you experience when accessing digital reports using a screen reader?
2. Are charts, tables, or other visual information difficult to interpret?
3. What makes information easier to navigate using assistive technology?
4. What accessibility barriers should an operational planning platform avoid?
5. What information should be available in a format that screen readers can interpret?

The interviews will focus on existing workflows and problems rather than asking stakeholders to choose specific software features.

### Recording Interview Findings

For each interview, the team will record:

- Stakeholder role and category.
- Date of the conversation.
- Current workflow described by the stakeholder.
- Problems or difficulties identified.
- Important information needs.
- Requirements that may need to be added or changed.

The team will use the responses to review and improve the five user stories.

## 6.2 Workflow Observation

**Method:** Observation

**Stakeholders:**
- Hospital administrators
- Bed managers
- Charge nurses
- Hospital data managers

**Purpose:**

With appropriate permission, the team plans to observe or review documented hospital workflows to understand how operational tasks are currently completed.

The observation will focus on:

- How hospital staff monitor bed availability and occupancy.
- How changes in patient demand are identified.
- How staffing needs are estimated and communicated.
- How operational data is collected, organized, and checked.
- Where delays, repetitive tasks, or information gaps occur.

If direct observation is not possible, the team will review publicly available workflow documentation or information provided by stakeholders.

## 6.3 Accessibility Review

**Method:** Accessibility Review

**Stakeholders:**
- Hospital staff members who use screen readers.
- Accessibility representatives.

**Purpose:**

The team plans to review how people using assistive technology access operational reports and forecast information.

The review will focus on:

- Whether report information can be understood using a screen reader.
- Whether important information is available without relying only on visual elements.
- Whether headings, labels, and data tables can be interpreted by assistive technology.
- Whether users can access the same important operational information as other staff members.

This review will help the team identify accessibility needs that might otherwise be overlooked.

## 6.4 Recording and Using Stakeholder Feedback

The team will organize relevant findings from interviews, observations, and the accessibility review in a design notebook or in the repository's `docs/elicitation/` folder.

The notes will include:

- The stakeholder category and role.
- The current workflow described or observed.
- Problems and difficulties identified.
- Important information or needs mentioned by stakeholders.
- Possible changes to the existing user stories.

The team will compare the findings with the five user stories in this document. If stakeholder feedback identifies missing or unclear requirements, the team will revise the stories before moving further into design and development.

**Elicitation Status:** Stakeholder interviews, workflow observations, and accessibility reviews will be documented as they are completed. The team will use actual feedback to confirm or revise the requirements.

# 7. Scope and Assumptions

The following points define the intended scope of CareFlow for this project.

1. CareFlow focuses on hospital operations and resource planning, not patient diagnosis or treatment.
2. The initial system will use historical hospital operational data.
3. CSV files will be the initial data-import format.
4. Forecasts will cover the upcoming seven days.
5. Staffing estimates will use available staffing data and configurable planning assumptions.
6. The system will use aggregated operational information rather than patient-identifiable records.
7. The system will display the latest available data and will not assume real-time hospital integration.
8. Forecasts are estimates and are not guaranteed future outcomes.
9. CareFlow will support planning but will not automatically assign beds or change staff schedules.

# 8. Conclusion

These five user stories identify the needs of CareFlow's primary, secondary, and hidden stakeholders.

The use case explains how hospital administrators generate forecasts, including alternate and exception situations. The acceptance criteria provide observable outcomes that can be checked during testing.

The INVEST review helps evaluate whether the stories are suitable for development. The requirements elicitation plan describes how the team will gather stakeholder feedback through interviews, workflow observation, and accessibility reviews.

Together, these requirements will guide the team's design, development, and testing work in the upcoming weeks.
