import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def login():
    st.title("Eco-Bin Connect Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state["logged_in"] = True
            st.rerun()   # IMPORTANT
        else:
            st.error("Invalid login")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
    st.stop()


st.sidebar.write("👤 Logged in as admin")

if st.sidebar.button("Logout"):
    st.session_state["logged_in"] = False
    st.rerun()


df = pd.read_csv("Eco bin connect.csv")

st.title("Eco-Bin Connect Dashboard")


area = st.selectbox("Select Area", df['Area'].unique())
filtered_df = df[df['Area'] == area]

st.subheader("Filtered Data")
st.write(filtered_df)


st.subheader("Waste Type Distribution")
st.bar_chart(filtered_df['Waste_Type'].value_counts())


if 'Latitude' in df.columns and 'Longitude' in df.columns:
    st.subheader("📍 Waste Locations Map")
    st.map(df[['Latitude', 'Longitude']].dropna())


st.subheader("Overflow Bins 🚨")
overflow = df[df['Bin_Status'] == "Overflow"]
st.write(overflow)


st.subheader("Complaints")
complaints = df[df['Complaint_Raised'] == "Yes"]
st.write(complaints)


df['Date'] = pd.to_datetime(df['Date'])

st.subheader("Daily Collection Trend")
st.line_chart(df.groupby('Date')['Collected_Status'].count())


st.subheader("Insights")

st.write("Most common waste:", df['Waste_Type'].value_counts().idxmax())
st.write("Most complaints area:", df[df['Complaint_Raised']=='Yes']['Area'].value_counts().idxmax())
st.write("Most missed waste:", df[df['Collected_Status']=='No']['Waste_Type'].value_counts().idxmax())
