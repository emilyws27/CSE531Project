import dask.dataframe as dd

# Load the data using Dask's read_csv, which is similar to pandas but operates lazily
df = dd.read_csv('./../../box/CSE 531 Project/extracted_chartevents.csv')

# Operations are similar to pandas but are executed in parallel
df['INTIME'] = dd.to_datetime(df['INTIME'])
df['OUTTIME'] = dd.to_datetime(df['OUTTIME'])
df['ICU_STAY_LENGTH'] = (df['OUTTIME'] - df['INTIME']).dt.total_seconds() / 3600

# Fill missing values
df['SHORT DESCRIPTION'] = df['SHORT DESCRIPTION'].fillna('NA')
df['GENDER'] = df['GENDER'].fillna("NA")

# Drop duplicates
df = df.drop_duplicates(subset=['SUBJECT_ID', 'HADM_ID', 'ICUSTAY_ID', 'ITEMID'])

# Standardize the 'FIRST_CAREUNIT' and 'LAST_CAREUNIT' columns
valid_care_units = ['CCU', 'CSRU', 'MICU', "NICU", "NWARD", "SICU", "TSICU"]
df['FIRST_CAREUNIT'] = df['FIRST_CAREUNIT'].apply(lambda x: x if x in valid_care_units else 'Other', meta=('FIRST_CAREUNIT', 'object'))
df['LAST_CAREUNIT'] = df['LAST_CAREUNIT'].apply(lambda x: x if x in valid_care_units else 'Other', meta=('LAST_CAREUNIT', 'object'))

# Standardize the gender column
df['GENDER'] = df['GENDER'].str.upper()
df['GENDER'] = df['GENDER'].map({'MALE': 'M', 'FEMALE': 'F', 'M': 'M', 'F': 'F'})

# Compute and convert Dask DataFrame to Pandas DataFrame for operations that require pandas
# Note: Only do this if you're sure the resulting DataFrame will fit into memory
df = df.compute()

# Save the cleaned and preprocessed data to a new CSV file
df.to_csv('./../../box/CSE 531 Project/cleaned_data_with_chart_events.csv', index=False)

print("Data cleaning and preprocessing completed.")
