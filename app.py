import streamlit as st
import os
from openai import OpenAI

# ---- Page Config ----
st.set_page_config(page_title="Service Desk AI Portal", page_icon="🤖", layout="wide")

# ---- OpenAI Client ----
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---- Styles ----
st.markdown("""
<style>
.hero {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
    padding: 32px;
    border-radius: 20px;
    margin-bottom: 24px;
}
.card {
    background: #f7f9fc;
    padding: 20px;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0 8px 20px rgba(0,0,0,0.05);
    transition: transform .2s ease;
}
.card:hover {
    transform: translateY(-4px);
}
.issue-btn {
    margin: 6px 0;
}
</style>
""", unsafe_allow_html=True)

# ---- GPT Helper ----
def ask_gpt(question, category):
    system_prompt = f"""
You are an enterprise IT Service Desk assistant.
Provide clear, concise, step-by-step troubleshooting guidance for {category} issues.
Avoid sensitive data. Be professional and helpful.
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
    )

    return response.output_text

# ---- Hero ----
st.markdown("""
<div class="hero">
    <h1>🤖 Service Desk AI Portal</h1>
    <p>Self-service IT support for common workplace issues.</p>
</div>
""", unsafe_allow_html=True)

# ---- Categories ----
categories = {
    "🌐 Internet / VPN": [
        "VPN is connected but I have no internet",
        "I cannot connect to VPN from home",
        "VPN keeps disconnecting",
        "Internal websites are not loading",
        "Slow internet when connected to VPN",
        "VPN client fails to start",
        "VPN shows connected but apps don’t work",
        "VPN authentication failed",
        "VPN takes too long to connect",
        "VPN blocked by firewall",
        "Proxy issues while on VPN",
        "DNS not resolving on VPN",
        "VPN drops on Wi-Fi",
        "VPN not working after update",
        "VPN app crashes"
    ],
    "🧩 Software Issues": [
        "Outlook is not syncing emails",
        "Teams microphone is not working",
        "Application crashes on startup",
        "I cannot install approved software",
        "Software update failed",
        "License expired error message",
        "Excel is freezing",
        "App not responding",
        "Printer driver not working",
        "Software not opening",
        "Missing DLL error",
        "App needs admin rights",
        "Corrupted installation",
        "Software compatibility issue",
        "Error code during launch"
    ],
    "🔐 Access / Password": [
        "I forgot my corporate password",
        "My account is locked",
        "Request access to shared drive",
        "I cannot access an internal system",
        "MFA is not working",
        "Permission denied error",
        "SSO login failed",
        "Expired password message",
        "Account disabled",
        "Access revoked by admin",
        "Unable to reset password",
        "New user access request",
        "Role missing permissions",
        "VPN access denied",
        "Cannot login after reset"
    ],
}

st.markdown("## ⚡ Choose a category")

c1, c2, c3 = st.columns(3)

for col, cat in zip([c1, c2, c3], categories.keys()):
    with col:
        if st.button(cat, use_container_width=True):
            st.session_state["selected_category"] = cat
            st.session_state["selected_question"] = None

# ---- Issues in 3 Columns ----
if "selected_category" in st.session_state:
    st.divider()
    st.subheader(f"Issues: {st.session_state['selected_category']}")

    issues = categories[st.session_state["selected_category"]]

    col1, col2, col3 = st.columns(3)

    for i, q in enumerate(issues):
        target_col = [col1, col2, col3][i % 3]
        with target_col:
            if st.button(q, key=q):
                st.session_state["selected_question"] = q



# ---- AI Answer ----
if st.session_state.get("selected_question"):
    st.divider()
    st.markdown("### 🤖 Recommended Fix")
    with st.spinner("Generating step-by-step solution..."):
        answer = ask_gpt(
            st.session_state["selected_question"],
            st.session_state["selected_category"]
        )
    st.success(answer)

# ---- Footer ----
st.markdown("---")
st.caption("Enterprise Service Desk • AI-powered troubleshooting")