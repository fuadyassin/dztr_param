# DZTR Parameter Library

This library provides functionalities to process and analyze dam data, including percentile calculations and CSV creation.

## Installation

```bash
pip install git+https://github.com/fuadyassin/dztr_param.git


from dztr_param import create_extended_columns, check_and_read_files, calculate_percentiles, update_extended_data, create_combined_csv

# Define the file paths
original_file_path = 'GRanD_Dams_v1_1_DZTR.xlsx'
extended_file_path = 'Extended_GRanD_Dams_v1_1_DZTR.xlsx'
output_file_path = 'combined_output.csv'

# List of GRAND_IDs to update
grand_ids_to_update = [253, 131]

# Create combined CSV
create_combined_csv(grand_ids_to_update, original_file_path, extended_file_path, output_file_path)


**`setup.py`**:
```python
from setuptools import setup, find_packages

setup(
    name='dztr_param',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
    ],
    author='Fuad Yassin',
    author_email='fuad.yassin@usask.ca',
    description='DZTR Parameter Processing Library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/fuadyassin/dztr_param',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

