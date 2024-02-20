import pandas as pd
outputFolderPath = './../../../box/CSE 531 Project/' 
# Load the CSV file
df = pd.read_csv(outputFolderPath+'combined_data.csv')



subjectsVect = df['SUBJECT_ID']
df_chartevents = pd.read_csv(outputFolderPath+'/mimic-iii-clinical-database-1.4/mimic-iii-clinical-database-1.4/CHARTEVENTS.csv/CHARTEVENTS.csv')
df_d_items = pd.read_csv(outputFolderPath+'mimic-iii-clinical-database-1.4/mimic-iii-clinical-database-1.4/D_ITEMS.csv/D_ITEMS.csv')

filtered_df = df_chartevents[df_chartevents['SUBJECT_ID'].isin(subjectsVect)]



filtered_df['ITEMID'] = filtered_df['ITEMID'].map(df_d_items['LABEL'])
uniqueLabels = filtered_df['LABEL'].unique().tolist()
for label in uniqueLabels:
    print(label)


filtered_df.to_csv(outputFolderPath+'filtered_chartevents.csv', index=False)


print('end of file')