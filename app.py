import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import matplotlib.pyplot as plt

names = ["Admin User", "Staff User"]
usernames = ["admin", "staff"]

# Passwords (plain text)
passwords = ["1234", "abcd"]

# Convert to hashed passwords
hashed_passwords = stauth.Hasher(passwords).generate()


authenticator = stauth.Authenticate(
    names,
    usernames,
    hashed_passwords,
    "eco_app",
    "abcdef",
    cookie_expiry_days=1
)

name, authentication_status, username = authenticator.login("Login", "main")


if authentication_status == False:
    st.error("Username/password incorrect")

if authentication_status == None:
    st.warning("Please enter login details")

if authentication_status:

    authenticator.logout("Logout", "sidebar")

    st.sidebar.write(f"Welcome {name} 👋")

    
    df = pd.read_csv("Eco bin connect.csv")

    st.title("Eco-Bin Connect Dashboard")

    area = st.selectbox("Select Area", df['Area'].unique())
    filtered_df = df[df['Area'] == area]

    st.write(filtered_df)

    st.bar_chart(filtered_df['Waste_Type'].value_counts())
