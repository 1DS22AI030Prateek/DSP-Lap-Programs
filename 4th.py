import streamlit as st
import re

# ---------------- Vulnerability Rules ----------------
VULNERABILITY_RULES = {
    "Use of eval()": r"\beval\(",
    "Use of exec()": r"\bexec\(",
    "Hardcoded password": r"password\s*=\s*[\"'].*[\"']",
    "SQL Injection risk": r"(SELECT|INSERT|UPDATE|DELETE).*\+.*",
    "Command injection risk": r"(os\.system|subprocess\.Popen|os\.popen)\(",
    "Insecure function (C)": r"\bgets\(",
}

# ---------------- Scan Function ----------------
def scan_code(code):
    results = []
    lines = code.splitlines()
    for i, line in enumerate(lines, start=1):
        for vuln, pattern in VULNERABILITY_RULES.items():
            if re.search(pattern, line):
                results.append({"Line": i, "Vulnerability": vuln, "Code": line.strip()})
    return results

# ---------------- Streamlit UI ----------------
st.set_page_config(page_title="Vulnerability Analyzer", page_icon="🛡️", layout="wide")

st.markdown("<h1 style='text-align:center; color:#D32F2F;'>🛡️ Vulnerability Analyzer Tool</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Scan your code files for common security vulnerabilities and bad coding patterns.</p>", unsafe_allow_html=True)
st.markdown("---")

# --- Upload file or paste code ---
option = st.radio("Input method:", ["Upload File", "Paste Code"], key="input_method_radio")

code_text = ""
if option == "Upload File":
    uploaded_file = st.file_uploader("Upload a source code file", type=["py","java","c","cpp","js"], key="file_upload")
    if uploaded_file is not None:
        code_text = uploaded_file.read().decode("utf-8")
        st.code(code_text, language="")
else:
    code_text = st.text_area("Paste your source code here:", key="code_text_area")

# --- Scan Button ---
if st.button("🔍 Scan Code for Vulnerabilities", key="scan_button"):
    if code_text.strip() == "":
        st.warning("⚠️ Please provide code to scan.")
    else:
        results = scan_code(code_text)
        if results:
            st.subheader("⚠️ Vulnerabilities Detected")
            st.table(results)
        else:
            st.success("✅ No obvious vulnerabilities detected!")
