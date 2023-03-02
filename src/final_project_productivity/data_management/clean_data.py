"""Function(s) for cleaning the data set(s)."""
import pandas as pd

def _clean_data(df):
    """Clean data set"""
    df = df.iloc[1:, :]
    df.rename(columns={df.columns[0]: "sector", df.columns[1]: "year"}, inplace=True)

    i = 2
    while i <= (len(df.columns) - 1):
        df = df.rename(columns={df.columns[i]: df.iloc[0, i]})
        i += 1

    df = df.iloc[1:, :]

    sector_values = df['sector'].values
    prev_sector = None
    for i in range(len(sector_values)):
        if pd.isnull(sector_values[i]):
            if prev_sector is not None:
                sector_values[i] = prev_sector
            else:
                continue
        else:
            prev_sector = sector_values[i]

    # update the sector column in the dataframe
    df['sector'] = sector_values

    df = df.sort_values(['sector','year'])

    df = df.dropna()

    df["year"] = df["year"].astype(int)

    return df

def _rename_frame(df):
    old_names = df.columns.tolist()[2:]
    new_names = ["CC", "CF", "FA", "TH", "CE", "VA"]
    df = df.rename(columns=dict(zip(old_names,new_names)))
    
    return df

def _merge_all(df1, df2, df3):
    merged_df = pd.merge(df1, df2, on=['sector', 'year'])
    merged_df = pd.merge(merged_df, df3, on=['sector', 'year'])
    
    return merged_df

def clean_and_merge(file1, file2, file3):
    df1 = _clean_data(file1)
    df2 = _clean_data(file2)
    df3 = _clean_data(file3)

    complete = _merge_all(df1, df2, df3)

    complete = _rename_frame(complete)

    return complete
