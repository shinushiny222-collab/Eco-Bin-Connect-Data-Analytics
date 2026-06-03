import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="EcoBin Connect",
    page_icon="♻️",
    layout="wide"
)

# ---------------- FILES ----------------

USERS_FILE = "users.csv"
COMPLAINTS_FILE = "complaints.csv"

if not os.path.exists(USERS_FILE):
    pd.DataFrame(columns=["username", "password"]).to_csv(
        USERS_FILE, index=False
    )

if not os.path.exists(COMPLAINTS_FILE):
    pd.DataFrame(
        columns=["Username", "Area", "WasteType", "Issue", "Status"]
    ).to_csv(COMPLAINTS_FILE, index=False)

# ---------------- SESSION ----------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# ---------------- FUNCTIONS ----------------

def signup():

    st.subheader(" Create Account")

    new_user = st.text_input("Username")

    new_pass = st.text_input(
        "Password",
        type="password",
        key="signup_pass"
    )

    if st.button("Sign Up"):

        users = pd.read_csv(USERS_FILE)

        if new_user in users["username"].values:
            st.error("Username already exists")

        else:

            users.loc[len(users)] = [new_user, new_pass]
            users.to_csv(USERS_FILE, index=False)

            st.success("Account Created Successfully")


def login():

    st.subheader(" Login")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

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
            st.error("Invalid Credentials")


# ---------------- LOGIN SCREEN ----------------

if not st.session_state.logged_in:

    st.title("EcoBin Connect")

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        login()

    with tab2:
        signup()

    st.stop()

# ---------------- SIDEBAR ----------------

st.sidebar.title("\\ EcoBin")

st.sidebar.success(
    f"Welcome {st.session_state.username}"
)

page = st.sidebar.radio(
    "Navigation",
    [
        " Home",
        " Report Waste",
        " My Complaints",
        " Dashboard"
    ]
)

if st.sidebar.button(" Logout"):
    st.session_state.logged_in = False
    st.rerun()

# ---------------- HOME ----------------

if page == " Home":

    st.title(" EcoBin Connect")

    st.markdown(
        """
        ### Smart Waste Management System

        Report waste issues

        Track complaints

        View waste analytics

        Keep your city clean 
        """
    )

# ---------------- REPORT PAGE ----------------

elif page == " Report Waste":

    st.title(" Report Waste")

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

    issue = st.text_area("Describe Issue")

    if st.button("Submit Complaint"):

        complaints = pd.read_csv(COMPLAINTS_FILE)

        complaints.loc[len(complaints)] = [
            st.session_state.username,
            area,
            waste_type,
            issue,
            "Pending"
        ]

        complaints.to_csv(
            COMPLAINTS_FILE,
            index=False
        )

        st.success(
            "Complaint Submitted Successfully"
        )

# ---------------- MY COMPLAINTS ----------------

elif page == " My Complaints":

    st.title(" My Complaints")

    complaints = pd.read_csv(COMPLAINTS_FILE)

    user_data = complaints[
        complaints["Username"]
        ==
        st.session_state.username
    ]

    if len(user_data) == 0:
        st.info("No Complaints Found")

    else:
        st.dataframe(user_data)

# ---------------- DASHBOARD ----------------

elif page == " Dashboard":

    st.title("EcoBin Dashboard")

    try:

        df = pd.read_csv("Eco bin connect.csv")

        col1, col2 = st.columns(2)

        efficiency = (
            (df["Collected_Status"] == "Yes").sum()
            /
            len(df)
        ) * 100

        complaints_count = (
            df["Complaint_Raised"] == "Yes"
        ).sum()

        col1.metric(
            "Collection Efficiency",
            f"{efficiency:.2f}%"
        )

        col2.metric(
            "Complaints",
            complaints_count
        )

        st.subheader("Waste Distribution")

        st.bar_chart(
            df["Waste_Type"].value_counts()
        )

        st.subheader("Area Wise Waste")

        st.bar_chart(
            df.groupby("Area")
            .size()
        )

        st.subheader("Overflow Bins")

        overflow = df[
            df["Bin_Status"] == "Overflow"
        ]

        st.dataframe(overflow)

        st.subheader("Insights")

        st.success(
            f"Most Common Waste: "
            f"{df['Waste_Type'].value_counts().idxmax()}"
        )

        st.warning(
            f"Most Complaints Area: "
            f"{df[df['Complaint_Raised']=='Yes']['Area'].value_counts().idxmax()}"
        )

    except:
        st.info(
            "Upload Eco bin connect.csv file"
        )
