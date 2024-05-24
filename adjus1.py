import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt

# Adjust API endpoint (replace with actual URL)
api_url = "https://dash.adjust.com/control-center/reports-service/report"

# Placeholder for your API token (obtain from Adjust dashboard)
api_token = "sJFzfMUwRVjGBEjhX-i2"

# Available dimensions and metrics (adjust as needed)
dimensions = ["app", "date", "partner", "campaign"]
metrics = ["installs", "revenue", "cost"]

def fetch_data(start_date, end_date, partner=None, campaign=None):
    """Fetches data from the Adjust Report Service API based on filters.

    Args:
        start_date (str): Start date in YYYY-MM-DD format.
        end_date (str): End date in YYYY-MM-DD format.
        partner (str, optional): Partner name to filter by. Defaults to None.
        campaign (str, optional): Campaign name to filter by. Defaults to None.

    Returns:
        pandas.DataFrame: Dataframe containing the fetched data.
    """

    filters = {
        "dimensions": ",".join(dimensions),
        "metrics": ",".join(metrics),
        "date_period": f"{start_date}:{end_date}",
    }

    if partner:
        filters["partner__in"] = partner

    if campaign:
        filters["campaign__in"] = campaign

    headers = {"Authorization": f"Bearer {api_token}"}
    response = requests.get(api_url, headers=headers, params=filters)

    if response.status_code == 200:
        data = response.json()
        return pd.DataFrame(data["rows"])
    else:
        st.error(f"Error fetching data: {response.status_code}")
        return None

def plot_data(data, metric):
    """Plots the selected metric as a curve graph using Matplotlib.

    Args:
        data (pandas.DataFrame): Dataframe containing fetched data.
        metric (str): Metric to plot (e.g., "installs", "revenue", "cost").
    """

    dates = data["date"]
    values = data[metric]

    plt.figure(figsize=(10, 6))
    plt.plot(dates, values)
    plt.xlabel("Date")
    plt.ylabel(metric)
    plt.title(f"{metric} over Time")
    plt.xticks(rotation=45)  # Rotate x-axis labels for readability
    st.pyplot()

st.title("Adjust Data Fetcher")

# Date filter
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", min_history=30)
with col2:
    end_date = st.date_input("End Date")

# Partner filter (optional)
partner_filter = st.selectbox("Partner Filter (Optional)", [""] + ["Partner 1", "Partner 2", "..."], key="partner_filter")

# Campaign filter (optional)
campaign_filter = st.selectbox("Campaign Filter (Optional)", [""] + ["Campaign A", "Campaign B", "..."], key="campaign_filter")

# Select metric for curve graph
metric_to_plot = st.selectbox("Select Metric for Curve Graph", metrics)

# Submit button
if st.button("Fetch Data"):
    data = fetch_data(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"), partner=partner_filter, campaign=campaign_filter)

    if data is not None:
        st.dataframe(data.head())  # Display a preview of the data
        plot_data(data, metric_to_plot)
