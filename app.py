import streamlit as st
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

import bcrypt

USERS = {
    "sanya": b"$2b$12$91uKzS6ffJY.iXly/6c.xOUMZYpceqBZ21yhPnN3s6wKKjD3jCMIi",
    
}

def authenticate(username, password):
    if username in USERS:
        return bcrypt.checkpw(password.encode("utf-8"), USERS[username])
    return False








def ask_gpt(question, category):
    system_prompt = f"""
You are an enterprise IT Service Desk assistant.
Provide clear, concise, step-by-step troubleshooting guidance for {category} issues.
Avoid sensitive data. Be professional.
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ]
    )

    return response.choices[0].message.content


st.set_page_config(page_title="Service Desk AI Bot", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None

# -------- LOGIN --------
if not st.session_state.logged_in:
    st.title("🔐 Corporate Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.rerun()
        else:
            st.error("Invalid credentials")

# -------- MAIN APP --------
else:
    st.sidebar.markdown(f"👤 Logged in as: {st.session_state.username}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.rerun()

    st.title("🤖 Service Desk AI Bot")
    st.write("Choose a category to see common questions:")

    categories = {
        "🌐 Internet / VPN": [
            "VPN is connected but I have no internet",
            "I cannot connect to VPN from home",
            "VPN keeps disconnecting",
            "Internal websites are not loading",
            "Slow internet when connected to VPN",
            "VPN client fails to start"
        ],
        "🧩 Software Issues": [
            "Outlook is not syncing emails",
            "Teams microphone is not working",
            "Application crashes on startup",
            "I cannot install approved software",
            "Software update failed",
            "License expired error message"
        ],
        "🔐 Access / Password": [
            "I forgot my corporate password",
            "My account is locked",
            "Request access to shared drive",
            "I cannot access an internal system",
            "MFA is not working",
            "Permission denied error"
        ]
    }

    # Category buttons
    cols = st.columns(3)
    for col, cat in zip(cols, categories.keys()):
        if col.button(cat):
            st.session_state["selected_category"] = cat
            st.session_state["selected_question"] = None

    # Show questions for selected category
    if "selected_category" in st.session_state:
        st.subheader(f"Questions for {st.session_state['selected_category']}")
        for q in categories[st.session_state["selected_category"]]:
            if st.button(q):
                st.session_state["selected_question"] = q

    # Show GPT answer
    if "selected_question" in st.session_state and st.session_state["selected_question"]:
        st.markdown("### 🤖 Answer")
        with st.spinner("Thinking..."):
            answer = ask_gpt(
                st.session_state["selected_question"],
                st.session_state["selected_category"]
            )
        st.success(answer)
