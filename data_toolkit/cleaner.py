import pandas as pd

def clean_dataframe(df):
    df=df.copy()
    df.columns=[str(c).strip().lower().replace(' ','_') for c in df.columns]
    df=df.drop_duplicates().dropna(how='all')
    return df
