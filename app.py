import streamlit as st

# -------- USER DATABASE --------
users = {
    "admin": "1234",
    "staff": "abcd"
}

# -------- SESSION --------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# -------- LOGIN FUNCTION --------
def login():
    st.title("🔐 Eco-Bin Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.session_state.user = username
        else:
            st.error("Invalid username or password")

# -------- LOGOUT --------
def logout():
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False

# -------- FLOW --------
if not st.session_state.logged_in:
    login()
    st.stop()

logout()
st.sidebar.write(f"Welcome {st.session_state.user} 👋")
