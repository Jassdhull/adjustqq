import streamlit as st
import requests

# Function to fetch data from the Adjust API
def fetch_adjust_data(endpoint, api_token):
    headers = {
        "Authorization": f"Bearer {api_token}"
    }

    response = requests.get(endpoint, headers=headers)

    if response.status_code == 200:
        return response.json(), None
    else:
        return None, f"Failed to fetch data. Status code: {response.status_code}\nError: {response.text}"

# Streamlit application
st.title("Adjust API Data Fetcher")
st.write("This app fetches data from the Adjust API using the provided endpoint and API token.")

# User inputs for API endpoint and token
endpoint = st.text_input("API Endpoint", "https://dash.adjust.com/control-center/reports-service/<endpoint>")
api_token = st.text_input("API Token", "sJFzfMUwRVjGBEjhX-i2")

# Fetch data button
if st.button("Fetch Data"):
    with st.spinner("Fetching data..."):
        data, error = fetch_adjust_data(endpoint, api_token)
        if data:
            st.success("Data fetched successfully!")
            st.json(data)
        else:
            st.error(error)

st.write("Click the button above to fetch data from the Adjust API.")

