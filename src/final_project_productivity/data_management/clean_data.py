"""Function(s) for cleaning the data set(s)."""
import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None

def _clean_data_nor(df):
    """Takes raw data from ssb.no as pandas data frame, removes empty columns and rows, set column names, set sector names for all rows,
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

def _clean_data_den(df):
    df = df.iloc[1:, :]
    df.rename(columns={df.columns[0]: "sector", df.columns[1]: "year"}, inplace=True)

    i = 2
    while i <= (len(df.columns) - 1):
        df = df.rename(columns={df.columns[i]: df.iloc[0, i]})
        i += 1
    df = df.iloc[1:, :]

    df['year'] = df['year'].fillna(method='ffill')
    
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
    
    names = df.columns.tolist()[2:]
    names = [x for x in names if isinstance(x, str)]

    if len(names) > 1:
        df = df.drop(df.index[-1])
        agg_func = {
            names[0]: 'last',
            names[1]: 'first'
            }
        df = df.groupby(['sector', 'year']).agg(agg_func).reset_index()
    
    df["year"] = df["year"].astype(int)
    
    return df

def _clean_data_swe(df, col_names):

    df = df[2:]
    for i in range(len(col_names)):
        df.rename(columns={df.columns[i]: col_names[i]}, inplace=True)

    if "none" in col_names:
        df = df.drop(columns='none')

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
    df = df.dropna()
    df = df.replace("..", np.nan)
    df = df[df['year'] >= 1993]
    
    return df

def _fill_col_CF_den(df, col, last_year):
    df.loc[df['year'] > last_year, col] = df.loc[df['year'] == last_year, col].values[0]
    return df

def _cap_form_fix_den(df):
    first_year = 1993
    last_year = 2019
    sectors = list(df['sector'].unique())
    column = df.columns.tolist()
    column = column[-2]

    for sector in sectors:
        sector_rows = df[df['sector'] == sector]
        
        avg_change = np.mean(sector_rows[sector_rows['year'] >= first_year][column].diff().fillna(0))
        avg_change = int(avg_change)
        val = sector_rows[sector_rows['year'] == first_year][column].values[0]
        
        for year in range((first_year-1), 1965, -1):
            year_row = sector_rows[sector_rows['year'] == year]
            val = val + avg_change
            avg_change = int(avg_change/1.15)
            df.loc[year_row.index, column] = val
    
    df = df.groupby('sector', group_keys=False).apply(_fill_col_CF_den, column, last_year)

    return df

def _rename_frame(df):
    """Takes data frame, reads column names, and renames all columns to standardized names.
    
    Returns: data frame with new column names"""

    old_names = df.columns.tolist()[2:]
    new_names = ["CC", "CF", "FA", "TH", "CE", "VA"]
    df = df.rename(columns=dict(zip(old_names,new_names)))
    
    return df

def _merge_nor_den(df1, df2, df3, df4=pd.DataFrame([])):
    """Takes three data frames, and stack them together from the right on sector and year.
    
    Returns: a data frame with the information from all three."""
    merged_df = df1 if df4.empty else pd.merge(df4, df1, on=['sector', 'year']) 
    merged_df = pd.merge(merged_df, df2, on=['sector', 'year'])
    merged_df = pd.merge(merged_df, df3, on=['sector', 'year'])
    
    return merged_df

def _merge_swe(df1, df2, df3, df4):
    merged_df = pd.merge(df1, df2, on=['sector', 'year'])
    merged_df = pd.merge(merged_df, df3, on=['sector', 'year'])
    merged_df = pd.merge(merged_df, df4, on=['sector', 'year'])

    merged_df = merged_df[["sector", "year", "CC", "CF", "FA", "TH", "CE", "VA"]]

    return merged_df

def clean_and_merge_nor(capital, hours, value_added):
    """Takes three data frames, capital, hours and value_added, and cleans them, then merge them and at the ned rename them.
    
    Returns: the complete data frame, ready to be saved"""
    
    df1 = _clean_data_nor(capital)
    df2 = _clean_data_nor(hours)
    df3 = _clean_data_nor(value_added)

    complete = _merge_nor_den(df1, df2, df3)
    complete = _rename_frame(complete)

    return complete

def clean_and_merge_den(capital, hours, value_added, capital2):
    """Takes three data frames, capital, hours and value_added, and cleans them, then merge them and at the ned rename them.
    
    Returns: the complete data frame, ready to be saved"""
    
    df1 = _clean_data_den(capital)
    df1 = _cap_form_fix_den(df1)

    df2 = _clean_data_den(hours)

    df3 = _clean_data_den(value_added)
    cols = df3.columns.tolist()
    cols[-1], cols[-2] = cols[-2], cols[-1]
    df3 = df3[cols]

    capital2 = capital2.drop(capital2.columns[0:2], axis=1)
    df4 = _clean_data_den(capital2)

    complete = _merge_nor_den(df1, df2, df3, df4)
    remove_first_word = lambda x: ' '.join(x.split()[1:])
    complete['sector'] = complete['sector'].apply(remove_first_word)
    complete = _rename_frame(complete)

    complete = complete.fillna(0)
    complete = complete.drop_duplicates(subset=['sector', 'year'])

    return complete

def clean_and_merge_swe(capital, hours, value_added, capital2, col_names):
    """Takes three data frames, capital, hours and value_added, and cleans them, then merge them and at the ned rename them.
    
    Returns: the complete data frame, ready to be saved"""

    df1 = _clean_data_swe(capital, col_names[0])
    df2 = _clean_data_swe(capital2, col_names[1])
    df3 = _clean_data_swe(hours, col_names[2])
    df4 = _clean_data_swe(value_added, col_names[3])

    complete = _merge_swe(df1, df2, df3, df4)

    remove_first_word = lambda x: ' '.join(x.split()[1:])
    complete['sector'] = complete['sector'].apply(remove_first_word)

    return complete

def replace_sector_names(df, sector_dict):
    """
    Replaces sector names in a pandas DataFrame with new names defined in a sector dictionary.

    Parameters:
    df (pandas.DataFrame): The DataFrame with the "sector" column to be replaced.
    sector_dict (dict): A dictionary with keys representing the old sector names and values representing the new sector names.

    Returns:
    pandas.DataFrame: The modified DataFrame with replaced sector names.
    """
    df["sector"] = df["sector"].apply(lambda x: sector_dict.get(x, x))

    return df

