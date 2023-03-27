import pandas as pd
from final_project_productivity.compare import combine_sectors
import tempfile

def test_combine_sectors():
    """
    Test the combine_sectors function to ensure it correctly combines data from multiple CSV files
    and returns a new dataframe with the appropriate columns.

    Raises:
        AssertionError: if any of the assertions fail.
    """
    data1 = {'year': [2018, 2019, 2020], 'productivity_sector1': [10, 15, 20]}
    data2 = {'year': [2018, 2019, 2020], 'productivity_sector1': [12, 16, 18]}
    data3 = {'year': [2018, 2019, 2020], 'productivity_sector1': [9, 11, 13]}
    df1 = pd.DataFrame(data1)
    df2 = pd.DataFrame(data2)
    df3 = pd.DataFrame(data3)

    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f1, \
         tempfile.NamedTemporaryFile(mode='w', delete=False) as f2, \
         tempfile.NamedTemporaryFile(mode='w', delete=False) as f3:
        df1.to_csv(f1.name, index=False)
        df2.to_csv(f2.name, index=False)
        df3.to_csv(f3.name, index=False)

    sector_name = 'sector1'
    countries = ['Norway', 'Denmark', 'Sweden']
    combined_df = combine_sectors(f1.name, f2.name, f3.name, sector_name, countries, 'productivity')

    expected_columns = ['year', 'productivity_sector1 Norway', 'productivity_sector1 Denmark', 'productivity_sector1 Sweden']
    assert list(combined_df.columns) == expected_columns, "There is a mismatch in the expected names of columns, and the actual names of columns."

    expected_values = [[2018, 10, 12, 9], [2019, 15, 16, 11], [2020, 20, 18, 13]]
    assert combined_df.values.tolist() == expected_values, "There is a mismatch in the expected values, and the actual values of the data frames."
