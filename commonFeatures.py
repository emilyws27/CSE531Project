import csv

def find_common_item_ids(csv_file_path):
    # Initialize a dictionary to store ITEMIDs for each SUBJECT_ID
    subject_item_mapping = {}

    # Read the CSV file
    with open(csv_file_path, 'r') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            subject_id = row['SUBJECT_ID']
            item_id = row['ITEMID']

            # Initialize a set for each SUBJECT_ID if not already present
            if subject_id not in subject_item_mapping:
                subject_item_mapping[subject_id] = set()

            # Add the ITEMID to the set for the current SUBJECT_ID
            subject_item_mapping[subject_id].add(item_id)

    # Find the intersection of all ITEMID sets
    common_item_ids = set.intersection(*subject_item_mapping.values())

    return common_item_ids


outputFolderPath = './../../../box/CSE 531 Project/'

common_item_ids = find_common_item_ids(outputFolderPath+'filtered_chartevents.csv')

# Print the common ITEMIDs
print("Common ITEMIDs for all SUBJECT_IDs:")
for item_id in common_item_ids:
    print(item_id)

