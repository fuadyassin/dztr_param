import pandas as pd

def create_com_csv_hylakes(grand_id_list, original_file_path, extended_file_path, hydrolakes_file_path, output_file_path, percentiles):
    # Read the original Excel file and the extended data
    original_data = pd.read_excel(original_file_path)
    extended_data = pd.read_excel(extended_file_path)
    hydrolakes_data = pd.read_excel(hydrolakes_file_path)
    
    # Define the row names for the CSV file
    row_names = [
        'GRANDID', 'HYLAKEID', 'DAM_NAME', 'LAT_DD', 'LONG_DD', 'SMAX', 'SINITIAL', 
        'QDS_MAX', 'QINITIAL', 'INFLOW_CORR', 'Q_RAND_NOISE', 'DZTR_TYPE',
        'LAKE_TYPE', 'LAKE_AREA', 'SHORE_LEN', 'DEPTH_AVE',
    ]
    
    # Percentile row names
    # percentiles = ['10', '45', '85']
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    metrics = ['Q', 'S']
    
    for metric in metrics:
        for percentile in percentiles:
            for month in months:
                row_names.append(f'{metric}{percentile}_{month}'.upper())
    
    # Create a dictionary to hold the data for the CSV
    csv_data = {'ROW_NAME': row_names}
    
    # Iterate over each GRAND_ID in the provided list
    for grand_id in grand_id_list:
        original_row = original_data[original_data['GRAND_ID'] == grand_id]
        extended_row = extended_data[extended_data['GRAND_ID'] == grand_id]
        hydrolakes_row = hydrolakes_data[hydrolakes_data['Grand_id'] == grand_id]
        
        if original_row.empty or extended_row.empty or hydrolakes_row.empty:
            print(f"No data found for GRAND_ID {grand_id}")
            continue
        
        # Create a list to hold the data for this GRAND_ID
        grand_id_data = []
        
        # Populate the first 16 rows from the original and hydrolakes data
        grand_id_data.append(grand_id)
        grand_id_data.append(hydrolakes_row['Hylak_id'].values[0])
        grand_id_data.append(original_row['DAM_NAME'].values[0])
        grand_id_data.append(original_row['LAT_DD'].values[0])
        grand_id_data.append(original_row['LONG_DD'].values[0])
        grand_id_data.append(original_row['CAP_MCM'].values[0])
        grand_id_data.append(original_row['CAP_MCM'].values[0] * 0.8)
        grand_id_data.append(original_row['Q_DS_MAX'].values[0])
        grand_id_data.append(original_row['DIS_AVG_LS'].values[0] * 0.001)  # Conversion from L/s to m³/s
        grand_id_data.append(original_row['INFLOW_CORR'].values[0])
        grand_id_data.append(original_row['Q_RAND_NOISE'].values[0])
        grand_id_data.append(original_row['DZTR_TYPE'].values[0])
        grand_id_data.append(hydrolakes_row['Lake_type'].values[0])
        grand_id_data.append(hydrolakes_row['Lake_area'].values[0])
        grand_id_data.append(hydrolakes_row['Shore_len'].values[0])
        grand_id_data.append(hydrolakes_row['Depth_avg'].values[0])
        
        # Populate the percentile values from the extended data
        for metric in metrics:
            for percentile in percentiles:
                for month in months:
                    column_name = f'{metric}{percentile}_{month}'
                    grand_id_data.append(extended_row[column_name].values[0])
        
        # Add this GRAND_ID's data to the CSV data dictionary with the key 'dam_<GRAND_ID>'
        csv_data[f'dam_{grand_id}'] = grand_id_data
    
    # Convert the dictionary to a DataFrame
    csv_df = pd.DataFrame(csv_data)
    
    # Save the DataFrame to a CSV file
    csv_df.to_csv(output_file_path, index=False)
    print(f"Combined CSV file created successfully at {output_file_path}")
