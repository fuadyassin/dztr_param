import os
import pandas as pd

def check_and_read_files(grand_id, folder='ResDataInflowStorageRelease'):
    files = os.listdir(folder)
    matching_files = [file for file in files if f"_{grand_id}." in file]
    
    if len(matching_files) == 0:
        print(f"No file exists for GRAND_ID {grand_id}.")
        return None
    elif len(matching_files) > 1:
        print(f"More than one file exists for GRAND_ID {grand_id}.")
        return None
    else:
        file_path = os.path.join(folder, matching_files[0])
        data = pd.read_excel(file_path)
        print(f"File for GRAND_ID {grand_id} has been read successfully.")
        return data
