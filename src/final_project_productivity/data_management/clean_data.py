"""Function(s) for cleaning the data set(s)."""
import pandas as pd
pd.options.mode.chained_assignment = None

def _clean_data(df):
    """Takes raw data as pandas data frame, removes empty columns and rows, set column names, set sector names for all rows,
    sorts it after sector, year and drops NA rows.

    Returns: cleaned data frame"""

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

    df['sector'] = sector_values
    df = df.sort_values(['sector','year'])
    df = df.dropna()
    df["year"] = df["year"].astype(int)

    return df

def _rename_frame(df):
    """Takes data frame, reads column names, and renames all columns to standardized names.
    
    Returns: data frame with new column names"""

    old_names = df.columns.tolist()[2:]
    new_names = ["CC", "CF", "FA", "TH", "CE", "VA"]
    df = df.rename(columns=dict(zip(old_names,new_names)))
    
    return df

def _merge_all(df1, df2, df3):
    """Takes three data frames, and stack them together from the right on sector and year.
    
    Returns: a data frame with the information from all three."""

    merged_df = pd.merge(df1, df2, on=['sector', 'year'])
    merged_df = pd.merge(merged_df, df3, on=['sector', 'year'])
    
    return merged_df

def clean_and_merge_nor(capital, hours, value_added):
    """Takes three data frames, capital, hours and value_added, and cleans them, then merge them and at the ned rename them.
    
    Returns: the complete data frame, ready to be saved"""
    
    df1 = _clean_data(capital)
    df2 = _clean_data(hours)
    df3 = _clean_data(value_added)

    complete = _merge_all(df1, df2, df3)
    complete = _rename_frame(complete)

    return complete
