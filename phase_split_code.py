import os
import pandas as pd
import shutil

def copy_phase_villages(source_root, target_root, phase_village_list_path):
    # Load the list of 2nd phase village codes from Excel
    phase_village_df = pd.read_excel(phase_village_list_path, dtype=str)
    phase_village_codes = phase_village_df['VillageCode'].tolist()

    # Iterate through district, mandal, and village folders
    for district_folder in os.listdir(source_root):
        district_path = os.path.join(source_root, district_folder)
        for mandal_folder in os.listdir(district_path):
            mandal_path = os.path.join(district_path, mandal_folder)
            for village_folder in os.listdir(mandal_path):
                village_code = village_folder.split('_')[0]
                if village_code in phase_village_codes:
                    source_village_path = os.path.join(mandal_path, village_folder)
                    target_village_path = os.path.join(target_root, district_folder, mandal_folder, village_folder)
                    shutil.copytree(source_village_path, target_village_path)
                    print(f"Copied {village_folder} to {target_village_path}")

# Example usage with raw strings
source_root = r"D:\All District - final deliverables"
target_root = r"C:\Users\HP\Desktop\final deliverables data\3rd phase"
phase_village_list_path = r"C:\Users\HP\Desktop\final deliverables data\3rd phase.xlsx"

copy_phase_villages(source_root, target_root, phase_village_list_path)
