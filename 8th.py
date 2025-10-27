# Install required libraries if not installed
# pip install streamlit cryptography pyjwt

import streamlit as st
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
import jwt
import datetime

# ---------------- RSA Digital Signature ----------------
def generate_keys():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    return private_key, public_key

def sign_message(private_key, message):
    signature = private_key.sign(
        message.encode(),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

def verify_signature(public_key, message, signature):
    try:
        public_key.verify(
            signature,
            message.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except:
        return False

# ---------------- Authentication & JWT ----------------
SECRET_KEY = "my_super_secret_key"  # For JWT tokens

# Example "database" of users
USERS_DB = {
    "virat": "virat123",
    "kohli": "kohli123"
}

def authenticate(username, password):
    if username in USERS_DB and USERS_DB[username] == password:
        token = jwt.encode({"user": username, "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=10)}, SECRET_KEY, algorithm="HS256")
        return token
    else:
        return None

def verify_token(token):
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return True, data["user"]
    except:
        return False, None

# ---------------- Streamlit UI ----------------
st.set_page_config(page_title="Digital Signatures & Auth Lab", page_icon="🔐")

st.markdown("<h1 style='text-align:center; color:#4CAF50;'>🔐 Digital Signatures & Auth Demo</h1>", unsafe_allow_html=True)
st.markdown("---")

# ---------------- Tabs ----------------
tab1, tab2 = st.tabs(["🖊 Digital Signature", "🔑 Authentication & Authorization"])

# -------- Digital Signature Tab --------
with tab1:
    st.subheader("RSA Digital Signature")
    
    message = st.text_area("Enter a message (e.g., transaction details):", value="Payment of $100 to Bob")
    
    if st.button("Generate Keys & Sign Message"):
        private_key, public_key = generate_keys()
        signature = sign_message(private_key, message)
        st.success("✅ Message signed successfully!")
        st.code(signature.hex(), language="bash")
        
        # Verify signature
        verified = verify_signature(public_key, message, signature)
        st.write(f"Signature Verified: {'✅ Valid' if verified else '❌ Invalid'}")
        
        # Show public key (simulating sharing for verification)
        pem = public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)
        st.text_area("Public Key (share with recipient to verify signature):", pem.decode())

# -------- Authentication & Authorization Tab --------
with tab2:
    st.subheader("Login & Token-based Authentication")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        token = authenticate(username, password)
        if token:
            st.success(f"✅ Login successful! JWT Token issued:\n{token}")
            
            # Simulate secure API call
            if st.button("Simulate Secure API Call"):
                valid, user = verify_token(token)
                if valid:
                    st.info(f"API Access Granted for user: {user}")
                else:
                    st.error("❌ Invalid or expired token")
        else:
            st.error("❌ Invalid credentials")

st.markdown("---")
st.caption("Case Study: Digital signatures in e-commerce/banking secure transactions and prevent tampering.")
