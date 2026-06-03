import streamlit as st
import pandas as pd
import os

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="EcoBin Connect",
    page_icon="♻️",
    layout="wide"
)

# ---------------- FILES ----------------

USERS_FILE = "users.csv"
COMPLAINTS_FILE = "complaints.csv"

# Create files automatically if not exists

if not os.path.exists(USERS_FILE):
    pd.DataFrame(
        columns=["username", "password"]
    ).to_csv(USERS_FILE, index=False)

if not os.path.exists(COMPLAINTS_FILE):
    pd.DataFrame(
        columns=[
            "ComplaintID",
            "Username",
            "Area",
            "WasteType",
            "Issue",
            "Status"
        ]
    ).to_csv(COMPLAINTS_FILE, index=False)

# ---------------- SESSION ----------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# ---------------- SIGNUP ----------------

def signup():

    st.subheader("📝 Create Account")

    new_user = st.text_input(
        "Username",
        key="signup_username"
    )

    new_pass = st.text_input(
        "Password",
        type="password",
        key="signup_password"
    )

    if st.button(
        "Sign Up",
        key="signup_button"
    ):

        if new_user == "" or new_pass == "":
            st.warning("Fill all fields")
            return

        users = pd.read_csv(USERS_FILE)

        if new_user in users["username"].values:
            st.error("Username already exists")

        else:

            users.loc[len(users)] = [
                new_user,
                new_pass
            ]

            users.to_csv(
                USERS_FILE,
                index=False
            )

            st.success(
                "Account created successfully"
            )

# ---------------- LOGIN ----------------

def login():

    st.subheader("🔐 Login")

    username = st.text_input(
        "Username",
        key="login_username"
    )

    password = st.text_input(
        "Password",
        type="password",
        key="login_password"
    )

    if st.button(
        "Login",
        key="login_button"
    ):

        users = pd.read_csv(USERS_FILE)

        match = users[
            (users["username"] == username)
            &
            (users["password"] == password)
        ]

        if len(match) > 0:

            st.session_state.logged_in = True
            st.session_state.username = username

            st.rerun()

        else:
            st.error("Invalid username or password")

# ---------------- LOGIN SCREEN ----------------

if not st.session_state.logged_in:

    st.title("♻️ EcoBin Connect")

    tab1, tab2 = st.tabs(
        ["Login", "Sign Up"]
    )

    with tab1:
        login()

    with tab2:
        signup()

    st.stop()

# ---------------- SIDEBAR ----------------

st.sidebar.title("♻️ EcoBin")

st.sidebar.success(
    f"Welcome {st.session_state.username}"
)

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "📝 Report Waste",
        "📋 My Complaints",
        "📊 Dashboard",
        "👨‍💼 Admin Panel"
    ]
)

if st.sidebar.button("🚪 Logout"):

    st.session_state.logged_in = False
    st.session_state.username = ""

    st.rerun()

# ---------------- HOME ----------------

if page == "🏠 Home":

    st.title("🌱 EcoBin Connect")

    st.markdown("""
    ### Smart Waste Management System

    ♻️ Report Waste Problems

    📋 Track Complaints

    📊 View Analytics

    🌍 Keep Your Area Clean
    """)

# ---------------- REPORT WASTE ----------------

elif page == "📝 Report Waste":

    st.title("📝 Report Waste")

    area = st.text_input("Area")

    waste_type = st.selectbox(
        "Waste Type",
        [
            "Plastic",
            "Organic",
            "Metal",
            "E-Waste"
        ]
    )

    issue = st.text_area(
        "Describe Issue"
    )

    if st.button(
        "Submit Complaint"
    ):

        complaints = pd.read_csv(
            COMPLAINTS_FILE
        )
        complaint_id = "CMP" + str(
            len(complaints) + 1
        ).zfill(3)
        complaints.loc[
        len(complaints)
        ] = [
            complaint_id,
            st.session_state.username,
            area,
            waste_type,
            issue,
            "Pending"
        ]
        st.success(
            f"Complaint Submitted Successfully! ID: {complaint_id}"
        )
# ---------------- MY COMPLAINTS ----------------

elif page == "📋 My Complaints":

    st.title("📋 My Complaints")

    complaints = pd.read_csv(
        COMPLAINTS_FILE
    )

    user_data = complaints[
        complaints["Username"]
        ==
        st.session_state.username
    ]

    if len(user_data) == 0:

        st.info(
            "No complaints found"
        )

    else:

        st.dataframe(
            user_data,
            use_container_width=True
        )

# ---------------- DASHBOARD ----------------

elif page == "📊 Dashboard":

    st.title("📊 EcoBin Dashboard")

    csv_file = "Eco bin connect.csv"

    if os.path.exists(csv_file):

        df = pd.read_csv(csv_file)

        col1, col2 = st.columns(2)

        efficiency = (
            (
                df["Collected_Status"]
                ==
                "Yes"
            ).sum()
            /
            len(df)
        ) * 100

        complaints_count = (
            df["Complaint_Raised"]
            ==
            "Yes"
        ).sum()

        col1.metric(
            "Collection Efficiency",
            f"{efficiency:.2f}%"
        )

        col2.metric(
            "Total Complaints",
            complaints_count
        )

        st.subheader(
            "Waste Distribution"
        )

        st.bar_chart(
            df["Waste_Type"]
            .value_counts()
        )

        st.subheader(
            "Area Wise Waste"
        )

        st.bar_chart(
            df.groupby("Area")
            .size()
        )

        overflow = df[
            df["Bin_Status"]
            ==
            "Overflow"
        ]

        st.subheader(
            "Overflow Bins"
        )

        st.dataframe(
            overflow,
            use_container_width=True
        )

    else:

        st.warning(
            "Eco bin connect.csv file not found"
        )
    else:

    st.warning(
        "Eco bin connect.csv file not found"
    )

# ---------------- ADMIN PANEL ----------------

elif page == "👨‍💼 Admin Panel":

    st.title("👨‍💼 Admin Panel")

    complaints = pd.read_csv(COMPLAINTS_FILE)

    if complaints.empty:

        st.info("No complaints available")

    else:

        st.dataframe(
            complaints,
            use_container_width=True
        )

        complaint_id = st.selectbox(
            "Select Complaint",
            complaints["ComplaintID"]
        )

        new_status = st.selectbox(
            "Update Status",
            [
                "Pending",
                "In Progress",
                "Resolved"
            ]
        )

        if st.button("Update Status"):

            complaints.loc[
                complaints["ComplaintID"] == complaint_id,
                "Status"
            ] = new_status

            complaints.to_csv(
                COMPLAINTS_FILE,
                index=False
            )

            st.success(
                "Status Updated Successfully"
            )

            st.rerun()
