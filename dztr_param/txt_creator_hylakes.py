import os
import pandas as pd
import numpy as np
def create_com_txt_hylakes(grand_id_list, original_file_path, extended_file_path, hydrolakes_file_path, output_file_path, percentiles):
    # Read the original Excel file and the extended data
    original_data = pd.read_excel(original_file_path)
    extended_data = pd.read_excel(extended_file_path)
    hydrolakes_data = pd.read_excel(hydrolakes_file_path)

    # Open the output text file for writing
    with open(output_file_path, 'w') as file:
        # Write the total number of reservoirs
        total_reservoirs = len(grand_id_list)
        file.write(f"{total_reservoirs} # Number of reservoirs\n")
        
        # Iterate over each GRAND_ID in the provided list
        for idx, grand_id in enumerate(grand_id_list, 1):
            original_row = original_data[original_data['GRAND_ID'] == grand_id]
            extended_row = extended_data[extended_data['GRAND_ID'] == grand_id]
            hydrolakes_row = hydrolakes_data[hydrolakes_data['Grand_id'] == grand_id]

            if original_row.empty or extended_row.empty or hydrolakes_row.empty:
                print(f"No data found for GRAND_ID {grand_id}")
                continue

            # Write reservoir index and dam name
            dam_name = original_row['DAM_NAME'].values[0]
            file.write(f"{idx} # {dam_name}\n")           
            # Write the MESH Rank
            file.write("9999 # MESH Rank\n")           
            # Write lat_dd and lon_dd
            lat_dd = original_row['LAT_DD'].values[0]
            lon_dd = original_row['LONG_DD'].values[0]
            file.write(f"{lat_dd} {lon_dd} # lat long location of reservoir\n")            
            # Write CAP_MCM
            cap_mcm = original_row['CAP_MCM'].values[0]
            file.write(f"{cap_mcm:.6e} # storage capacity\n")         
            # Write DIS_AVG_LS * 0.001
            dis_avg_ls = original_row['DIS_AVG_LS'].values[0] * 0.001
            file.write(f"{dis_avg_ls:.6e} # initial discharge\n")        
            # Write CAP_MCM * 0.8
            initial_storage = cap_mcm * 0.8
            file.write(f"{initial_storage:.6e} # initial storage\n")        
            # Write Q_DS_MAX
            q_ds_max = original_row['Q_DS_MAX'].values[0]
            file.write(f"{q_ds_max:.6e} # D/s channel capacity\n")          
            # Write INFLOW_CORR
            inflow_corr = original_row['INFLOW_CORR'].values[0]
            file.write(f"{inflow_corr:.6e} # Inflow correction\n")
            # Write dead storage
            file.write("0.1 # dead storage\n")            
            # Write Q_RAND_NOISE
            q_rand_noise = original_row['Q_RAND_NOISE'].values[0]
            file.write(f"{q_rand_noise:.6e} # random error term variance\n")
            # Write months header
            months = ' '.join(map(str, range(1, 13)))
            file.write(f"{months} # months\n")          
            # Write percentile data
            #percentiles = [10, 45, 85]
            metrics = ['S', 'Q']
            month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            
            for metric in metrics:
                for percentile in percentiles:
                    values = []
                    for month in range(1, 13):
                        column_name = f'{metric}{percentile}_{month_names[month-1]}'
                        value = extended_row[column_name].values[0]
                        values.append(f"{value:.6e}")
                    file.write(' '.join(values) + f" # {metric}{percentile} values for each month\n")

    print(f"Combined TXT file created successfully at {output_file_path}")
