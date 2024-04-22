import os
import re
import pandas as pd

def extract_village_info(village_folder_name):
    match = re.match(r'^(\d{7})_(.+)', village_folder_name)
    if match:
        return match.group(1), match.group(2)
    else:
        return None, None

def retrieve_data_from_folders(root_folder, folders_list):
    data = {}
    
    # Add new columns at the beginning
    data['District'] = []
    data['Mandal'] = []
    # Add more columns as needed

    data['Village Name'] = []
    for folder_name in folders_list:
        data[folder_name] = []

    for district_folder in os.listdir(root_folder):
        district_path = os.path.join(root_folder, district_folder)
        for mandal_folder in os.listdir(district_path):
            mandal_path = os.path.join(district_path, mandal_folder)
            for village_folder in os.listdir(mandal_path):
                village_path = os.path.join(mandal_path, village_folder)
                village_code, village_name = extract_village_info(village_folder)
                if village_code and village_name:
                    village_folder_name = f"{village_code}_{village_name}"
                    data['Village Name'].append(village_folder_name)
                    for folder_name in folders_list:
                        folder_name_replaced = folder_name.replace('0000000', village_code).replace('Villagename', village_name)
                        folder_path = os.path.join(village_path, folder_name_replaced)
                        if os.path.exists(folder_path) and os.path.isdir(folder_path):
                            num_files = len([file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))])
                        else:
                            num_files = " "  # Set to 0 if folder is empty or not found
                        data[folder_name].append(num_files)
                    
                    # Add data to new columns
                    data['District'].append(district_folder)
                    data['Mandal'].append(mandal_folder)
                    # Add data to more columns as needed
    
    df = pd.DataFrame(data)
    return df

# Specify the root folder (district folder) using the network path
root_folder = r"\\CENTRAL_LAB\Final_deliverables\2nd phase"

# List of folders to retrieve data from
folders_list = [
    '0000000_LPM',
    '0000000_RLR',
    '0000000_VM_Villagename',
    '0000000_ST_Villagename',
    '0000000_COR_Villagename',
    '0000000_HT_Villagename',
    '0000000_ORI_Villagename',
    '0000000_TR_Villagename',
    '0000000_13_Notification',
    '0000000_Appreceation'
]

# Retrieve data from folders
data_df = retrieve_data_from_folders(root_folder, folders_list)

# Modify the data format in Excel
data_df.columns = ['District', 'Mandal', 'Village Name', 'LPM', 'RLR', 'VM', 'Stone Map', 'Correlation Map', 'Habitation Map', 'ORI Map', 'Traverse Map', '13 Notification', 'Appreciation']
# Add more column names to match the added columns

# Export to Excel
output_excel_path = r'C:\Users\HP\Desktop\final deliverables data\data_from_folders_modified.xlsx'
data_df.to_excel(output_excel_path, index=False)
print(f"Data retrieved and exported to {output_excel_path}")
