def create_extended_columns():
    columns = ['GRAND_ID', 'RES_NAME', 'DAM_NAME']
    metrics = ['Q', 'S', 'I']
    percentiles = ['5', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55', '60', '70', '75', '80', '85', '90', '95', '99']
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    for metric in metrics:
        for percentile in percentiles:
            columns.append(f"{metric}{percentile}")
            for month in months:
                columns.append(f"{metric}{percentile}_{month}")

    return columns
