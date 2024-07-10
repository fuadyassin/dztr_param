# DZTR Parameter Library

The `dztr_param` library provides functionalities to process and analyze reservoir storage, inflow, and release data, including percentile calculations and CSV creation. It is designed to have all parameterization needed for dztr model for GrandID dams as long as data avaialbe for it. And then generating necessary output files for further analysis in hydrological model run.

## Features

- **Extended Columns Creation**: Automatically create extended columns required for analysis.
- **File Reading**: Efficiently read and check data files.
- **Percentile Calculation**: Calculate percentiles for various metrics such as storage, inflow, and outflow.
- **Data Updating**: Update extended data with new calculations.
- **CSV and TXT Creation**: Generate combined output files (CSV or TXT) based on the processed data.

## Installation

To install the library directly from GitHub, use the following command: `pip install git+https://github.com/fuadyassin/dztr_param.git`

### Uninstall the Existing Package

If you need to uninstall the existing package: `pip uninstall dztr_param -y`

### Upgrade the Package

To upgrade the package to the latest version: `pip install --upgrade git+https://github.com/fuadyassin/dztr_param.git`

## Usage

### Import and Check Available Functions

```python
import dztr_param
print(dir(dztr_param))
from dztr_param import create_extended_columns, check_and_read_files, calculate_percentiles, update_extended_data, create_combined_csv
```
## Define file paths
```python
original_file_path = '/content/drive/MyDrive/DZTR/GRanD_Dams_v1_1_DZTR.xlsx'
extended_file_path = '/content/drive/MyDrive/DZTR/Extended_GRanD_Dams_v1_1_DZTR.xlsx'
output_csvfile_path = '/content/drive/MyDrive/DZTR/combined_output.csv'
hydrolakes_file_path = '/content/drive/MyDrive/DZTR/Hydro_LakesTypes_2_3_DZTR.xlsx'
output_txtfile_path = '/content/drive/MyDrive/DZTR/combined_output.txt'
datafolder = '/content/drive/MyDrive/DZTR/ResDataInflowStorageRelease'
```
## Create Extended DataFrame (Optional)
```python
import pandas as pd

# Create an empty DataFrame with the extended columns
extended_columns = create_extended_columns()
extended_data = pd.DataFrame(columns=extended_columns)

# Populate the new DataFrame with the relevant columns from the original data
original_data = pd.read_excel(original_file_path)
extended_data[['GRAND_ID', 'RES_NAME', 'DAM_NAME']] = original_data[['GRAND_ID', 'RES_NAME', 'DAM_NAME']]

# Save the extended DataFrame to a new Excel file
extended_data.to_excel(extended_file_path, index=False)

```
## Update Data with Newly Estimated Quantiles
If the values are already calculated and available in the file for a given ID, skip this step.
```python
# Read the existing extended Excel file into a DataFrame
extended_data = pd.read_excel(extended_file_path)

# List of GRAND_IDs to update, if id is not part of the list use the first otherwise it just needs the id and will pick up names
grand_ids_to_update = [(253, 'ResName1', 'DamName1'), (131, 'ResName2', 'DamName2')]
# or
grand_ids_to_update = [253, 131]

# Update the data
extended_data = update_extended_data(extended_data, grand_ids_to_update, folder=datafolder)

# Save the updated DataFrame back to the Excel file
extended_data.to_excel(extended_file_path, index=False)
```
## Generate Output Files for Model Requirement
Once the quantiles are estimated and updated in the file, generate files for model requirements in either CSV or TXT format.
```python
# Define the list of percentiles
percentiles = ['10', '45', '85']

# Create combined CSV
create_combined_csv(grand_ids_to_update, original_file_path, extended_file_path, output_csvfile_path)

# Create combined TXT (assuming a similar function exists for TXT creation)
create_combined_txt(grand_ids_to_update, original_file_path, extended_file_path, hydrolakes_file_path, output_txtfile_path, percentiles)
```

