import os
import shutil
import re

def extract_village_info(village_folder_name):
    match = re.match(r'^(\d{7})_(.+)', village_folder_name)
    if match:
        return match.group(1), match.group(2)
    else:
        return None, None

def copy_vm_folders(root_folder, target_folder):
    for district_folder in os.listdir(root_folder):
        district_path = os.path.join(root_folder, district_folder)
        for mandal_folder in os.listdir(district_path):
            mandal_path = os.path.join(district_path, mandal_folder)
            for village_folder in os.listdir(mandal_path):
                village_path = os.path.join(mandal_path, village_folder)
                village_code, village_name = extract_village_info(village_folder)
                if village_code and village_name:
                    vm_folder_path = os.path.join(village_path, f'{village_code}_VM_{village_name}')
                    if os.path.exists(vm_folder_path) and os.path.isdir(vm_folder_path):
                        target_vm_folder_path = os.path.join(target_folder, f"{village_folder}")
                        shutil.copytree(vm_folder_path, target_vm_folder_path)
                        print(f"Copied {vm_folder_path} to {target_vm_folder_path}")

# Specify the root folder (district folder) where villages are located
root_folder = r'\\CENTRAL_LAB\Final_deliverables\sample'

# Specify the target folder where VM folders will be copied
target_folder = r'C:\Users\HP\Desktop\VM_Folders'

# Copy VM folders to the target folder
copy_vm_folders(root_folder, target_folder)
