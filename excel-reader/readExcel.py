import pandas as pd

# Read the Excel file (replace 'sample.xlsx' with your file path)
df = pd.read_excel('sample.xlsx', sheet_name='Sheet1')
print(df)
