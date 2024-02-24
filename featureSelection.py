import pandas as pd

outputFolderPath = './../../../box/CSE 531 Project/' 

# Load the CSV file
df = pd.read_csv(outputFolderPath+'filtered_chartevents.csv', low_memory=False)




uniqueLabels = df['ITEMID'].unique().tolist()
for label in uniqueLabels:
    print(label)
