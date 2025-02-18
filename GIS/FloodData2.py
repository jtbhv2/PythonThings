import tkinter as tk
import pandas as pd
import requests
import datetime
import subprocess


def runGISGrabber():
    subprocess.run(['python', 'mistergisgrabber(Final).py'])

def fetch_data(filter_condition):
    url = "https://maps.memphistn.gov/mapping/rest/services/PublicWorks/Drain_Services_PROD/FeatureServer/0/query"
    params = {
        "where": filter_condition,
        "outFields": "*",
        "f": "json"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        # Check if "features" exist and have data
        if "features" in data and len(data["features"]) > 0:
            # Convert the feature data into a DataFrame
            df = pd.json_normalize(data["features"])

            # Define a manual mapping of old column names to aliases
            columnMapping = {
                'attributes.INCIDENT_NUMBER': 'Service Request Number',
                'attributes.REPORTED_DATE': 'Reported Date',
                'attributes.ADDRESS1': 'Location',
                'attributes.REQUEST_TYPE':'Service Request Type ID',
                'attributes.REQUEST_SUMMARY':'Service Request Summary',
                'attributes.Drain_Zone':'Drain Zone',
                'attributes.MAP_PG':'Map Page',
                'attributes.MAP_BLK':'Map Block',
                'attributes.ASSIGNED_TO':'Assigned To',
                'attributes.SCF_URL':'SeeClickFix URL'
            }

            # Rename the columns based on the manual mapping
            df.rename(columns=columnMapping, inplace=True)

            # Keep only the needed columns
            columnsToKeep = list(columnMapping.values())
            df = df[columnsToKeep]

            #Convert some dates
            df['Reported Date'] = pd.to_datetime(df['Reported Date'], unit='ms', origin='unix')


            return df
        else:
            print("No features found in the data.")
            return pd.DataFrame()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return pd.DataFrame()

def export_data(df):
    if df.empty:
        print("No data to export.")
        return
    # Exporting the dataframe to an Excel file
    currentDate = datetime.datetime.now().strftime('%Y-%m-%d__%H-%M-%S')
    outputPath = f'FloodData{currentDate}.xlsx'
    df.to_excel(outputPath, index=False)
    print(f"Data exported successfully to {outputPath}.")

def query_data():
    global exportButton, df1
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
    
    resultLabel.config(text=(f"Number of Flooding Requests: {floodingRequests}\n"
                            f"Number of Flooding Requests Completed Today: {floodingCompleted}\n"
                            f"Number of Outstanding Flooding Requests: {outstandingFloods}\n"
                            f"Number of Hotspot Locations Completed Today: {hotspotsCompleted}\n"
                            f"Number of Outstanding Hotspot Locations: {outstandingHotspots}"))

    # Show the "Export" button after fetching data
    exportButton.pack(pady=5)

def main():
    global resultLabel, exportButton
    root = tk.Tk()
    root.title("Flood Data")
    root.geometry("500x300")

    # activeTicketsButton = tk.Button(root, text="Get Active Tickets", command=runGISGrabber)
    # activeTicketsButton.pack(pady=5)

    submitButton = tk.Button(root, text="Retrieve Flood Data", command=query_data)
    submitButton.pack(pady=5)

    resultLabel = tk.Label(root, text="")
    resultLabel.pack(pady=10)

    exportButton = tk.Button(root, text="Export to Excel", command=lambda: export_data(df1))
    exportButton.pack_forget()

    root.mainloop()

if __name__ == "__main__":
    main()
