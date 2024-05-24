import streamlit as st
import requests
import json

# Your Adjust API endpoint and token
API_ENDPOINT = "https://dash.adjust.com/control-center/reports-service/<endpoint>"
API_TOKEN = "sJFzfMUwRVjGBEjhX-i2"

def fetch_adjust_data():
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }

    response = requests.get(API_ENDPOINT, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        st.error(f"Failed to fetch data. Status code: {response.status_code}")
        st.error(response.text)
        return None

st.title("Adjust API Data Fetcher")
st.write("This app fetches data from the Adjust API using the provided endpoint and API token.")

# Fetch data button
if st.button("Fetch Data"):
    with st.spinner("Fetching data..."):
        data = fetch_adjust_data()
        if data:
            st.success("Data fetched successfully!")
            st.json(data)
        else:
            st.error("Failed to fetch data. Please check the API endpoint and token.")

st.write("Click the button above to fetch data from the Adjust API.")
