import re
import pandas as pd
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# ---------------- Feature Extraction ----------------
def extract_features(url):
    return {
        "url_length": len(url),
        "has_at": 1 if "@" in url else 0,
        "has_https": 1 if url.startswith("https") else 0,
        "num_digits": sum(c.isdigit() for c in url),
        "num_hyphen": url.count("-"),
        "num_subdir": url.count("/")
    }

# ---------------- Load or Create Dataset ----------------
# Example dataset (replace with your CSV if available)
data = {
    "url": [
        "https://www.google.com",
        "http://phishing-site.com/login@secure",
        "https://secure-bank.com/account",
        "http://fake-update.com/install",
        "https://amazon.com/payment",
        "http://paypal.verify-account.com"
    ],
    "label": [0, 1, 0, 1, 0, 1]  # 0 = legitimate, 1 = phishing
}
df = pd.DataFrame(data)

# Extract features for dataset
feature_df = pd.DataFrame([extract_features(u) for u in df["url"]])
X = feature_df
y = df["label"]

# ---------------- Train/Test Split ----------------
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# ---------------- Model Training ----------------
model = LogisticRegression()
model.fit(X_train, y_train)

# ---------------- Evaluate ----------------
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))

# ---------------- Streamlit UI ----------------
st.title("🔐 Phishing Website Detection")
st.write("Enter a URL to check if it's phishing or legitimate.")

# ---- Single URL Input ----
user_url = st.text_input("Enter URL here:")

if st.button("Check URL"):
    if user_url.strip() == "":
        st.warning("⚠️ Please enter a valid URL.")
    else:
        features = pd.DataFrame([extract_features(user_url)])
        prediction = model.predict(features)[0]
        result = "⚠️ Phishing Website" if prediction == 1 else "✅ Legitimate Website"
        st.subheader(result)

# ---- Batch URL Upload ----
st.write("---")
st.subheader("📂 Upload a file with multiple URLs (CSV or TXT)")

uploaded_file = st.file_uploader("Upload file", type=["csv", "txt"])

if uploaded_file is not None:
    try:
        # Read file
        if uploaded_file.name.endswith(".csv"):
            url_df = pd.read_csv(uploaded_file)
            urls = url_df.iloc[:, 0].tolist()  # Take first column as URLs
        else:  # TXT file
            urls = uploaded_file.read().decode("utf-8").splitlines()

        # Extract features & predict
        batch_features = pd.DataFrame([extract_features(u) for u in urls])
        batch_preds = model.predict(batch_features)

        # Results table
        results = pd.DataFrame({
            "URL": urls,
            "Prediction": ["⚠️ Phishing" if p == 1 else "✅ Legitimate" for p in batch_preds]
        })

        st.subheader("📊 Results Table")
        st.dataframe(results)

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
