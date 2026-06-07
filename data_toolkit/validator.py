def validate_dataframe(df):
    issues=[]
    if df.empty:
        issues.append('Dataset is empty')
    return issues
