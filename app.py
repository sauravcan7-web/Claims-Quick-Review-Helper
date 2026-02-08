import streamlit as st
import pandas as pd
import os

# Page setup
st.set_page_config(page_title="Claims Quick-Review Helper", layout="wide")

st.title("Claims Quick-Review Helper")
st.markdown("""
**Trainee Loss Adjuster Tool**  
Simple helper I created to practice key tasks:  
• Upload and quickly review new claim batches  
• Spot high-risk or delayed claims  
• Prepare preliminary report notes  
• Export summaries for seniors / team  
""")

# ──────────────────────────────
# Upload or fallback to sample
# ──────────────────────────────
st.subheader("Upload Claims Data (CSV)")
uploaded = st.file_uploader("Upload your claims file", type="csv")

if uploaded is not None:
    df = pd.read_csv(uploaded)
    st.success(f"Loaded {len(df)} claims from uploaded file.")
else:
    local_path = os.path.join("data", "claims_data.csv")
    if os.path.exists(local_path):
        df = pd.read_csv(local_path)
        st.info(f"Using sample data: {len(df)} claims")
    else:
        df = None
        st.warning("No data available. Please upload a CSV file.")

if df is not None:
    # ──────────────────────────────
    # Date parsing (with dayfirst=True to avoid warning)
    # ──────────────────────────────
    date_column = None
    for col in ['incident_date', 'loss_date', 'date_of_loss', 'claim_date', 'policy_bind_date']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], dayfirst=True, errors='coerce')
            date_column = col
            break

    if date_column:
        df['days_open'] = (pd.Timestamp.now() - df[date_column]).dt.days.clip(lower=0)

    # ──────────────────────────────
    # Quick Overview Metrics
    # ──────────────────────────────
    st.subheader("Quick Caseload Overview")

    cols = st.columns(4)
    cols[0].metric("Total Claims", len(df))
    cols[1].metric("Avg Claim Amount", f"${df.get('total_claim_amount', pd.Series(0)).mean():,.0f}" if 'total_claim_amount' in df.columns else "N/A")

    fraud_pct = (df.get('fraud_reported', pd.Series('N')).eq('Y').mean() * 100)
    cols[2].metric("Fraud Reported %", f"{fraud_pct:.1f}%")

    if date_column:
        avg_days = df['days_open'].mean()
        old_pct = (df['days_open'] > 60).mean() * 100
        cols[3].metric("Avg Days Open", f"{avg_days:.1f}")
        st.caption(f"{old_pct:.1f}% claims open >60 days – may need priority follow-up")

    # Risk flagging
    severity_col = next((c for c in ['incident_severity', 'severity'] if c in df.columns), None)
    df['risk_flag'] = 'Low'

    conditions = []
    if 'total_claim_amount' in df.columns:
        conditions.append(df['total_claim_amount'] > df['total_claim_amount'].quantile(0.8))
    if severity_col:
        conditions.append(df[severity_col].isin(['Major', 'Total Loss', 'High', 'Severe']))
    if 'fraud_reported' in df.columns:
        conditions.append(df['fraud_reported'] == 'Y')

    if conditions:
        df.loc[pd.concat(conditions, axis=1).any(axis=1), 'risk_flag'] = 'High'

    high_risk_pct = (df['risk_flag'] == 'High').mean() * 100
    st.metric("High Risk Claims %", f"{high_risk_pct:.1f}%")

    # Top 5 high value claims
    if 'total_claim_amount' in df.columns:
        st.markdown("**Top 5 Highest Value Claims**")
        top5 = df.nlargest(5, 'total_claim_amount')[
            ['policy_number', 'total_claim_amount', 'risk_flag', severity_col or 'N/A', date_column or 'N/A']
        ]
        st.dataframe(top5, hide_index=True)

    # ──────────────────────────────
    # Clean chart: Claims by Type
    # ──────────────────────────────
    type_col = next((c for c in ['incident_type', 'claim_type', 'type_of_loss'] if c in df.columns), None)
    if type_col:
        st.subheader("Claims by Type")
        type_counts = df[type_col].value_counts().sort_values(ascending=False)
        st.bar_chart(
            type_counts,
            x_label="Claim / Incident Type",
            y_label="Number of Claims",
            color="#1f77b4"
        )
        st.caption("Helps identify the most frequent claim types – useful for preparing similar cases.")
    else:
        st.info("No claim type column found (e.g. 'incident_type'). Chart skipped.")

    # ──────────────────────────────
    # Filters
    # ──────────────────────────────
    st.subheader("Filter Claims")
    c1, c2 = st.columns(2)
    sel_type = 'All'
    sel_sev = 'All'

    with c1:
        if type_col:
            types = ['All'] + sorted(df[type_col].dropna().unique().tolist())
            sel_type = st.selectbox("Claim Type", types)

    with c2:
        if severity_col:
            sevs = ['All'] + sorted(df[severity_col].dropna().unique().tolist())
            sel_sev = st.selectbox("Severity", sevs)

    filtered = df.copy()
    if type_col and sel_type != 'All':
        filtered = filtered[filtered[type_col] == sel_type]
    if severity_col and sel_sev != 'All':
        filtered = filtered[filtered[severity_col] == sel_sev]

    st.dataframe(filtered.head(60), use_container_width=True)

    # ──────────────────────────────
    # Safe claim selection + report preview
    # ──────────────────────────────
    st.subheader("Select Claim → Preliminary Report Preview")
    if not filtered.empty:
        filtered_reset = filtered.reset_index(drop=True)
        labels = []
        for i, row in filtered_reset.iterrows():
            amt = row.get('total_claim_amount', 0)
            date_str = row.get(date_column, pd.NaT).strftime('%Y-%m-%d') if pd.notna(row.get(date_column)) else 'N/A'
            label = f"Pol: {row.get('policy_number','N/A')} | {date_str} | ${amt:,.0f} | {row['risk_flag']}"
            labels.append(label)

        selected_label = st.selectbox("Choose claim", labels)
        if selected_label:
            idx = labels.index(selected_label)
            row = filtered_reset.loc[idx]

            st.markdown("### Preliminary Report Preview (Trainee Draft)")
            st.write(f"**Policy Number:** {row.get('policy_number', 'N/A')}")
            st.write(f"**Date of Loss:** {row.get(date_column, 'N/A')}")
            st.write(f"**Type:** {row.get(type_col, 'N/A')}")
            st.write(f"**Severity:** {row.get(severity_col, 'N/A')}")
            st.write(f"**Claim Amount:** ${row.get('total_claim_amount', 0):,.0f}")
            st.write(f"**Risk Flag:** {row['risk_flag']}")

            st.markdown("**Trainee Adjuster Notes:**")
            st.write("• Liability: Appears covered – confirm policy wording and exclusions.")
            st.write("• Quantum: Reported amount as initial estimate – may adjust after investigation.")
            st.write("• Recommended Actions:")
            if row['risk_flag'] == 'High':
                st.write("  - Recommend surveyor or expert inspection")
                st.write("  - Escalate to senior adjuster / potential fraud review")
            else:
                st.write("  - Proceed with standard documentation and claimant contact")
            st.write("• Communication: Update insured / broker promptly to manage expectations.")

    # ──────────────────────────────
    # Export
    # ──────────────────────────────
    st.subheader("Export Filtered Data")
    csv = filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download as CSV",
        data=csv,
        file_name="filtered_claims_report.csv",
        mime="text/csv"
    )
