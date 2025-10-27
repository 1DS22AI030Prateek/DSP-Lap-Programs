# streamlit_app.py
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="GDPR vs DPDP Case Study", layout="wide")
st.title("🧾 Case Study: GDPR vs DPDP Act 2023")

# ---------- Header Section ----------
st.markdown("""
<div style='background-color:#003366; padding:15px; border-radius:10px'>
<h3 style='color:white; text-align:center;'>Understanding Data Protection Laws: A Comparative Study of GDPR (EU) and DPDP Act 2023 (India)</h3>
</div>
""", unsafe_allow_html=True)

st.markdown("")

# ---------- Comparative Chart ----------
st.subheader("⚖️ Comparative Chart: GDPR vs DPDP Act 2023")

data = {
    "Feature / Principle": [
        "Scope", "Personal Data Definition", "Consent", "Data Protection Officer (DPO)",
        "Data Subject Rights", "Data Breach Notification", "Penalties", 
        "Cross-Border Data Transfer", "Children’s Data", "Data Protection by Design & Default"
    ],
    "GDPR (EU, 2018)": [
        "Applies to all organizations processing data of EU residents, even outside EU.",
        "Covers all identifiable data (name, email, IP, etc.)",
        "Freely given, informed, specific, revocable consent.",
        "Mandatory for large-scale or sensitive data processing.",
        "Access, rectification, erasure, portability, objection, restriction.",
        "Notify within 72 hrs; inform individuals if high risk.",
        "Up to €20M or 4% of global turnover.",
        "Allowed under adequacy or standard clauses.",
        "Parental consent below age 16.",
        "Mandatory by design and default."
    ],
    "DPDP Act 2023 (India)": [
        "Covers entities handling data of Indian residents globally.",
        "Includes sensitive data (health, finance, biometric).",
        "Explicit, free, informed, revocable consent required.",
        "Mandatory for designated entities; ensures DPDP compliance.",
        "Access, correction, erasure, grievance redressal.",
        "Promptly notify DPA and individuals.",
        "Up to ₹250 crore or 5% of turnover; strict penalties.",
        "Allowed under DPA or government rules.",
        "Consent below age 18 mandatory.",
        "Focus on AI/ML transparency and privacy."
    ]
}
df = pd.DataFrame(data)
st.dataframe(df, use_container_width=True, height=380)

# ---------- DPO Section ----------
st.subheader("🧑‍💼 Role of Data Protection Officer (DPO)")

dpo_data = {
    "Responsibility": [
        "Compliance Oversight", "Point of Contact", 
        "Risk Assessment & Mitigation", "Training & Awareness", "Reporting"
    ],
    "GDPR Role": [
        "Ensures GDPR compliance and monitoring.",
        "Acts as contact between company & EU authorities.",
        "Conducts DPIAs and risk audits.",
        "Educates employees on data protection.",
        "Reports breaches to regulators."
    ],
    "DPDP Act Role": [
        "Ensures adherence to DPDP principles.",
        "Liaises with Data Protection Authority & citizens.",
        "Assesses risks; ensures minimal data processing.",
        "Trains teams on DPDP, AI ethics, privacy.",
        "Reports non-compliance to DPA promptly."
    ]
}
st.dataframe(pd.DataFrame(dpo_data), use_container_width=True, height=250)

# ---------- Incident Report Section ----------
st.subheader("📋 Generate Mock Data Incident Report")

st.markdown("""
<div style='background-color:#f0f8ff; padding:10px; border-left:5px solid #003366; border-radius:5px'>
Fill out the details below to simulate how an organization would report a data breach or incident under GDPR / DPDP compliance.
</div>
""", unsafe_allow_html=True)

with st.form("incident_form"):
    c1, c2 = st.columns(2)
    with c1:
        org_name = st.text_input("🏢 Organization Name")
        dpo_name = st.text_input("👤 DPO / Responsible Person")
        incident_type = st.selectbox("⚠️ Type of Incident", ["Data Breach", "Unauthorized Access", "Data Loss", "Leak", "Other"])
        incident_datetime = st.date_input("📅 Date of Incident", datetime.today())
        affected_data = st.text_area("📂 Categories of Personal Data Affected")
    with c2:
        affected_count = st.number_input("👥 Individuals Affected", min_value=1, value=1)
        cause = st.text_area("🔍 Cause of Incident")
        actions_taken = st.text_area("🚑 Immediate Actions Taken")
        risk_level = st.selectbox("🔥 Risk Level", ["Low", "Medium", "High"])
        impact = st.text_area("📈 Potential Impact")

    st.markdown("---")
    c3, c4 = st.columns(2)
    with c3:
        notified_authority = st.selectbox("📢 Regulatory Authority Notified?", ["Yes", "No"])
        notified_individuals = st.selectbox("📞 Affected Individuals Notified?", ["Yes", "No"])
    with c4:
        preventive_measures = st.text_area("🛡️ Preventive Measures Taken")
        closure_date = st.date_input("✅ Incident Resolved Date", datetime.today())
        lessons_learned = st.text_area("📘 Lessons Learned / Recommendations")

    submitted = st.form_submit_button("🧾 Generate Report")

if submitted:
    st.success("✅ Incident Report Generated Successfully!")
    st.download_button(
        label="📥 Download Report",
        data=f"""
        INCIDENT REPORT
        --------------------------
        Organization: {org_name}
        DPO: {dpo_name}
        Incident Type: {incident_type}
        Date of Incident: {incident_datetime}

        Affected Data: {affected_data}
        Individuals Affected: {affected_count}

        Cause: {cause}
        Immediate Actions: {actions_taken}
        Risk Level: {risk_level}
        Potential Impact: {impact}

        Authority Notified: {notified_authority}
        Individuals Notified: {notified_individuals}

        Preventive Measures: {preventive_measures}
        Date Resolved: {closure_date}
        Lessons Learned: {lessons_learned}
        """,
        file_name="incident_report.txt",
        mime="text/plain"
    )
