import tkinter as tk
import pandas as pd
import requests

def fetch_data(filter_condition):
    url = "https://maps.memphistn.gov/mapping/rest/services/PublicWorks/Drain_Services_PROD/FeatureServer/0/query"
    params = {
        "where": filter_condition,  # Placeholder for filtering condition
        "outFields": "*",
        "f": "json"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json().get("features", [])
        records = [record["attributes"] for record in data]
        return pd.DataFrame(records)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return pd.DataFrame()

def query_data():
    df1 = fetch_data("(REQUEST_TYPE LIKE '%flood%' Or REQUEST_SUMMARY LIKE '%flood%' Or REQUEST_SUMMARY LIKE '%stand%' Or REQUEST_SUMMARY LIKE '%clog%' Or REQUEST_TYPE LIKE '%clean inlet%' Or REQUEST_SUMMARY LIKE '%clean inlet%' Or REQUEST_SUMMARY LIKE '%hotspot%') And REQUEST_STATUS = 'Open'")
    df2 = fetch_data("(REQUEST_TYPE LIKE '%flood%' Or REQUEST_SUMMARY LIKE '%flood%' Or REQUEST_SUMMARY LIKE '%stand%' Or REQUEST_SUMMARY LIKE '%clog%' Or REQUEST_TYPE LIKE '%clean inlet%' Or REQUEST_SUMMARY LIKE '%clean inlet%') AND REQUEST_SUMMARY not LIKE '%hotspot%' And CLOSE_DATE >= CURRENT_DATE()")
    df3 = fetch_data("(REQUEST_TYPE LIKE '%flood%' Or REQUEST_SUMMARY LIKE '%flood%' Or REQUEST_SUMMARY LIKE '%stand%' Or REQUEST_SUMMARY LIKE '%clog%' Or REQUEST_TYPE LIKE '%clean inlet%' Or REQUEST_SUMMARY LIKE '%clean inlet%') And REQUEST_SUMMARY NOT LIKE '%hotspot%' And REQUEST_STATUS = 'Open'")
    df4 = fetch_data("REQUEST_SUMMARY LIKE '%hotspot%' And REQUEST_STATUS = 'Open'")
    df5 = fetch_data("REQUEST_SUMMARY LIKE '%hotspot%' And CLOSE_DATE >= CURRENT_DATE()")
    

    floodingRequests = len(df1) if not df1.empty else 0
    floodingCompleted = len(df2) if not df2.empty else 0
    outstandingFloods = len(df3) if not df3.empty else 0
    outstandingHotspots = len(df4) if not df4.empty else 0
    hotspotsCompleted = len(df5) if not df5.empty else 0
    
    resultLabel.config(text=(
        f"Number of Flooding Requests: {floodingRequests}\n"
        f"Number of Flooding Requests Completed Today: {floodingCompleted}\n"
        f"Number of Outstanding Flooding Requests: {outstandingFloods}\n"
        f"Number of Hotspot Locations Completed Today: {hotspotsCompleted}\n"
        f"Number of Outstanding Hotspot Locations: {outstandingHotspots}"
    ))

def main():
    global resultLabel
    root = tk.Tk()
    root.title("Flood Data")
    root.geometry("500x200")
    
    submitButton = tk.Button(root, text="Retrieve Flood Data", command=query_data)
    submitButton.pack(pady=5)
    
    resultLabel = tk.Label(root, text="")
    resultLabel.pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    main()
