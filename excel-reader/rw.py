import pandas as pd

# Read the Excel file into a DataFrame
df = pd.read_excel('sample.xlsx', sheet_name='【参考】必要機能一覧0430')

# Create a new column 'new_values' with split values
df['new_values'] = df['画面'].str.split('\n')

# Explode the new column to create separate rows
df = df.explode('new_values')

# Drop the original column with multiline values
df = df.drop('画面', axis=1)

# Rename the new column
df = df.rename(columns={'new_values': '画面'})

# Select the columns you want to write to the new Excel file
columns_to_write = ['機能ID', '機能分類（Lv0）', '機能分類（Lv1）','機能分類（Lv2）','機能名（Lv3）','機能要件（機能詳細）','画面', 'データソース']
df_selected = df[columns_to_write]

# Write the selected columns to a new Excel file
#df_selected.to_excel('new_file.xlsx', index=False)

# Print the DataFrame to the console
#print(df)
print(df_selected)

# Write the DataFrame to a new Excel file
df_selected.to_excel('out1.xlsx', index=False)