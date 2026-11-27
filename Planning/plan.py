"""CareFlow Assignment 8 plan generator: one data source -> Tasklist.md, Plan.md, CSVs, Gantt PNG."""
import csv, datetime as dt
import numpy as np

D = dt.date
HOL = {D(2027, 1, 18)} | {D(2027, 3, 15) + dt.timedelta(i) for i in range(5)}  # MLK, spring break
N, V, G = "Nurik Najmiddinov", "Vaishnavi Koduri", "Gunnar Heiert"
SHORT = {N: "Nurik", V: "Vaish", G: "Gunnar"}
MEM = [N, V, G]
COL = {N: "#1F3A5F", V: "#0F8B8D", G: "#7B4FA0"}
BUF = 0.18

def bdays(start, n):
    """Return list of n business days from start, skipping weekends and holidays."""
    out, d = [], start
    while len(out) < n:
        if d.weekday() < 5 and d not in HOL:
            out.append(d)
        d += dt.timedelta(1)
    return out

# Milestones in the implementation semester (CS 5002). Each closes a two-week work window.
MS = [
    ("MS-A", D(2027, 1, 11), D(2027, 1, 22), "Data layer and API skeleton",
     "C5 Operations Database schema from the D1 ERD is migrated on PostgreSQL, and C2 Backend API runs with a health endpoint and an OpenAPI contract covering I2 and I7.",
     "Migration script runs on a clean database; OpenAPI file reviewed against D2 interface tables.", "Vaish reviews T1; Nurik reviews T3"),
    ("MS-B", D(2027, 1, 25), D(2027, 2, 5), "Secure login end to end",
     "A user signs in on C1 Web Dashboard, C3 Auth Module issues a 60-minute JWT, and a protected C2 endpoint returns 200 for an allowed role and 403 for a disallowed one.",
     "Live demo with one account per role; automated auth tests pass in CI.", "Dr. Yu Zhao (advisor meeting)"),
    ("MS-C", D(2027, 2, 8), D(2027, 2, 19), "Upload path and staging deployment",
     "A sample operations CSV goes C1 to C2 to C4 Data Ingestion to C5, and the validation report returns within 30 s. Every merge to main deploys automatically to an Azure staging environment.",
     "Timed upload of a 90-day sample file with three bad rows; GitHub Actions run history.", "Nurik (upload); Gunnar (pipeline)"),
    ("MS-D", D(2027, 2, 22), D(2027, 3, 5), "Synthetic dataset and alerts engine",
     "Two years of synthetic daily data for Emergency, Medical-Surgical, and ICU are loaded through C4, and C7 Planning & Alerts raises capacity and staffing flags from a test forecast.",
     "Data profile report; C7 unit tests with threshold cases at 89%, 90%, and 91%.", "Dr. Yu Zhao (mid-semester review)"),
    ("MS-E", D(2027, 3, 8), D(2027, 3, 26), "Feature-complete CareFlow",
     "C6 Forecasting Service produces a 7-day forecast within 2 minutes, and C1 shows forecasts, alerts, and upload history with a data-table alternative for every chart.",
     "End-to-end demo following UC-01 and UC-02 on the staging site.", "Both members; demo to Dr. Yu Zhao"),
    ("MS-F", D(2027, 3, 29), D(2027, 4, 9), "Verified system",
     "All I1 to I13 integration tests pass, the 3 s, 2 min, and 30 s timing budgets are met, and the selected model beats the baseline on MAE and WAPE.",
     "Test report and model evaluation report committed to the repository.", "Gunnar (tests); Nurik (model evaluation)"),
    ("MS-G", D(2027, 4, 12), D(2027, 4, 23), "Final release v1.0",
     "Release v1.0 is tagged and deployed, and the user guide, deployment guide, and final report are complete for the CS 5002 final presentation.",
     "Tagged release on GitHub; documents reviewed by both members and the advisor.", "Dr. Yu Zhao and Dr. Justin Zhan"),
]

# id, verb-first statement, module, owner, window (milestone id), O, M, P, support hours by the other member, deps
T = [
    ("T1", "Develop the C5 Operations Database schema, migrations, and seed accounts from the D1 ERD (7 entities, UUID run_id).", "C5 Operations Database", N, "MS-A", 8, 12, 20, 3, []),
    ("T3", "Develop the C2 Backend API skeleton, the OpenAPI contract for I2, and the database access layer for I7.", "C2 Backend API", V, "MS-A", 10, 16, 26, 3, []),
    ("T2", "Develop the C3 Auth Module: password hashing, 60-minute JWT issue and verification (I3), user lookup over I13, and role checks for the four roles.", "C3 Auth Module", G, "MS-B", 10, 14, 22, 3, ["T1", "T3"]),
    ("T5", "Develop the C1 Web Dashboard shell: sign-in page, navigation, department filter, and current-operations views over I1 and I2.", "C1 Web Dashboard", V, "MS-B", 12, 18, 28, 2, ["T3"]),
    ("T4", "Develop the C4 Data Ingestion upload path: header and row validation, transactional import into C5 (I5, I6), and the rejected-row validation report.", "C4 Data Ingestion", N, "MS-C", 12, 18, 30, 3, ["T1", "T3"]),
    ("T10", "Develop the deployment pipeline: Docker images for C1, C2, and C6, GitHub Actions CI, and an Azure staging environment.", "Microsoft Azure (deployment)", G, "MS-C", 10, 16, 28, 3, ["T3"]),
    ("T6", "Obtain and validate the Python-generated synthetic dataset for the three departments and build the feature set used by the C6 Forecasting Service.", "C6 Forecasting Service", N, "MS-D", 8, 12, 20, 2, ["T4"]),
    ("T8", "Develop the C7 Planning & Alerts rules that compare forecasts with capacity settings and staffing ratios and write flags to C5 (I9, I12).", "C7 Planning & Alerts", G, "MS-D", 10, 16, 24, 3, ["T1", "T3"]),
    ("T7", "Develop the C6 Forecasting Service: 7-day admission and bed occupancy models, the baseline, and the ForecastRun states QUEUED, RUNNING, SUCCESS, FAILED (I8, I10, I11).", "C6 Forecasting Service", N, "MS-E", 16, 24, 40, 3, ["T6"]),
    ("T9", "Develop the C1 Web Dashboard forecast, alert, and upload pages with Plotly charts, the 90% threshold line, and data-table alternatives.", "C1 Web Dashboard", V, "MS-E", 14, 20, 32, 3, ["T4", "T5", "T8"]),
    ("T15", "Develop the C1 Web Dashboard settings and administration pages: capacity thresholds, staffing ratios, and user role management for the admin role.", "C1 Web Dashboard", V, "MS-D", 10, 14, 22, 2, ["T3", "T5"]),
    ("T12", "Validate and refine the C6 Forecasting Service models against the baseline using MAE, RMSE, WAPE, and forecast bias.", "C6 Forecasting Service", N, "MS-F", 8, 12, 20, 2, ["T7"]),
    ("T11", "Test the integrated system: integration tests for I1 to I13, role-access tests, and timing tests for the 3 s, 2 min, and 30 s budgets.", "C1 to C7 (system)", G, "MS-F", 12, 18, 26, 5, ["T7", "T9", "T10"]),
    ("T13", "Document the user guide, deployment guide, and final design report, and update README.md and Design_Diagrams to match the built system.", "All modules (documentation)", G, "MS-G", 10, 14, 20, 5, ["T11", "T12"]),
    ("T14", "Refine C1 and C2 by fixing defects found in T11 and applying accessibility and usability fixes before release v1.0.", "C1 Web Dashboard, C2 Backend API", V, "MS-G", 8, 12, 20, 3, ["T11"]),
]
REV = {"T1": V, "T2": N, "T3": N, "T4": G, "T5": G, "T6": G, "T7": V, "T8": N, "T9": N, "T10": V, "T11": N, "T12": G, "T13": N, "T14": G, "T15": G}
CRIT = {"T1", "T4", "T6", "T7", "T11", "T13"}
ORDER = sorted(T, key=lambda t: int(t[0][1:]))
msd = {m[0]: m for m in MS}

rows = []
for tid, stmt, mod, own, w, o, m, p, sup, deps in ORDER:
    ms = msd[w]
    days = bdays(ms[1], 9)  # 9 working days in a window (8 in the MLK week)
    days = [d for d in days if d <= ms[2]]
    work = days[:-3]                         # planned work days
    buf_days = max(1, round(len(work) * BUF))  # 15-20% task buffer
    tb = days[len(work):len(work) + buf_days]
    pert = (o + 4 * m + p) / 6
    rows.append(dict(id=tid, stmt=stmt, mod=mod, own=own, ms=w, start=work[0], plan=work[-1], tbuf=tb, done=tb[-1],
                     prot=[d for d in bdays(tb[-1] + dt.timedelta(1), 5) if d <= ms[2]],
                     o=o, m=m, p=p, pert=pert, hrs=round(pert * (1 + BUF)), sup=sup, deps=deps, crit=tid in CRIT,
                     workn=len(work), bufn=len(tb)))
R = {r["id"]: r for r in rows}
hours = lambda r, m: r["hrs"] if r["own"] == m else (r["sup"] if REV[r["id"]] == m else 0)

f = lambda d: d.strftime("%b %d").replace(" 0", " ")
fy = lambda d: d.strftime("%a, %b %d, %Y").replace(" 0", " ")

# ---------- Tasklist.md
with open("Tasklist.md", "w") as fh:
    fh.write("# CareFlow Task List\n\nCS 5001/5002 Senior Design · Team: Nurik Najmiddinov, Vaishnavi Koduri, Gunnar Heiert\n\n"
             "Module names match Project-Description.md and Design D0 to D2. Full plan: [Planning/Plan.md](Planning/Plan.md).\n\n")
    for r in rows:
        fh.write(f"{r['id']}. {r['stmt']} Module: {r['mod']}. Owner: {SHORT[r['own']]}.\n\n")

# ---------- CSVs
with open("timeline.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["ID", "Statement", "Owner", "Start", "Planned finish", "Task buffer", "Completion", "Dependencies", "Critical path", "Milestone"])
    for r in rows:
        w.writerow([r["id"], r["stmt"], SHORT[r["own"]], r["start"], r["plan"], f"{r['tbuf'][0]} to {r['tbuf'][-1]}", r["done"],
                    " ".join(r["deps"]) or "-", "yes" if r["crit"] else "", r["ms"]])
with open("effort_matrix.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["ID", "O", "M", "P", "PERT", "Primary hours (+18%)", "Nurik", "Vaish", "Gunnar", "Row total", "Primary"])
    for r in rows:
        hh = [hours(r, m) for m in MEM]
        w.writerow([r["id"], r["o"], r["m"], r["p"], round(r["pert"], 1), r["hrs"], *hh, sum(hh), SHORT[r["own"]]])

# ---------- Gantt
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, matplotlib.dates as md
fig, ax = plt.subplots(figsize=(13, 6.6), dpi=170)
labels = []
for i, r in enumerate(rows[::-1]):
    y = i
    col = COL[r["own"]]
    ax.barh(y, (r["plan"] - r["start"]).days + 1, left=md.date2num(r["start"]), color=col, edgecolor="#C62828" if r["crit"] else col, linewidth=2 if r["crit"] else 0, height=0.6)
    ax.barh(y, (r["done"] - r["tbuf"][0]).days + 1, left=md.date2num(r["tbuf"][0]), color="#F2B84B", height=0.6)
    if r["prot"]:
        ax.barh(y, (r["prot"][-1] - r["prot"][0]).days + 1, left=md.date2num(r["prot"][0]), color="#D9D9D9", hatch="///", edgecolor="#999", height=0.6)
    labels.append(f"{r['id']} · {SHORT[r['own']]}{' ★' if r['crit'] else ''}")
ax.set_yticks(range(len(rows))); ax.set_yticklabels(labels, fontsize=9)
for m in MS:
    ax.axvline(md.date2num(m[2])+1, color="#C62828", lw=1, ls="--")
    ax.text(md.date2num(m[2])+1, len(rows) - 0.3, m[0], color="#C62828", fontsize=8.5, ha="center", fontweight="bold")
ax.axvspan(md.date2num(D(2027, 3, 13)), md.date2num(D(2027, 3, 21)), color="#EEEEEE")
ax.text(md.date2num(D(2027, 3, 17)), 0.4, "Spring\nbreak", ha="center", fontsize=8, color="#555")
ax.xaxis.set_major_locator(md.WeekdayLocator(byweekday=md.MO)); ax.xaxis.set_major_formatter(md.DateFormatter("%b %d"))
plt.setp(ax.get_xticklabels(), rotation=45, fontsize=8)
ax.set_xlim(md.date2num(D(2027, 1, 9)), md.date2num(D(2027, 4, 26)))
ax.set_ylim(-0.7, len(rows) + 0.2)
from matplotlib.patches import Patch
ax.legend(handles=[*[Patch(color=COL[m], label=f"{SHORT[m]} task") for m in MEM], Patch(color="#F2B84B", label="Task buffer (18%)"),
                   Patch(facecolor="#D9D9D9", hatch="///", edgecolor="#999", label="Protected milestone block"), Patch(facecolor="white", edgecolor="#C62828", linewidth=2, label="Critical path (★)")],
          loc="lower left", fontsize=8, ncol=6, bbox_to_anchor=(0, -0.22))
ax.set_title("CareFlow implementation timeline, Spring 2027 (CS 5002)", fontsize=12, fontweight="bold", loc="left")
ax.grid(axis="x", color="#EEE"); ax.set_axisbelow(True)
plt.tight_layout(); plt.savefig("Gantt.png")

# ---------- Plan.md
L = []
a = L.append
a("# CareFlow: Task List, Milestones, Timeline, and Effort Matrix\n")
a("**CS 5001 Senior Design I, Assignment 8** · University of Cincinnati  \n**Team:** Nurik Najmiddinov, Vaishnavi Koduri, Gunnar Heiert  \n**Advisor:** Dr. Yu Zhao · **Instructor:** Dr. Justin Zhan  \n**Project:** CareFlow, an AI-powered hospital operations and resource planning platform\n")
a("**Team.** Gunnar Heiert joined the team on November 17 at our advisor's request. Work is divided across all three members, five tasks each.\n")
a("**Planning assumptions.** Nurik and Vaish are on campus in Spring 2027 with no co-op rotation; Gunnar's spring availability is to be confirmed. Each member plans about 8 to 12 hours per week on the project. "
  "UC Spring 2027 runs January 11 to April 29, with Martin Luther King Jr. Day on January 18 and spring break March 15 to 21; final exams are the last week of April. "
  "No project tasks are scheduled during fall final exams, winter break (mid-December to January 10), or spring break. "
  "Each task's hours use the three-point estimate (O + 4M + P) / 6 plus an 18% buffer.\n")

a("## 1. Task List (Assignment #5)\n")
a("Fifteen tasks, five per member, each one to two weeks long. Module names match Project-Description.md and Design D0 to D2. The same list is in `Tasklist.md` at the repository root.\n")
for r in rows:
    a(f"**{r['id']}.** {r['stmt']} *Module: {r['mod']}.* **Owner: {SHORT[r['own']]}.**\n")

a("## 2. Milestones List (Assignment #6)\n")
a("### 2.1 Course deliverables, CS 5001\n")
a("Our team registered for the course partway through the semester, so assignments from A6 onward are being completed on a catch-up schedule. The Canvas due date and our planned completion date are both shown.\n")
a("| # | Deliverable | What it demonstrates | Canvas due | Completed / planned | Verified by | Status |\n|---|---|---|---|---|---|---|")
cd = [("A1", "Professional biography", "Each member's background and project interests", "Sep 2", "Complete", "Instructor", "**Complete**"),
      ("A2", "Team formation and project description", "CareFlow problem, solution, and scope defined", "Sep 9", "Complete", "Instructor", "**Complete**"),
      ("A3", "Advisor selection and design constraints essay", "Dr. Yu Zhao confirmed as advisor; design constraints analyzed", "Sep 18", "Complete", "Instructor; advisor approval", "**Complete**"),
      ("A4", "User stories and use cases", "US-01 to US-05 and UC-01, UC-02 with acceptance criteria", "Sep 28", "Complete", "Instructor", "**Complete**"),
      ("A5", "High-level system design (D0)", "Components C1 to C7 and interfaces I1 to I13", "Oct 2", "Complete", "Instructor; advisor", "**Complete**"),
      ("A6", "Detailed system design, part 1 (D1)", "ERD with 7 entities and 8 relationships", "Oct 8", "Complete", "Instructor; advisor", "**Complete**"),
      ("A7", "Detailed system design, part 2 (D2) and peer review notes", "Dashboard mockup, ingestion error flow, auth and role flow, ForecastRun state machine", "Oct 14", "Nov 25", "Instructor; peer team", "**Complete**"),
      ("A8", "Task list, milestones, timeline, and effort matrix", "Design turned into a plan with owners and dates (this document)", "Oct 28", "Nov 25", "Instructor; advisor", "**Complete**"),
      ("A9", "Requirements document and technical specification document", "Requirements traceable to C1 to C7 and testable", "Oct 30", "Nov 27", "Instructor; advisor", "Planned"),
      ("A10", "Test and validation plan draft", "Test cases for I1 to I13, timing budgets, and model metrics", "Nov 4", "Nov 29", "Instructor", "Planned"),
      ("A11", "Ethics and responsible-use statement", "Synthetic-data, privacy, and human-in-the-loop safeguards", "Nov 11", "Nov 30", "Instructor", "Planned"),
      ("A12", "Presentation draft and documented advisor feedback", "Advisor has reviewed the presentation and feedback is recorded", "Nov 18", "Dec 1", "Dr. Yu Zhao", "Planned"),
      ("A13", "Team oral presentation, recorded video, and peer reviews", "Team presents the CareFlow design and plan", "Nov 18", "Dec 3", "Instructor; peer teams", "Planned"),
      ("A14", "Design report, design notebook, and team and self assessment", "Complete CS 5001 design record; reproduces Tables 1 and 2", "Dec 2", "Dec 2", "Instructor; advisor", "Planned"),
      ("A15", "Project advisor assessments", "Advisor's assessment of team progress", "Nov 25", "Dec 2", "Dr. Yu Zhao", "Planned"),
      ("A16", "ABET teamwork survey", "Each member's assessment of team participation", "Dec 4", "Dec 4", "Instructor", "Planned")]
for x in cd:
    a("| " + " | ".join(x[:3]) + f" | {x[3]}, 2026 | " + (x[4] if x[4] == "Complete" else x[4] + ", 2026") + f" | {x[5]} | {x[6]} |")
a("")
a("### 2.2 Internal milestones, CS 5002 implementation (Spring 2027)\n")
a("Each milestone is a checkable outcome at the end of a two-week window (three weeks across spring break).\n")
a("| # | Milestone | What it demonstrates | Date | How it is verified | Verified by |\n|---|---|---|---|---|---|")
for m in MS:
    a(f"| {m[0]} | {m[3]} | {m[4]} | {fy(m[2])} | {m[5]} | {m[6]} |")
a("")

a("## 3. Table 1: Timeline (Assignment #6)\n")
a("Planned work runs from Start to Planned finish. The task buffer (18%, rounded to whole days) follows, and Completion is the committed date. "
  "A protected block of two to three working days before every milestone absorbs slippage on the critical path and is not assigned new work. ★ marks the critical path.\n")
a("| ID | Task | Owner | Start | Planned finish | Task buffer | Completion | Protected block | Depends on |\n|---|---|---|---|---|---|---|---|---|")
for m in MS:
    for r in [x for x in rows if x["ms"] == m[0]]:
        tb = f(r["tbuf"][0]) if r["bufn"] == 1 else f"{f(r['tbuf'][0])} to {f(r['tbuf'][-1])}"
        pr = f"{f(r['prot'][0])} to {f(r['prot'][-1])}" if r["prot"] else "-"
        a(f"| {r['id']}{' ★' if r['crit'] else ''} | {r['stmt']} | {SHORT[r['own']]} | {f(r['start'])} | {f(r['plan'])} | {tb} ({r['bufn']} d) | {f(r['done'])} | {pr} | {', '.join(r['deps']) or '-'} |")
    a(f"| **{m[0]}** | **Milestone: {m[3]}** | Both | | | | **{f(m[2])}** | | {', '.join(x['id'] for x in rows if x['ms'] == m[0])} |")
a("")
a("**Critical path:** T1 → T4 → T6 → T7 → T11 → T13 → MS-G. T7 (C6 Forecasting Service) is the longest and riskiest task, and its window spans spring break, so it gets the three-week MS-E window. "
  "If T7 slips past its protected block, T12 starts with the baseline model only (risk R1), and T11 tests against the baseline so testing is not blocked.\n")
a("![CareFlow Gantt chart](Gantt.png)\n")

a("## 4. Table 2: Effort Matrix (Assignment #6)\n")
a("Hours per task. The owner's hours are the three-point estimate plus 18% buffer; the designated reviewer's hours are code review, pairing, and integration support. "
  "**Bold** marks the one member of primary responsibility, who carries the largest share of every task.\n")
a("| ID | Module | O | M | P | (O+4M+P)/6 | Nurik | Vaish | Gunnar | Row total |\n|---|---|---|---|---|---|---|---|---|---|")
tot = {m: 0 for m in MEM}
for r in rows:
    cells = []
    for m in MEM:
        h = hours(r, m); tot[m] += h
        cells.append(f"**{h}**" if r["own"] == m else (str(h) if h else "-"))
    a(f"| {r['id']} | {r['mod']} | {r['o']} | {r['m']} | {r['p']} | {r['pert']:.1f} | " + " | ".join(cells) + f" | {sum(hours(r, m) for m in MEM)} |")
T_ = sum(tot.values())
a("| **Total** | | | | | | " + " | ".join(f"**{tot[m]}**" for m in MEM) + f" | **{T_}** |")
a("| **Share** | | | | | | " + " | ".join(f"**{100 * tot[m] / T_:.0f}%**" for m in MEM) + " | 100% |")
a("")
hi, lo = max(tot, key=tot.get), min(tot, key=tot.get)
diff = tot[hi] - tot[lo]
a(f"**Balance.** The largest and smallest columns ({SHORT[hi]} and {SHORT[lo]}) differ by {diff} hours, {100 * diff / (T_ / 3):.0f}% of an even share. "
  "Each task has one designated reviewer who carries its support hours. We compare logged hours against this table at every milestone. "
  "If one column runs more than 10% above an even share, the next unstarted reviewer role moves to the member with the fewest hours, and Tables 1 and 2 are updated in the repository. "
  "Gunnar joined after the design phase, so he reviews T4, T5, and T6 early on to learn the codebase before his own tasks.\n")
weeks = 15
a(f"Spread over the {weeks}-week semester, this is about " + ", ".join(f"{tot[m] / weeks:.0f} hours per week for {SHORT[m]}" for m in MEM) + ", leaving room for team meetings, advisor meetings, and CS 5002 course deliverables.\n")

a("## 5. Work Breakdown Structure\n")
phases = [("1 Foundation", "MS-A, MS-B", ["T1", "T3", "T2", "T5"]),
          ("2 Data path and infrastructure", "MS-C", ["T4", "T10"]),
          ("3 Data, planning logic, and settings", "MS-D", ["T6", "T8", "T15"]),
          ("4 Forecasting and full dashboard", "MS-E", ["T7", "T9"]),
          ("5 Verification", "MS-F", ["T12", "T11"]),
          ("6 Release", "MS-G", ["T13", "T14"])]
a("```\nCareFlow (CS 5002 implementation)")
for pi, (ph, ms, ids) in enumerate(phases):
    last = pi == len(phases) - 1
    a(f"{'└──' if last else '├──'} {ph}  [{ms}]")
    for j, t in enumerate(ids):
        r = R[t]
        a(f"{'    ' if last else '│   '}{'└──' if j == len(ids) - 1 else '├──'} {t}  {r['mod']}  ({SHORT[r['own']]})")
a("```\n")
a("Level 1 is the phase and level 2 is the Task List item. Every task appears once, with the same ID and owner as in Tables 1 and 2. CS 5001 course deliverables A1 to A16 are tracked as milestones in Section 2.1.\n")

a("## 6. Risk Register\n")
a("| # | Risk | Category | Likelihood | Impact | Strategy | Mitigation (where it shows in Table 1) | Owner | Trigger |\n|---|---|---|---|---|---|---|---|---|")
risks = [
    ("R1", "Forecast models do not beat the baseline on synthetic data", "Technical", "Medium", "High", "Reduce", "Baseline model is built first in T7, so a working forecast always exists; T12 is a dedicated refinement task; MS-E protected block", "Nurik", "Model MAE or WAPE not better than baseline at MS-E"),
    ("R2", "Uneven participation, or a member becomes unavailable (Gunnar joined after the design phase)", "Team", "Medium", "High", "Reduce", "Weekly team check-in; every task has a named reviewer who can take it over; 18% buffers and protected blocks; scope priority: C1 to C6 first, C7 staffing ratios can be simplified to capacity alerts only", "Nurik", "A task more than 2 working days past its Completion date, or a member misses two check-ins in a row"),
    ("R3", "C6 work interrupted by spring break and midterms", "Team", "Medium", "Medium", "Avoid", "No tasks scheduled March 15 to 21; T7 given a three-week window with a protected block before MS-E", "Nurik", "T7 less than half done on March 12"),
    ("R4", "Azure deployment problems or student credit limits", "External", "Medium", "Medium", "Reduce", "Deploy to staging early (T10 by MS-C) so issues surface six weeks before release; Docker Compose local deployment as fallback", "Gunnar", "Staging deploy failing for more than 3 days, or credits below 25%"),
    ("R5", "Interface mismatch between C1, C2, C4, and C6", "Technical", "Medium", "Medium", "Reduce", "OpenAPI contract fixed in T3 at MS-A; contract tests run in CI from MS-C", "Vaish", "CI contract tests failing after a merge"),
    ("R6", "No access to real hospital data", "External", "High", "Low", "Accept", "Project is designed on Python-generated synthetic data (T6); any real dataset is optional and decided with the advisor after MS-F", "Nurik", "Advisor requests real-data validation"),
    ("R7", "Advisor feedback delayed", "External", "Low", "Medium", "Reduce", "Advisor meetings booked for every milestone date in the first week of January", "Vaish", "No advisor response within 5 working days of a milestone"),
]
for x in risks:
    a("| " + " | ".join(x) + " |")
a("")
a("High-impact schedule risks R1, R2, and R3 are visible in Table 1 through the critical-path markers, the T7 three-week window, and the protected blocks before every milestone.\n")
a("## 7. Consistency check\n")
a("All 15 tasks appear in the Task List, the work breakdown structure, Table 1, and Table 2 with the same ID, module, and owner. Every task links to one milestone, and every milestone has a date and a verifier.\n")
open("Plan.md", "w").write("\n".join(L))
print({SHORT[m]: tot[m] for m in MEM})
