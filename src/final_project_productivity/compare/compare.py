import pandas as pd

def combine_sectors(df1, df2, df3, sector, countries, productivity):
    """ 
    Combine a given sector from three dataframes into a single dataframe with columns for each country.
    
    Args:
        df1 (pd.DataFrame): First country
        df2 (pd.DataFrame): Second country
        df3 (pd.DataFrame): Third country
        sector (str): Name of the sector to extract
        countries (list): List of country names to use as column suffixes
        
    Returns:
        pd.DataFrame: A new dataframe with columns for each country's data for the given sector
    """

    sector = f'{productivity}_{sector}'

    sector_df1 = pd.read_csv(df1)
    sector_df2 = pd.read_csv(df2)
    sector_df3 = pd.read_csv(df3)

    # Extract data for the given sector from each dataframe
    sector_df1 = sector_df1.loc[:, ['year', sector]].rename(columns={sector: f'{sector} {countries[0]}'})
    sector_df2 = sector_df2.loc[:, ['year', sector]].rename(columns={sector: f'{sector} {countries[1]}'})
    sector_df3 = sector_df3.loc[:, ['year', sector]].rename(columns={sector: f'{sector} {countries[2]}'})
    
    # Combine the sector data from each country into a single dataframe
    combined_df = pd.concat([sector_df1, sector_df2, sector_df3], axis=1)

    combined_df = combined_df.loc[:,~combined_df.columns.duplicated()]
    
    return combined_df
