import pandas as pd

# Read xlsx file and store it in a dataframe
df = pd.read_excel('file.xlsx', skiprows=8)

# Select the first 4 columns
df = df.iloc[:, :4]

# Convert dataframe to json
json_data = df.to_json(orient='records')

# Write json data to a file
with open('file.json', 'w') as f:
    f.write(json_data)

