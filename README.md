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

## Define file paths
```python
original_file_path = '/content/drive/MyDrive/DZTR/GRanD_Dams_v1_1_DZTR.xlsx'
extended_file_path = '/content/drive/MyDrive/DZTR/Extended_GRanD_Dams_v1_1_DZTR.xlsx'
output_csvfile_path = '/content/drive/MyDrive/DZTR/combined_output.csv'
hydrolakes_file_path = '/content/drive/MyDrive/DZTR/Hydro_LakesTypes_2_3_DZTR.xlsx'
output_txtfile_path = '/content/drive/MyDrive/DZTR/combined_output.txt'
datafolder = '/content/drive/MyDrive/DZTR/ResDataInflowStorageRelease'





