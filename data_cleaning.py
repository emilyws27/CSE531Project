import pandas as pd

# Load the data from a CSV file
df = pd.read_csv('combined_data.csv')

# Convert the 'INTIME' and 'OUTTIME' columns to datetime
df['INTIME'] = pd.to_datetime(df['INTIME'])
df['OUTTIME'] = pd.to_datetime(df['OUTTIME'])

# Calculate the length of stay in the ICU
df['ICU_STAY_LENGTH'] = (df['OUTTIME'] - df['INTIME']).dt.total_seconds() / 3600  # ICU stay length in hours

# missing values
df['SHORT DESCRIPTION'] = df['SHORT DESCRIPTION'].fillna('NA')
df['GENDER']= df['GENDER'].fillna("NA")

# removing duplicates based on 'SUBJECT_ID' and 'HADM_ID'
df = df.drop_duplicates(subset=['SUBJECT_ID', 'HADM_ID'])

# making sure all the care units are valid
valid_care_units = ['CCU', 'CSRU', 'MICU', "NICU", "NWARD", "SICU", "TSICU"]  # Replace with actual care unit names
df['FIRST_CAREUNIT'] = df['FIRST_CAREUNIT'].apply(lambda x: x if x in valid_care_units else 'Other')
df['LAST_CAREUNIT'] = df['LAST_CAREUNIT'].apply(lambda x: x if x in valid_care_units else 'Other')

# Standardize the gender column to have consistent formatting, e.g., "M" and "F"
df['GENDER'] = df['GENDER'].str.upper()
df['GENDER'] = df['GENDER'].map({'MALE': 'M', 'FEMALE': 'F', 'M': 'M', 'F': 'F'})

# Save the cleaned and preprocessed data to a new CSV file
df.to_csv('cleaned_data.csv', index=False)

print("Data cleaning and preprocessing completed.")
