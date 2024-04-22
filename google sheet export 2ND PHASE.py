import os
import re
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Define the SCOPES and your Google Sheets credentials file
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = r"C:\Users\HP\Downloads\final-deliverables-9b9f5d55ebb6.json"
SPREADSHEET_ID = '1kdlHztbY3_El72jUj5R9AfTU7XmXlP9ObY5AKUrcPTM'

def authenticate_google_sheets():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)
    return service

def update_google_sheet(service, data):
    sheet = service.spreadsheets()
    range_name = 'Sheet1!A1'
    body = {
        'values': data,
        'majorDimension': 'ROWS'
    }
    result = sheet.values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=range_name,
        valueInputOption='USER_ENTERED',
        body=body
    ).execute()
    print(f"Updated {result['updatedCells']} cells.")

def extract_village_info(village_folder_name):
    match = re.match(r'^(\d{7})_(.+)', village_folder_name)
    if match:
        return match.group(1), match.group(2)
    else:
        return None, None

def retrieve_data_from_folders(root_folder):
    data = [['District', 'Mandal', 'Village Name', 'LPM', 'RLR', 'VM', 'Stone Map', 'Correlation Map', 'Habitation Map', 'ORI Map', 'Traverse Map', '13 Notification', 'Appreciation','Shapefile']]

    for district_folder in os.listdir(root_folder):
        district_path = os.path.join(root_folder, district_folder)
        for mandal_folder in os.listdir(district_path):
            mandal_path = os.path.join(district_path, mandal_folder)
            for village_folder in os.listdir(mandal_path):
                village_path = os.path.join(mandal_path, village_folder)
                village_code, village_name = extract_village_info(village_folder)
                if village_code and village_name:
                    village_folder_name = f"{village_code}_{village_name}"
                    row_data = [district_folder, mandal_folder, village_folder_name]
                    for folder_name in folders_list:
                        folder_name_replaced = folder_name.replace('0000000', village_code).replace('Villagename', village_name)
                        folder_path = os.path.join(village_path, folder_name_replaced)
                        if os.path.exists(folder_path) and os.path.isdir(folder_path):
                            num_files = len([file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))])
                        if num_files == 0:
                            num_files = ""  # Set to 0 if folder is empty or not found
                        row_data.append(num_files)
                    data.append(row_data)
    
    return data
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
    '0000000_Appreceation',
    '0000000_Shape_File'
]

def main():
    service = authenticate_google_sheets()
    data_to_update = retrieve_data_from_folders(r"\\CENTRAL_LAB\Final_deliverables\2nd phase")
    update_google_sheet(service, data_to_update)

if __name__ == '__main__':
    main()
