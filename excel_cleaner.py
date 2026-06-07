import pandas as pd
from pathlib import Path


def clean_excel(input_file, output_file=None):
    df = pd.read_excel(input_file)
    original_rows = len(df)
    df.columns=[str(c).strip().lower().replace(' ','_') for c in df.columns]
    df=df.drop_duplicates().dropna(how='all')
    for col in df.select_dtypes(include=['object']).columns:
        df[col]=df[col].astype(str).str.strip()
    if output_file is None:
        output_file=str(Path(input_file).with_stem(Path(input_file).stem+'_cleaned'))
    df.to_excel(output_file,index=False)
    print({'rows_before':original_rows,'rows_after':len(df)})
    return df

if __name__=='__main__':
    clean_excel(input('Excel file path: ').strip())