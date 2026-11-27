# CareFlow

**AI-Powered Hospital Operations and Resource Planning Platform**

CS5001 / CS5002 Senior Design, University of Cincinnati (2026–2027)

## Team

| Name | Major | Role |
|---|---|---|
| Nurik Najmiddinov | Computer Science | Coordinator, Documentation Owner |
| Vaishnavi Koduri | Computer Science | Lead Developer / Architect, QA / Test Owner |
| Gunnar Heiert | Computer Science | Testing and DevOps |

**Advisor:** Dr. Yu Zhao, Department of Computer Science  
**Instructor:** Dr. Justin Zhan

## About

CareFlow is a web application that helps hospital administrators see current operations (admissions, discharges, bed occupancy, staffing) and uses machine learning to forecast admissions and bed occupancy for the next seven days, flagging possible capacity and staffing shortages. It is an operational planning tool only; it does not make clinical or patient-level decisions. The initial implementation uses synthetic, aggregated operational data.

See [Project-Description.md](Project-Description.md) for details.

## Repository Contents

| File | Description |
|---|---|
| [Project-Description.md](Project-Description.md) | Project overview, components, and planned technology |
| [Team_Contract.md](Team_Contract.md) | Team contract (roles, communication, meetings, decisions, conflict plan) |
| [Constraints_Essay.md](Constraints_Essay.md) | Assignment 3: design constraints essay |
| [User_Stories.md](User_Stories.md) | Assignment 4: stakeholders, user stories, use cases, acceptance criteria |
| [Design_Diagrams/](Design_Diagrams/) | Assignments 5–7: design documents and diagrams (see below) |
| [Tasklist.md](Tasklist.md) | Assignment 8: task list with one owner per task |
| [Planning/](Planning/) | Assignment 8: milestones, timeline, effort matrix, risk register, Gantt chart |
| [Bio_Nurik_Najmiddinov.md](Bio_Nurik_Najmiddinov.md) | Professional biography: Nurik Najmiddinov |
| [Bio_Vaish_Koduri.md](Bio_Vaish_Koduri.md) | Professional biography: Vaishnavi Koduri |
| Bio_Gunnar_Heiert.md | Professional biography: Gunnar Heiert (to be added) |

### Design_Diagrams

| Design | Files |
|---|---|
| D0: high-level design (Assignment 5) | `D0_High_Level_Design` (.md, .pdf), `D0_Block_Diagram`, `D0_Data_Flow` (.drawio + .png) |
| D1: detailed design, part 1 (Assignment 6) | `D1_Detailed_Design` (.docx, .pdf), `D1_ERD` (.drawio, .png, .pdf) |
| D2: detailed design, part 2 (Assignment 7) | `Figure1_System_Architecture`, `Figure2_Dashboard_Mockup`, `Figure3_Authentication_RBAC_Flow`, `Figure4_CSV_Ingestion_Error_Flow`, `Figure5_ForecastRun_State_Machine`, `Figure6_Component_Interaction_Data_Ownership` (.png + .drawio; dashboard as .html); `D2_Detailed_Design` and `Peer_Review_Notes.md` (to be added) |

### Planning

| File | Description |
|---|---|
| [Plan.md](Planning/Plan.md) | Task list, milestones, timeline (Table 1), effort matrix (Table 2), work breakdown structure, risk register |
| [Gantt.png](Planning/Gantt.png) | Spring 2027 implementation timeline |
| [timeline.csv](Planning/timeline.csv), [effort_matrix.csv](Planning/effort_matrix.csv) | Tables 1 and 2 as data |
| [plan.py](Planning/plan.py) | Script that generates the planning files from one data source |

## Planned Technology

React + TypeScript · Python + FastAPI · PostgreSQL · scikit-learn / XGBoost · Plotly · Docker · Microsoft Azure · GitHub Actions
