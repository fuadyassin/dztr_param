import numpy as np
import pandas as pd

def calculate_percentiles(resdata):
    percentiles = range(5, 105, 5)  # Percentiles from 5 to 100, incrementing by 5
    variables = ['Storage(mil_m3)', 'Inflow(cms)', 'Outflow(cms)']
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    results = {}
    
    for variable in variables:
        if variable in resdata.columns:
            all_data_percentiles = np.percentile(resdata[variable].dropna(), percentiles)
            results[f'{variable}_all'] = all_data_percentiles
            
            for i, month in enumerate(months, start=1):
                monthly_data = resdata[resdata['month'] == i][variable].dropna()
                if not monthly_data.empty:
                    monthly_percentiles = np.percentile(monthly_data, percentiles)
                    results[f'{variable}_{month}'] = monthly_percentiles
                else:
                    results[f'{variable}_{month}'] = [np.nan] * len(percentiles)
    
    index = [f'P{p}' for p in percentiles]
    columns = []
    for variable in variables:
        if variable in resdata.columns:
            columns.append(f'{variable}_all')
            for month in months:
                columns.append(f'{variable}_{month}')
    
    results_df = pd.DataFrame(results, index=index, columns=columns)
    return results_df
