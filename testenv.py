input_features = r"https://maps.memphistn.gov/mapping/rest/services/PublicWorks/Drain_Services_Admin_PROD/FeatureServer/0"
target_features = r"https://maps.memphistn.gov/mapping/rest/services/PublicWorks/Drain_Services_PROD/FeatureServer/0"

import arcpy
import time
from datetime import datetime

today_date = datetime.today().date()
arcpy.CalculateField_management(input_features, "Date_Notified", f"'{today_date}'", "PYTHON3")
