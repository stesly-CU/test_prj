import streamlit as st
import pandas as pd
import numpy as np
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities.hasher import Hasher  # <-- add this

names = ["Ben", "Bob"]
usernames = ["user1", "user2"]

passwords = ["ben2025!", "password"]
hashed_passwords = Hasher.hash_list(passwords)  # <-- fix

# (optional) print to copy once, then hardcode if you want
# print(hashed_passwords)

credentials = {
    "usernames": {
        usernames[i]: {"name": names[i], "password": hashed_passwords[i]}
        for i in range(len(usernames))
    }
}

authenticator = stauth.Authenticate(
    credentials,
    "time_series_dashboard",
    "abcdef",
    cookie_expiry_days=1,
)

authenticator.login("main")


# --- Login checks via session_state ---
if st.session_state["authentication_status"] is False:
    st.error("❌ Username/password is incorrect")

elif st.session_state["authentication_status"] is None:
    st.warning("⚠️ Please enter your username and password")

elif st.session_state["authentication_status"]:
    authenticator.logout("Logout", "sidebar")

    # --- Main dashboard ---
    st.title("📈 Time Series Dashboard (Demo)")
    st.write(f"Welcome **{st.session_state['name']}** 👋")

    # Generate dummy time series data
    np.random.seed(42)
    dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq="D")
    values = np.random.randn(len(dates)).cumsum()
    df = pd.DataFrame({"date": dates, "value": values})

    # Sidebar filters
    st.sidebar.header("Filters")
    start_date = st.sidebar.date_input("Start date", df["date"].min())
    end_date = st.sidebar.date_input("End date", df["date"].max())

    mask = (df["date"] >= pd.to_datetime(start_date)) & (df["date"] <= pd.to_datetime(end_date))
    filtered_df = df.loc[mask]

    # Chart + Table
    st.line_chart(filtered_df.set_index("date")["value"])
    st.write("Filtered data", filtered_df)

    # Export CSV
    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download filtered data as CSV",
        data=csv,
        file_name="filtered_timeseries.csv",
        mime="text/csv",
    )
