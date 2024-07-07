def create_extended_columns():
    columns = ['GRAND_ID', 'RES_NAME', 'DAM_NAME']
    metrics = ['Q', 'S', 'I']
    percentiles = ['5', '10', '35', '45', '75', '85', '95']
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    for metric in metrics:
        for percentile in percentiles:
            columns.append(f"{metric}{percentile}")
            for month in months:
                columns.append(f"{metric}{percentile}_{month}")

    return columns
