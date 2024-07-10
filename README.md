# DZTR Parameter Library

This library provides functionalities to process and analyze dam data, including percentile calculations and CSV creation.

## Installation

```bash
pip install git+https://github.com/fuadyassin/dztr_param.git


from dztr_param import create_extended_columns, check_and_read_files, calculate_percentiles, update_extended_data, create_combined_csv

# Define the file paths
original_file_path = '/content/drive/MyDrive/DZTR/GRanD_Dams_v1_1_DZTR.xlsx'
extended_file_path = '/content/drive/MyDrive/DZTR/Extended_GRanD_Dams_v1_1_DZTR.xlsx'
output_csvfile_path = '/content/drive/MyDrive/DZTR/combined_output.csv'
hydrolakes_file_path = '/content/drive/MyDrive/DZTR/Hydro_LakesTypes_2_3_DZTR.xlsx'
output_txtfile_path = '/content/drive/MyDrive/DZTR/combined_output.txt'
datafolder = '/content/drive/MyDrive/DZTR/ResDataInflowStorageRelease'
############### if the file is already created, this step can be skipped#####################
# Create an empty DataFrame with the extended columns 
extended_columns = create_extended_columns()
extended_data = pd.DataFrame(columns=extended_columns)

# Populate the new DataFrame with the relevant columns from the original data
extended_data[['GRAND_ID', 'RES_NAME', 'DAM_NAME']] = original_data[['GRAND_ID', 'RES_NAME', 'DAM_NAME']]

# Save the extended DataFrame to a new Excel file
extended_data.to_excel(extended_file_path, index=False)
##############################################################################################
# Then update the data with newly estimated quantiles of storage, inflow and outflow
# if this values already caclulated and available in the file for agiven ID, skip this tep 
# Read the existing extended Excel file into a DataFrame
extended_data = pd.read_excel(extended_file_path)

# List of GRAND_IDs to update, if id is not part of the list use the first otherwise it just need the id and will pick up names
grand_ids_to_update = [(253, 'ResName1', 'DamName1'), (131, 'ResName2', 'DamName2')]
# or
grand_ids_to_update = [253, 131]

extended_data = update_extended_data(extended_data, grand_ids_to_update, folder=datafolder)

# Save the updated DataFrame back to the Excel file
extended_data.to_excel(extended_file_path, index=False)
###############################################################################################
# once the quantiles are estimated and updated in the file, now file for model requirement can be generated, either csv or txt
# it requires at which quantile you will be spliting the zones
# Define the list of percentiles
percentiles = ['10', '45', '85']
# Create combined CSV
create_com_csv_hylakes(grand_ids_to_update, original_file_path, extended_file_path, hydrolakes_file_path, output_csvfile_path, percentiles)
# Create combined txt
create_com_txt_hylakes(grand_ids_to_update, original_file_path, extended_file_path, hydrolakes_file_path, output_txtfile_path, percentiles)




