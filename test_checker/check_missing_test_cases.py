import pandas as pd
import matplotlib.pyplot as plt

# Load CSV
df = pd.read_csv('rpm (2).csv', quoting=1, on_bad_lines='skip', low_memory=False)
df.dropna(how='all', inplace=True)
df = df.iloc[:, :27]
df = df.dropna(axis=1, how='all')

# Correct required columns based on the actual CSV
required_columns = [
    'ID', 'Title', 'Automation Type', 'Created By', 'Created On',
    'Estimate', 'Expected Result', 'Forecast','Preconditions', 'Priority', 'References',
    'Section', 'Section Depth', 'Section Description', 'Section Hierarchy',
    'Steps', 'Steps', 'Steps (Additional Info)', 'Steps (Expected Result)',
    'Steps (References)', 'Steps (Shared step ID)', 'Steps (Step)',
    'Suite', 'Suite ID', 'Type', 'Updated By', 'Updated On'
]


# Identify valid test case IDs
valid_id_mask = df['ID'].astype(str).str.match(r'^C\d+$', na=False)
df['Valid_ID'] = valid_id_mask

valid_rows = df[valid_id_mask].copy()

# Missing Steps 

# Define the step-related columns
step_cols = ['Steps', 'Steps (Expected Result)', 'Steps (Step)', 'Steps (Additional Info)']

# Identify rows with all step columns missing (NaN or blank)
missing_steps_mask = valid_rows[step_cols].isna().all(axis=1)
missing_steps_rows = valid_rows[missing_steps_mask]

# Count
# missing_count = missing_steps_mask.sum()
missing_steps_count = missing_steps_rows.shape[0]
has_steps_count = len(valid_rows) - missing_steps_count

# Pie chart
plt.figure(figsize=(8, 5))
plt.pie(
    [missing_steps_count, has_steps_count],
    labels=["Missing Steps (1,058/18,307 test cases)", "Has Steps (17,249/18,307 test cases)"],
    autopct='%1.1f%%',
    startangle=90
)
plt.title("Step Completion in Test Cases")
plt.savefig("missing_steps_pie_chart2.png")  # optional: save to file
plt.show()

print(missing_steps_rows[['ID', 'Title', 'Created On']].to_string(index=False))
print(f"🧱 {missing_steps_count} valid test cases are missing all step-related columns.")
print(f"✅ {has_steps_count} valid test cases have at least one step-related field filled.")

# Created On older than 01/01/2024
valid_rows['Created On'] = pd.to_datetime(valid_rows['Created On'], errors='coerce')
created_old = valid_rows['Created On'] >= pd.Timestamp('2024-01-01')

print(f"📅 {created_old.sum()} valid test cases were created after 01/01/2024.")
print("📄 Rows (Excel-style):", (valid_rows[created_old].index + 2).tolist()) # 3689 cases!

# Pie chart values
labels = ['Created Before 2024', 'Created In or After 2024']
sizes = [created_old.sum(), len(valid_rows) - created_old.sum()]
colors = ["#ff9999",'#66b3ff']

# Plot
plt.figure(figsize=(6,6))
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
plt.title('Test Case Creation Dates')
plt.axis('equal')  # Equal aspect ratio ensures pie is a circle
plt.savefig("created_on_distribution.png")
plt.show()


# Test cases created per year

# Ensure Created On is in datetime format
df['Created On'] = pd.to_datetime(df['Created On'], errors='coerce')


# Extract year
valid_rows['Created Year'] = valid_rows['Created On'].dt.year

# Count per year
created_per_year = valid_rows['Created Year'].value_counts().sort_index()

# Plot
plt.figure(figsize=(8, 5))
created_per_year.plot(kind='bar')
plt.title("Test Cases Created per Year")
plt.xlabel("Year")
plt.ylabel("Number of Test Cases")
plt.tight_layout()
plt.savefig("test_cases_created_yoy.png")
plt.show()



# Test cases created in 2025 (adjust year as needed)
# created_2025_mask = valid_rows['Created On'].dt.year == 2025
# created_2025 = valid_rows[created_2025_mask]

# print(f"📅 {len(created_2025)} test cases were created in 2025.")
# print("🧾 Rows (Excel-style):", (created_2025.index + 2).tolist())
# print(created_2025[['ID', 'Title', 'Created On']])


# Updated On older than 01/01/2024 (adjust date as needed)
valid_rows['Updated On'] = pd.to_datetime(valid_rows['Updated On'], errors='coerce')
# Define cutoff date
cutoff_date = pd.Timestamp("2024-01-01")

# Mask for not updated since cutoff
not_updated_mask = valid_rows['Updated On'] < cutoff_date
not_updated_count = not_updated_mask.sum()
updated_count = len(valid_rows) - not_updated_count

# Pie chart
labels = ["Not Updated Since 07/01/2024\n(15,663/18,307)", "Updated Since 07/01/2024\n(2,644/18,307)"]
sizes = [not_updated_count, updated_count]
colors = ['#ff9999', '#66b3ff']

plt.figure(figsize=(6, 6))
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
plt.title("Test Cases Not Updated Since July 1, 2024")
plt.axis('equal')  # Makes pie a circle
plt.tight_layout()
plt.savefig("not_updated_since_july_pie_chart.png")
plt.show()

# Optional print
print(f"{not_updated_count} test cases were last updated before July 1, 2024.")

updated_old_mask = valid_rows['Updated On'] >= pd.Timestamp('2024-01-01')

print(f"🔄 {updated_old_mask.sum()} valid test cases were updated after 01/01/2024.")
print("📄 Rows (Excel-style):", (valid_rows[updated_old_mask].index + 2).tolist()) # about 3700


# Updated On
valid_rows['Updated On'] = pd.to_datetime(valid_rows['Updated On'], errors='coerce')
updated_old = valid_rows['Updated On'] < pd.Timestamp('2024-01-01')

# Pie chart values
labels = ['Updated Before 2024', 'Updated In or After 2024']
sizes = [updated_old.sum(), len(valid_rows) - updated_old.sum()]
colors = ["#ff9999",'#66b3ff']

# Plot
plt.figure(figsize=(6,6))
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
plt.title('Test Case Updated Dates')
plt.axis('equal')  # Equal aspect ratio ensures pie is a circle
plt.savefig("updated_on_distribution.png")
plt.show()

# Updated On cases/per year
# Ensure 'Updated On' is in datetime format for valid_rows
valid_rows['Updated On'] = pd.to_datetime(valid_rows['Updated On'], errors='coerce')

# Extract year
valid_rows['Updated Year'] = valid_rows['Updated On'].dt.year

# Count per year
updated_per_year = valid_rows['Updated Year'].dropna().astype(int).value_counts().sort_index()

# Plot
plt.figure(figsize=(8, 5))
updated_per_year.plot(kind='bar')
plt.title("Test Cases Updated per Year")
plt.xlabel("Year")
plt.ylabel("Number of Test Cases")
plt.tight_layout()
plt.savefig("test_cases_updated_yoy.png")
plt.show()


# Print summary of all the data
print(valid_id_mask.sum())
print(((df['Title'].notna()) & (df['ID'].isna())).sum())