"""Functions for estimating the productivity levels."""
import pandas as pd
import numpy as np

def _changes(df):
    """
    Computes the logarithmic changes of each numerical column in a pandas DataFrame, except for the 'sector' and 'year' columns, 
    and returns the updated DataFrame.

    Parameters:
        df (pandas.DataFrame): The input DataFrame to be processed.

    Returns:
        pandas.DataFrame: The processed DataFrame with additional columns for the logarithmic changes.
    """

    columns = df.columns.tolist()
    columns.remove('year')
    columns.remove('sector')
    change = ['logchange_' + col for col in columns]

    df = df.replace(0, np.nan)
    old = np.seterr(invalid='ignore')

    for i in range(len(columns)):

        df[change[i]] = np.nan # initialize change column to NaN
        df[change[i]] = np.log(df[columns[i]] / df[columns[i]].shift(1))
        df.loc[df['sector'] != df['sector'].shift(1), [change[i]]] = None

    return df

def _level_LP_and_TFP(df_sector, year):
    """
    Calculates the leveled path from the changes in productivity measures labour productivity and total factor productivity for a given sector of a pandas DataFrame.
    
    Args:
        df_sector (pandas.DataFrame): The DataFrame containing data for a given sector.
        year (int): The year from which to start the leveled path calculation.

    Returns:
        pandas.DataFrame: The original DataFrame with two additional columns 'level_LP' and 'level_TFP' representing the leveled path of labour productivity and total factor productivity, respectively.
    """

    years  = list(df_sector['year'].values.astype(int))
    pos = years.index(year)
    before_year = years[:(pos+1)]
    after_year = years[pos:]

    for i in range(1, len(after_year)):
        last_TFP = df_sector.loc[df_sector["year"] == after_year[i-1], 'level_TFP'].values[0]
        change_TFP = df_sector.loc[df_sector["year"] == after_year[i],'logchange_TFP'].values[0].round(3)
        TFP = (last_TFP * change_TFP) + last_TFP

        last_LP = df_sector.loc[df_sector["year"] == after_year[i-1], 'level_LP'].values[0]
        change_LP = df_sector.loc[df_sector["year"] == after_year[i],'logchange_LP'].values[0].round(3)
        LP = (last_LP * change_LP) + last_LP

        df_sector.loc[df_sector["year"] == after_year[i], 'level_TFP'] = TFP
        df_sector.loc[df_sector["year"] == after_year[i], 'level_LP'] = LP

    for i in reversed(range(1, (len(before_year)))):
        last_TFP = df_sector.loc[df_sector["year"] == before_year[i], 'level_TFP'].values[0]
        change_TFP = df_sector.loc[df_sector["year"] == before_year[i-1],'logchange_TFP'].values[0].round(3)
        TFP = last_TFP - (last_TFP * change_TFP)

        last_LP = df_sector.loc[df_sector["year"] == before_year[i], 'level_LP'].values[0]
        change_LP = df_sector.loc[df_sector["year"] == before_year[i-1],'logchange_LP'].values[0].round(3)
        LP = last_LP - (last_LP * change_LP)

        df_sector.loc[df_sector["year"] == before_year[i-1], 'level_TFP'] = TFP
        df_sector.loc[df_sector["year"] == before_year[i-1], 'level_LP'] = LP
    
    return df_sector

def productivity_table(df, ref_year=2000):
    """
    Takes a pandas DataFrame, calculates the logarithmic changes of each numerical column,
    and additional productivity measures including productivity growth in labour productivity (LP) and total factor productivity (TFP),
    and a leveled path of both variables with a reference year set to 100.
    
    Optional keyword arguments:
        ref_year (int): the desired reference year to set as 100 (default: 2000)
    
    Returns:
        pandas DataFrame: the input DataFrame with only the log changes and productivity measures,
        rounded to three decimals.
    """

    df = _changes(df)

    df["CCShare"] = (df["CF"] + df["CC"]) / (df["CF"] + df["CC"]  + df["CE"])
    df["logchange_LP"] = df["logchange_VA"] - df["logchange_TH"]
    df["logchange_TFP"] = (df["logchange_LP"] - (df["CCShare"]*(df["logchange_FA"] - df["logchange_TH"])))

    df = df.iloc[:, [0, 1] + list(range(8, len(df.columns)))]

    df["level_TFP"] = np.nan
    df.loc[df['year'] == ref_year, 'level_TFP'] = 100
    df["level_LP"] = np.nan
    df.loc[df['year'] == ref_year, 'level_LP'] = 100

    df = df.groupby('sector', group_keys=True).apply(_level_LP_and_TFP, year=ref_year).reset_index(drop=True)

    return df.round(3)

def for_plotting(df):
    """
    Takes a data frame and prepares it for plotting by pivoting the data and returning only the relevant columns.

    Args:
        df: A pandas data frame.
        
    Returns:
        A pivoted data frame with columns for log changes in labor productivity and total factor productivity,
        as well as leveled paths for labor productivity and total factor productivity.
    """

    sectors = df['sector'].str.strip().unique()
    dfs = []
    
    for sector in sectors:
        sector_data = df[df['sector'] == sector]
        pivoted = sector_data.pivot(index='year', columns='sector')
        pivoted.columns = ['_'.join(col).strip() for col in pivoted.columns.values]
        result = pivoted[[
            f'logchange_LP_{sector}', 
            f'logchange_TFP_{sector}', 
            f'level_LP_{sector}', 
            f'level_TFP_{sector}'
        ]]
    
        result = result.reset_index()
        dfs.append(result)

    result = pd.concat(dfs, axis=1)
    result = result.loc[:, ~result.columns.duplicated()]
    
    return result

def largest_sectors(df_cleaned, indicator = "VA"):
    """
    Takes a cleaned data frame and an indicator, and returns a data frame with the names of the sectors that have the
    largest values for the chosen indicator.

    Parameters:
        df_cleaned (pd.DataFrame): A cleaned data frame containing sectoral data
        indicator (str): The indicator to use (default is "VA")

    Returns:
        pd.DataFrame: A data frame with the names of the sectors that have the largest values for the chosen indicator, 
        sorted from highest to lowest.
    """

    df_cleaned[indicator] = pd.to_numeric(df_cleaned[indicator], errors='coerce')
    df = df_cleaned[['sector', indicator]]
    max = df.loc[df[indicator].idxmax(), 'sector']
    df_filtered = df[df['sector'] != max]
    df_max = df_filtered.groupby('sector').max()
    top_sectors = df_max.sort_values(indicator, ascending=False).index.tolist()
    top_sectors = pd.DataFrame(top_sectors)

    return top_sectors
