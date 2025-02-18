import requests
import pandas as pd

# Define the URL and parameters
url = "https://maps.memphistn.gov/mapping/rest/services/PublicWorks/Drain_Services_PROD/FeatureServer/1/query"
params = {
    "where": "1=1",
    "outFields": "*",
    "f": "json"
}

# Fetch data from the GIS server
response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()

    if "features" in data and len(data["features"]) > 0:
        # Convert the feature data into a DataFrame
        df = pd.json_normalize(data["features"])

        # Define a manual mapping of old column names to aliases
        columnMapping = {
            'attributes.INCIDENT_NUMBER': 'Service Request Number',  # Replace 'field1' with actual column name, 'alias1' with your desired alias
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

        #Remove unneeded columns
        columnsToKeep = list(columnMapping.values())
        df = df[columnsToKeep]

        # Save to Excel
        outputPath = r"C:\Users\brian.stlouis\Documents\Drain_Services_Data.xlsx"
        df.to_excel(outputPath, index=False)
        print(f"Data saved successfully to {outputPath}")
    else:
        print("No features found in the dataset.")
else:
    print(f"Error: {response.status_code} - {response.text}")
