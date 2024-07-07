import pandas as pd
from .file_reader import check_and_read_files
from .percentiles import calculate_percentiles

def update_extended_data(extended_data, grand_id, res_name, dam_name):
    resdata = check_and_read_files(grand_id)
    
    if resdata is not None:
        first_date = resdata.iloc[0]
        last_date = resdata.iloc[-1]
        
        start_year, start_month, start_day = int(first_date['year']), int(first_date['month']), int(first_date['day'])
        end_year, end_month, end_day = int(last_date['year']), int(last_date['month']), int(last_date['day'])
        
        start_date = pd.Timestamp(year=start_year, month=start_month, day=start_day)
        end_date = pd.Timestamp(year=end_year, month=end_month, day=end_day)
        timed = pd.date_range(start=start_date, end=end_date, freq='D')
        
        resdata['timed'] = timed
        
        percentiles_df = calculate_percentiles(resdata)
        
        update_dict = {}
        
        for metric in ['Q', 'S', 'I']:
            if metric == 'Q':
                variable = 'Outflow(cms)'
            elif metric == 'S':
                variable = 'Storage(mil_m3)'
            elif metric == 'I':
                variable = 'Inflow(cms)'
            
            if variable in resdata.columns:
                for idx, percentile in enumerate(range(5, 105, 5)):
                    update_dict[f'{metric}{percentile}'] = percentiles_df[f'{variable}_all'][idx]
                    for month in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
                        update_dict[f'{metric}{percentile}_{month}'] = percentiles_df[f'{variable}_{month}'][idx]
        
        if grand_id not in extended_data['GRAND_ID'].values:
            new_row = {'GRAND_ID': grand_id, 'RES_NAME': res_name, 'DAM_NAME': dam_name}
            extended_data = extended_data.append(new_row, ignore_index=True)
        
        index = extended_data.index[extended_data['GRAND_ID'] == grand_id].tolist()[0]
        update_df = pd.DataFrame(update_dict, index=[index])
        extended_data.update(update_df)
    
    return extended_data
