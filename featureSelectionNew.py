import pandas as pd

outputFolderPath = './../../../box/CSE 531 Project/' 

# Load the CSV file
df = pd.read_csv(outputFolderPath+'combined_data.csv', low_memory=False)

subjectsVect = df['SUBJECT_ID']
df_chartevents = pd.read_csv(outputFolderPath+'/mimic-iii-clinical-database-1.4/mimic-iii-clinical-database-1.4/CHARTEVENTS.csv/CHARTEVENTS.csv', low_memory=False)
df_d_items = pd.read_csv(outputFolderPath+'mimic-iii-clinical-database-1.4/mimic-iii-clinical-database-1.4/D_ITEMS.csv/D_ITEMS.csv', low_memory=False)

filtered_df = df_chartevents[df_chartevents['SUBJECT_ID'].isin(subjectsVect)].copy()

# Create a mapping dictionary from df_d_items
item_label_map = df_d_items.set_index('ITEMID')['LABEL'].to_dict()

# Use the map for ITEMID column
filtered_df.loc[:, 'ITEMID'] = filtered_df['ITEMID'].map(item_label_map)

# Check if 'LABEL' column exists
if 'LABEL' in filtered_df.columns:
    uniqueLabels = filtered_df['LABEL'].unique().tolist()
    for label in uniqueLabels:
        print(label)
else:
    print("LABEL column does not exist in filtered_df")

filtered_df.to_csv(outputFolderPath+'filtered_chartevents.csv', index=False)

print('end of file')
