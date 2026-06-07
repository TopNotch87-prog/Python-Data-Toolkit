def profile_dataframe(df):
    return {
        'rows': len(df),
        'columns': len(df.columns),
        'missing_values': df.isnull().sum().to_dict(),
        'dtypes': df.dtypes.astype(str).to_dict()
    }
