import pandas as pd
from collections import Counter
import os

# Define paths
updated_combined_data_path = 'updated_combined_data.csv'
chartevents_path = './../../box/CSE 531 Project/filtered_chartevents.csv'
features_path = 'charteventsFeatures.txt'
output_path = './../../box/CSE 531 Project/extracted_chartevents.csv'

# Step 1: Read the features from charteventsFeatures.txt
with open(features_path, 'r') as file:
    features = file.read().splitlines()

# Convert features to integers if they are numeric IDs
try:
    features = [int(feature) for feature in features]
except ValueError:
    # Handle the case where features are not integers
    pass

# Step 2: Find the 1000 most common features (assuming features are already ITEMID from chartevents)
feature_counts = Counter(features)
top_1000_features = [feature for feature, count in feature_counts.most_common(1000)]

# Load the updated combined data
updated_combined_data_df = pd.read_csv(updated_combined_data_path)

# Prepare to read the CHARTEVENTS.csv in chunks
chunksize = 10 ** 5  # Adjust based on your system's memory

# Initialize a counter for the number of rows processed
rows_processed = 0
# Define columns to keep
columns_to_keep = ['SUBJECT_ID', 'ICUSTAY_ID', 'ITEMID', 'VALUE', 'VALUENUM']

try:
    # Process CHARTEVENTS.csv in chunks, filtering based on top 1000 features
    for chunk in pd.read_csv(chartevents_path, chunksize=chunksize, usecols=columns_to_keep):
        # Filter rows where ITEMID is in top_1000_features
        chunk_filtered = chunk[chunk['ITEMID'].isin(top_1000_features)]
        
        # Merge filtered chunk with updated_combined_data_df on SUBJECT_ID and ICUSTAY_ID
        merged_chunk = pd.merge(updated_combined_data_df, chunk_filtered, on=['SUBJECT_ID', 'ICUSTAY_ID'])
        rows_processed += len(merged_chunk)
        
        # Check if file exists to decide on writing header
        file_exists = os.path.isfile(output_path)
        
        # Append to CSV file (without header if file already exists)
        merged_chunk.to_csv(output_path, mode='a', header=not file_exists, index=False)
        
        print(f"Processed chunk, total rows processed so far: {rows_processed}")
        
except Exception as e:
    print(f"Error encountered: {e}.")
    raise

print(f"Data appended to {output_path}. Total rows processed: {rows_processed}.")
