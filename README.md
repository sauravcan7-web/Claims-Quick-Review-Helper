To practice these skills hands-on, I built a small web tool called Claims Quick-Review Helper using Python and Streamlit. It lets me upload claim data (CSV), filter it, run basic analysis, flag high-risk cases, and generate a draft preliminary report preview.

The goal wasn’t to replace professional software — it was to simulate real trainee tasks and demonstrate initiative.

What the Tool Does (Core Features)
Upload & Quick Load Upload any claims CSV (or use a sample dataset). The tool handles common columns like incident date, claim type, amount, severity, and fraud flags.
Caseload Overview At a glance:

Total claims
Average claim amount
Fraud reported percentage
Average days open (with % overdue >60 days)
High-risk claims % (flagged based on large amount, severity, or fraud)
These metrics help prioritize — exactly what a trainee adjuster needs when managing delegated claims.

Claims by Type Visualization A clean bar chart shows the most frequent claim types (e.g., Collision, Property Damage, Liability). This helps spot patterns: “Many theft claims lately → prepare for common coverage questions.”

Risk Flagging & Top High-Value Claims Simple rules flag “High Risk” cases (e.g., top 20% amounts + major severity + fraud reported). Displays top 5 highest-value claims — useful for identifying potential large losses early.

Become a member
Filter & Preliminary Report Preview Filter by type/severity → select a claim → get a formatted preview:

Policy number, date, type, amount
Risk flag
Trainee-style notes: liability thoughts, quantum estimate, recommended actions (e.g., “Recommend surveyor if high risk”), communication tips.
Export for Sharing Download filtered data as CSV — ready to share with seniors or use in reports.

Tech Behind It (Kept Simple)
Python + Pandas: For data loading, filtering, calculations, and risk logic.
Streamlit: Turns the script into an interactive web app in minutes — no frontend skills needed.
Through self-study and hands-on simulation, I have developed a solid foundational understanding of the loss adjusting process, including receipt and acknowledgment of new claim instructions, timely coordination and investigation of losses, on-site assessments, liability determination under policy wording, quantum estimation (including damage valuation and business interruption elements), reserve setting, interim payment calculations, expert instruction (surveyors, forensic engineers, lawyers), fraud indicator recognition, subrogation potential, negotiation and settlement of claims, and preparation of structured preliminary, interim, and final reports. I am familiar with core industry concepts such as policy exclusions, proximate cause, betterment, salvage, contribution, average, and indemnity principles, as well as the importance of maintaining professional communication with insureds, brokers, insurers, and reinsurers to achieve fair, accurate, and timely resolutions.

What I Learned About Loss Adjusting
Building this reinforced key trainee responsibilities:

Acknowledging and triaging new claims quickly
Assessing liability, quantum, and risks early
Recommending experts or escalation
Preparing clear, structured reports
Communicating professionally with insureds/brokers
