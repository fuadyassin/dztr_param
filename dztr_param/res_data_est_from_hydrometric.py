import os
import requests
import numpy as np
import pandas as pd
from io import StringIO

def create_date_range(start_date, end_date):
    return pd.date_range(start=start_date, end=end_date)

def get_area_volume_from_csv(csv_id, depth, folder_path):
    file_path = f"{folder_path}/{csv_id}.csv"

    with open(file_path, 'r') as file:
        lines = file.readlines()

    dam_height = None
    for line in lines:
        if line.startswith("Dam Height (m)"):
            dam_height = float(line.split('=')[1].strip())
            break

    if dam_height is None:
        raise ValueError("Dam Height (m) not found in the CSV file.")

    depth = dam_height - depth

    if depth > dam_height or depth < 0:
        raise ValueError("Depth must be within the range of 0 to Dam Height.")

    # Find the starting index of the actual data
    data_start_idx = next(i for i, line in enumerate(lines) if line.startswith("Depth(m)"))
    data_lines = lines[data_start_idx + 1:]  # Skip the header line

    # Use comma as delimiter and handle whitespace issues
    df = pd.read_csv(StringIO(''.join(data_lines)), delimiter=',', skipinitialspace=True)
    
    # Manually set the correct column names
    df.columns = ['Depth(m)', 'Area(skm)', 'Storage(mcm)']
    
    # Append a row for dam height if it does not exist
    if dam_height not in df['Depth(m)'].values:
        last_row = df.iloc[-1]
        new_row = pd.DataFrame({
            'Depth(m)': [dam_height],
            'Area(skm)': [last_row['Area(skm)']],
            'Storage(mcm)': [last_row['Storage(mcm)']]
        })
        df = pd.concat([df, new_row], ignore_index=True)

    if depth in df['Depth(m)'].values:
        area = df.loc[df['Depth(m)'] == depth, 'Area(skm)'].values[0]
        volume = df.loc[df['Depth(m)'] == depth, 'Storage(mcm)'].values[0]
        return area, volume

    lower_df = df[df['Depth(m)'] <= depth].tail(1)
    upper_df = df[df['Depth(m)'] > depth].head(1)

    if lower_df.empty or upper_df.empty:
        raise ValueError("Depth is out of the range of the available data.")

    lower_depth = lower_df['Depth(m)'].values[0]
    upper_depth = upper_df['Depth(m)'].values[0]

    if depth == lower_depth:
        return lower_df['Area(skm)'].values[0], lower_df['Storage(mcm)'].values[0]

    if depth == upper_depth:
        return upper_df['Area(skm)'].values[0], upper_df['Storage(mcm)'].values[0]

    area = lower_df['Area(skm)'].values[0] + (depth - lower_depth) * (upper_df['Area(skm)'].values[0] - lower_df['Area(skm)'].values[0]) / (upper_depth - lower_depth)
    volume = lower_df['Storage(mcm)'].values[0] + (depth - lower_depth) * (upper_df['Storage(mcm)'].values[0] - lower_df['Storage(mcm)'].values[0]) / (upper_depth - lower_depth)

    return area, volume

def fetch_hydrometric_data_ca(station_numbers, start_date, end_date, data_type='discharge', limit=1000):
    if data_type not in ['discharge', 'level']:
        raise ValueError("data_type must be either 'discharge' or 'level'")

    property_name = 'DISCHARGE' if data_type == 'discharge' else 'LEVEL'

    if start_date is None or end_date is None:
        start_date = '1900-01-01'
        end_date = pd.Timestamp.today().strftime('%Y-%m-%d')

    dates = create_date_range(start_date, end_date)
    combined_df = pd.DataFrame({'Date': dates})

    for station_number in station_numbers:
        data_dict = {'Date': dates, station_number: [np.nan] * len(dates)}
        date_index_dict = {str(date.date()): idx for idx, date in enumerate(dates)}

        offset = 0
        full_data = []

        while True:
            url = f"https://api.weather.gc.ca/collections/hydrometric-daily-mean/items"
            params = {
                'STATION_NUMBER': station_number,
                'datetime': f"{start_date}/{end_date}",
                'limit': limit,
                'offset': offset,
                'f': 'json'
            }

            response = requests.get(url, params=params)
            response_data = response.json()

            if 'features' in response_data and response_data['features']:
                full_data.extend(response_data['features'])
                offset += limit
                if len(response_data['features']) < limit:
                    break
            else:
                break

        if full_data:
            data_list = [
                {
                    'Date': feature['properties']['DATE'],
                    'value': feature['properties'][property_name] if feature['properties'][property_name] is not None else np.nan
                }
                for feature in full_data
            ]

            data_df = pd.DataFrame(data_list)
            data_df['value'] = pd.to_numeric(data_df['value'], errors='coerce')
            data_df['Date'] = pd.to_datetime(data_df['Date']).dt.date.astype(str)

            for date, value in zip(data_df['Date'], data_df['value']):
                if date in date_index_dict:
                    date_index = date_index_dict[date]
                    if np.isnan(data_dict[station_number][date_index]):
                        data_dict[station_number][date_index] = value
                    else:
                        data_dict[station_number][date_index] += value

            station_df = pd.DataFrame(data_dict)
            combined_df = pd.merge(combined_df, station_df, on='Date', how='outer')

    combined_df['value'] = combined_df.iloc[:, 1:].sum(axis=1)
    combined_df = combined_df[['Date', 'value']]

    return combined_df

def merge_hydrometric_data(level_station_number, inflow_station_numbers, outflow_station_numbers, start_date, end_date, csv_id, folder_path, output_path):
    storage_df = fetch_hydrometric_data_ca([level_station_number], start_date, end_date, data_type='level')
    storage_df = storage_df.rename(columns={'value': 'Storage(mcm)'})

    if inflow_station_numbers:
        inflow_df = fetch_hydrometric_data_ca(inflow_station_numbers, start_date, end_date, data_type='discharge')
        inflow_df = inflow_df.rename(columns={'value': 'Inflow(cms)'})
    else:
        inflow_df = None

    outflow_df = fetch_hydrometric_data_ca(outflow_station_numbers, start_date, end_date, data_type='discharge')
    outflow_df = outflow_df.rename(columns={'value': 'Outflow(cms)'})

    merged_df = storage_df.copy()

    if inflow_df is not None:
        merged_df = pd.merge(merged_df, inflow_df, on='Date', how='outer')

    merged_df = pd.merge(merged_df, outflow_df, on='Date', how='outer')

    max_level = merged_df['Storage(mcm)'].max()
    for i, row in merged_df.iterrows():
        if not pd.isna(row['Storage(mcm)']):
            depth = max_level - row['Storage(mcm)']
            _, volume = get_area_volume_from_csv(csv_id, depth, folder_path)
            merged_df.at[i, 'Storage(mcm)'] = volume

    merged_df.to_excel(os.path.join(output_path, f"{csv_id}_inf_sto_out.xlsx"), index=False)
