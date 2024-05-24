import streamlit as st
import requests

# Function to fetch data from the Adjust API
def fetch_adjust_data(endpoint, api_token, params=None):
    headers = {
        "Authorization": f"Bearer {api_token}"
    }

    response = requests.get(endpoint, headers=headers, params=params)

    if response.status_code == 200:
        return response.json(), None
    else:
        return None, f"Failed to fetch data. Status code: {response.status_code}\nError: {response.text}"

# Streamlit application
st.title("Adjust API Data Fetcher")
st.write("This app fetches data from the Adjust API using the provided endpoint and API token.")

# User inputs for API endpoint and token
endpoint = st.text_input("API Endpoint", "https://dash.adjust.com/control-center/reports-service/filters_data")
api_token = st.text_input("API Token", "sJFzfMUwRVjGBEjhX-i2")

# Input fields for query parameters
required_filters = st.text_input("Required Filters (comma separated)", "overview_metrics,cost_metrics")
section = st.selectbox("Section", ["overview", "cost", "sessions", "clicks", "installs", "events"])

# Optional search terms
overview_metrics_contains = st.text_input("Overview Metrics Contains (optional)")
cost_metrics_contains = st.text_input("Cost Metrics Contains (optional)")

# Fetch data button
if st.button("Fetch Data"):
    with st.spinner("Fetching data..."):
        params = {
            "required_filters": required_filters,
            "section": section
        }

        if overview_metrics_contains:
            params["overview_metrics__contains"] = overview_metrics_contains

        if cost_metrics_contains:
            params["cost_metrics__contains"] = cost_metrics_contains

        data, error = fetch_adjust_data(endpoint, api_token, params)
        if data:
            st.success("Data fetched successfully!")
            st.json(data)
        else:
            st.error(error)

st.write("Click the button above to fetch data from the Adjust API.")


