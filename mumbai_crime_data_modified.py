import pandas as pd
from datetime import datetime

# Load the CSV
df = pd.read_csv('C:/Users/Sakshi/Downloads/mumbai_crime_data.csv')

# Clean column names
df.columns = df.columns.str.strip()

# Convert date strings to proper format
def convert_date(date_str):
    if pd.isna(date_str) or date_str.strip() == "":
        return None
    for fmt in ("%m-%d-%Y %H:%M", "%d-%m-%Y %H:%M"):
        try:
            return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
        except:
            continue
    return None  # If all conversions fail

# Extract just time part
def extract_time(datetime_str):
    if pd.isna(datetime_str) or datetime_str.strip() == "":
        return None
    for fmt in ("%m-%d-%Y %H:%M", "%d-%m-%Y %H:%M"):
        try:
            return datetime.strptime(datetime_str, fmt).strftime("%H:%M:%S")
        except:
            continue
    return None

# Apply conversions
df["Date Reported"] = df["Date Reported"].apply(convert_date)
df["Date of Occurrence"] = df["Date of Occurrence"].apply(convert_date)
df["Date Case Closed"] = df["Date Case Closed"].apply(convert_date)
df["Time of Occurrence"] = df["Time of Occurrence"].apply(extract_time)

# Replace empty strings with 'NULL' literal for PostgreSQL
df = df.fillna("NULL")

# Save to new CSV
df.to_csv('C:/Users/Sakshi/Downloads/mumbai_crime_data_modified.csv', index=False)
print("✅ Cleaned Mumbai data saved.")
