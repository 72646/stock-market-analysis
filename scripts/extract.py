# YAML → CSV Extraction

import yaml
import pandas as pd
import glob
import os

print(" Searching YAML files...")

# UPDATED PATH (matches your structure)
files = glob.glob("stock_project/data_yaml/**/*.yaml", recursive=True)

print("Files found:", len(files))

rows = []

# Read each YAML file
for file in files:
    print("Reading:", file)

    with open(file, "r") as f:
        data = yaml.safe_load(f)

        # if list of records
        if isinstance(data, list):
            rows.extend(data)
        else:
            rows.append(data)

print("Rows collected:", len(rows))


# Convert to DataFrame
df = pd.DataFrame(rows)


# Create csv folder automatically
os.makedirs("csv", exist_ok=True)


# Save CSV inside project
df.to_csv("csv/all_stocks.csv", index=False)

print("CSV created successfully at: csv/all_stocks.csv")
