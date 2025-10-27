import hashlib
import base64
import streamlit as st

# ---------------- Hash Functions ----------------
def compute_hash(text, algo="sha256"):
    h = hashlib.new(algo)
    h.update(text.encode())
    return h.hexdigest()

def compute_file_hash(file, algo="sha256"):
    h = hashlib.new(algo)
    while chunk := file.read(4096):
        h.update(chunk)
    return h.hexdigest()

# ---------------- Normal Function ----------------
def normal_function(x):
    return x * x

# ---------------- Obfuscated Function ----------------
def obfuscated_function(x):
    code = """
def hidden_logic(n):
    return n * n
result = hidden_logic(x)
"""
    encoded = base64.b64encode(code.encode()).decode()
    decoded = base64.b64decode(encoded).decode()
    local_vars = {"x": x}
    exec(decoded, {}, local_vars)
    return local_vars["result"]

# ---------------- Streamlit UI ----------------
st.set_page_config(page_title="Hash & Obfuscation Lab", page_icon="🛡️", layout="centered")

st.markdown("<h1 style='text-align:center; color:#FF5722;'>🛡️ Hashing & Obfuscation Lab Demo</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Explore how hashing secures data and how obfuscation hides logic.</p>", unsafe_allow_html=True)
st.markdown("---")

# Tabs for navigation
tab1, tab2 = st.tabs(["🔑 Hash Functions", "🎭 Obfuscation"])

# -------- Hash Functions Tab --------
with tab1:
    st.subheader("Hash Generator")
    option = st.radio("Select Input Type:", ["Text", "File"])

    algo = st.selectbox("Choose Algorithm:", ["md5", "sha1", "sha256", "sha512"])

    if option == "Text":
        text = st.text_area("Enter text here:")
        if st.button("Compute Text Hash"):
            if text:
                st.markdown("### ✅ Hash Result")
                st.code(compute_hash(text, algo), language="bash")

    else:
        uploaded = st.file_uploader("Upload a file:")
        if uploaded and st.button("Compute File Hash"):
            uploaded.seek(0)
            st.markdown("### ✅ File Hash Result")
            st.code(compute_file_hash(uploaded, algo), language="bash")

# -------- Obfuscation Tab --------
with tab2:
    st.subheader("Function Obfuscation")
    st.markdown("Here we compare **normal** and **obfuscated** functions that compute the square of a number.")

    col1, col2 = st.columns(2)

    # Normal Function input & run
    with col1:
        normal_x = st.number_input("Enter a number for Normal Function:", value=4, key="normal_input")
        if st.button("Run Normal Function"):
            st.success(f"Normal Function Output: {normal_function(normal_x)}")

    # Obfuscated Function input & run
    with col2:
        obf_x = st.number_input("Enter a number for Obfuscated Function:", value=4, key="obf_input")
        if st.button("Run Obfuscated Function"):
            st.warning(f"Obfuscated Function Output: {obfuscated_function(obf_x)}")

st.markdown("---")
st.caption("⚡ Developed for Data Security & Privacy Lab")
