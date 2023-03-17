import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None

from_year = 1993

def _clean_data_nor(df):
    """
    Takes raw data from Statistics Norway (ssb.no) as a pandas DataFrame, removes empty columns and rows, sets column names,
    sets sector names for all rows, sorts it after sector and year, and drops rows with missing values.

    Args:
        df (pandas.DataFrame): The raw data to be cleaned.

    Returns:
        pandas.DataFrame: The cleaned data frame.
    """
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
    df = df[df['year'] >= from_year]

    return df

def _clean_data_den(df):
    """
    Takes raw data from dst.dk as a pandas dataframe, removes empty columns and rows, sets column names, sets sector names for all rows,
    fills missing year values with previous year's value, sorts data by sector and year, and drops rows with missing values.

    Args:
        df (pandas.DataFrame): The raw data as a pandas dataframe.

    Returns:
        pandas.DataFrame: The cleaned data as a pandas dataframe.
    """
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
    df = df[df['year'] >= from_year]
    
    return df

def _fill_col_CF_den(df, col, last_year):
    """
    Fills missing values in a column of a DataFrame by copying the last non-null value.

    Args:
        df (pd.DataFrame): The DataFrame to operate on.
        col (str): The name of the column to fill.
        last_year (int): The last year for which there is data in the DataFrame.

    Returns:
        pd.DataFrame: The modified DataFrame with missing values in the specified column filled.
    """
    df.loc[df['year'] > last_year, col] = df.loc[df['year'] == last_year, col].values[0]
    return df

def _cap_form_fix_den(df):
    """
    Fixes the capital formation data in the given DataFrame for the Denmark dataset by filling in missing values 
    from earlier years. This is done by calculating the average yearly change for each sector after the first 
    year of data, and using it to fill in missing values in earlier years. The resulting DataFrame is sorted by 
    sector and year, and missing values after the last year of available data are filled in with the last 
    available value.

    Args:
        df (pandas.DataFrame): The DataFrame containing the raw data.

    Returns:
        pandas.DataFrame: The DataFrame with missing values filled in.
    """
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

def _clean_data_swe(df, col_names):
    """
    Cleans raw data from Statistics Sweden by removing empty rows and columns, setting column names and sector names for all rows,
    dropping NA rows, and replacing '..' values with NaN.

    Args:
        df (pandas.DataFrame): The raw data as a pandas DataFrame.
        col_names (list): A list of column names to assign to the DataFrame.

    Returns:
        pandas.DataFrame: The cleaned DataFrame.
    """
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
    df = df[df['year'] >= from_year]
    
    return df

def _merge_nor_den(df1, df2, df3, df4=pd.DataFrame([])):
    """
    Takes three (or four) data frames, and stack them together from the right on sector and year.
    
    Returns: 
        a data frame with the information from all three.
    """
    merged_df = df1 if df4.empty else pd.merge(df4, df1, on=['sector', 'year']) 
    merged_df = pd.merge(merged_df, df2, on=['sector', 'year'])
    merged_df = pd.merge(merged_df, df3, on=['sector', 'year'])
    
    return merged_df

def _merge_swe(df1, df2, df3, df4):
    """
    Takes four data frames, and stack them together from the right on sector and year.
    
    Returns: 
        a data frame with the information from all four.
    """
    merged_df = pd.merge(df1, df2, on=['sector', 'year'])
    merged_df = pd.merge(merged_df, df3, on=['sector', 'year'])
    merged_df = pd.merge(merged_df, df4, on=['sector', 'year'])
    merged_df = merged_df[["sector", "year", "CC", "CF", "FA", "TH", "CE", "VA"]]

    return merged_df

def _rename_frame(df):
    """
    Renames columns in a given DataFrame with a given order to a standardized set of names.

    Args:
        df (pandas.DataFrame): The input DataFrame to be processed.

    Returns:
        pandas.DataFrame: A new DataFrame with columns renamed to the following standardized names: "CC", "CF", "FA", "TH", "CE", "VA".
    """
    old_names = df.columns.tolist()[2:]
    new_names = ["CC", "CF", "FA", "TH", "CE", "VA"]
    df = df.rename(columns=dict(zip(old_names,new_names)))
    
    return df

def clean_and_merge_nor(capital, hours, value_added):
    """
    Cleans and merges three dataframes containing information on capital, hours, and value added, respectively.
    
    Args:
        capital (str): The path to the Excel file containing information on capital.
        hours (str): The path to the Excel file containing information on hours.
        value_added (str): The path to the Excel file containing information on value added.
    
    Returns:
        pandas.DataFrame: A merged DataFrame with columns renamed to standardized names.
    """
    capital = pd.read_excel(capital)
    hours = pd.read_excel(hours)
    value_added = pd.read_excel(value_added)

    capital = _clean_data_nor(capital)
    hours = _clean_data_nor(hours)
    value_added = _clean_data_nor(value_added)

    complete = _merge_nor_den(capital, hours, value_added)
    complete = _rename_frame(complete)

    return complete

def clean_and_merge_den(capital, capital2, hours, value_added):
    """
    Reads and cleans four data frames from Denmark and merges them into one.

    Args:
        capital (str): File path to the first capital data file.
        capital2 (str): File path to the second capital data file.
        hours (str): File path to the hours data file.
        value_added (str): File path to the value added data file.

    Returns:
        pandas.DataFrame: The merged and cleaned DataFrame with renamed columns and sector names.
    """
    capital = pd.read_excel(capital)
    capital2 = pd.read_excel(capital2)
    hours = pd.read_excel(hours)
    value_added = pd.read_excel(value_added)

    capital = _clean_data_den(capital)
    capital = _cap_form_fix_den(capital)
    hours = _clean_data_den(hours)

    value_added = _clean_data_den(value_added)
    cols = value_added.columns.tolist()
    cols[-1], cols[-2] = cols[-2], cols[-1]
    value_added = value_added[cols]

    capital2 = capital2.drop(capital2.columns[0:2], axis=1)
    capital2 = _clean_data_den(capital2)

    complete = _merge_nor_den(capital, hours, value_added, capital2)
    remove_first_word = lambda x: ' '.join(x.split()[1:])
    complete['sector'] = complete['sector'].apply(remove_first_word)
    complete = _rename_frame(complete)

    complete = complete.fillna(0)
    complete = complete.drop_duplicates(subset=['sector', 'year'])

    return complete

def clean_and_merge_swe(capital, capital2, hours, value_added, col_names):
    """
    Reads and cleans four data frames from Sweden and merges them into one.
    
    Args:
        capital (str): File path to the first capital data file.
        capital2 (str): File path to the second capital data file.
        hours (str): File path to the hours data file.
        value_added (str): File path to the value added data file.
        col_names (list): A list containing four sublists, each specifying the column names to be assigned to 
                          the corresponding DataFrame. The sublists must be ordered as follows: 
                          [capital_col_names, capital2_col_names, hours_col_names, value_added_col_names]
                          
    Returns:
        pandas.DataFrame: The merged and cleaned DataFrame with renamed columns and sector names.
    """
    capital = pd.read_excel(capital)
    capital2 = pd.read_excel(capital2)
    hours = pd.read_excel(hours)
    value_added = pd.read_excel(value_added)

    capital = _clean_data_swe(capital, col_names[0])
    capital2 = _clean_data_swe(capital2, col_names[1])
    hours = _clean_data_swe(hours, col_names[2])
    value_added = _clean_data_swe(value_added, col_names[3])

    complete = _merge_swe(capital, capital2, hours, value_added)
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

