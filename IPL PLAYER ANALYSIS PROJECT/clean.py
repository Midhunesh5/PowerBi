import pandas as pd

# Step 1: Load the CSV file
file_path = "BATTING STATS - IPL_2016.csv"  # Replace with your actual file path
df = pd.read_csv(file_path)

# Step 2: Clean the "HS" Column (split into Highest Score and Not Out Indicator)
# Split "HS" into numeric part and asterisk indicator
df[['Highest_Score', 'Not_Out']] = df['HS'].str.split('*', expand=True)
# Convert "Highest_Score" to numeric
df['Highest_Score'] = pd.to_numeric(df['Highest_Score'], errors='coerce')
# Replace "Not_Out" with 1 if asterisk was present, 0 if not
df['Not_Out'] = df['Not_Out'].apply(lambda x: 1 if x == '' else 0)
# Drop the original "HS" column
df = df.drop(columns=['HS'])

# Step 3: Set Data Types
# Ensure numeric columns are correctly typed
numeric_columns = ['POS', 'Mat', 'Inns', 'NO', 'Runs', 'Highest_Score', 'BF', '100', '50', '4s', '6s']
for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce', downcast='integer')

# "Avg" and "SR" as float (decimal)
df['Avg'] = pd.to_numeric(df['Avg'], errors='coerce', downcast='float')
df['SR'] = pd.to_numeric(df['SR'], errors='coerce', downcast='float')

# "Player" remains as string (already default)

# Step 4: Fix "Avg" Column (Recalculate if needed)
# Recalculate Avg as Runs / (Inns - NO), handle division by zero
df['Calculated_Avg'] = df.apply(
    lambda row: row['Runs'] / (row['Inns'] - row['NO']) if (row['Inns'] - row['NO']) > 0 else None, 
    axis=1
)
# Compare with original "Avg" and replace if you want (optional)
# For now, keep both columns; you can drop "Avg" later if "Calculated_Avg" is preferred
# df['Avg'] = df['Calculated_Avg']  # Uncomment to replace original Avg

# Step 5: Clean "Player" Column
# Remove leading/trailing spaces and capitalize each word
df['Player'] = df['Player'].str.strip().str.title()

# Step 6: Rename Columns for Clarity
df = df.rename(columns={
    'POS': 'Position',
    'Mat': 'Matches',
    'Inns': 'Innings',
    'NO': 'Not_Outs',
    'Runs': 'Total_Runs',
    'Avg': 'Batting_Average',
    'BF': 'Balls_Faced',
    'SR': 'Strike_Rate',
    '100': 'Centuries',
    '50': 'Fifties',
    '4s': 'Fours',
    '6s': 'Sixes'
})

# Step 7: Check for Errors (Optional Validation)
# Replace NaN with 0 or leave as is depending on your preference
# For now, leave NaN as is for Power BI to handle
# df = df.fillna(0)  # Uncomment to replace NaN with 0

# Step 8: Save the Cleaned Data to a New CSV
output_file = "cleaned_cricket_stats.csv"
df.to_csv(output_file, index=False)

print("Data cleaning complete. Cleaned file saved as:", output_file)

# Optional: Display the first few rows to verify
print(df.head())