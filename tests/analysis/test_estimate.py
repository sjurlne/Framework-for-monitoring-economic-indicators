"""Tests for the regression model."""
from final_project_productivity.analysis.estimation import _changes, for_plotting
import numpy as np
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

@pytest.fixture
def data():
    return {
        'year': [2018, 2019, 2020, 2018, 2019, 2020],
        'sector': ['A', 'A', 'A', 'B', 'B', 'B'],
        'col1': [10, 20, 30, 40, 50, 60],
        'col2': [100, 200, 300, 400, 500, 600]
    }
def test_changes(data):
    """
    Test function to check the output of _changes() function.

    Args:
        data (dict): A dictionary with keys 'year', 'sector', 'col1' and 'col2'
        containing values for corresponding columns in a pandas dataframe.

    Tested Conditions:
        Test if the columns of the returned dataframe matches the expected columns.
        Test if the logchange values of the returned dataframe match the expected values.
        Test if the logchange values of the first observation for each sector is NAN.

    Raises:
        AssertionError.
    """
    df = pd.DataFrame(data)

    result = _changes(df)

    expected_cols = ['year', 'sector', 'col1', 'col2', 'logchange_col1', 'logchange_col2']
    assert result.columns.tolist() == expected_cols

    assert np.isclose(result.loc[1, 'logchange_col1'], np.log(20/10)), "There is something wrong with the calculation of logarithm of changes."
    assert np.isclose(result.loc[1, 'logchange_col2'], np.log(200/100)), "There is something wrong with the calculation of logarithm of changes."
    assert np.isclose(result.loc[2, 'logchange_col1'], np.log(30/20)), "There is something wrong with the calculation of logarithm of changes."
    assert np.isclose(result.loc[2, 'logchange_col2'], np.log(300/200)), "There is something wrong with the calculation of logarithm of changes."
    assert np.isclose(result.loc[4, 'logchange_col1'], np.log(50/40)), "There is something wrong with the calculation of logarithm of changes."
    assert np.isclose(result.loc[4, 'logchange_col2'], np.log(500/400)), "There is something wrong with the calculation of logarithm of changes."
    assert np.isclose(result.loc[5, 'logchange_col1'], np.log(60/50)), "There is something wrong with the calculation of logarithm of changes."
    assert np.isclose(result.loc[5, 'logchange_col2'], np.log(600/500)), "There is something wrong with the calculation of logarithm of changes."

    assert pd.isna(result.loc[0, 'logchange_col1']), "Columns expected to be NaN because of new sectors, are not NaN."
    assert pd.isna(result.loc[0, 'logchange_col2']), "Columns expected to be NaN because of new sectors, are not NaN."
    assert pd.isna(result.loc[3, 'logchange_col1']), "Columns expected to be NaN because of new sectors, are not NaN."
    assert pd.isna(result.loc[3, 'logchange_col2']), "Columns expected to be NaN because of new sectors, are not NaN."

@pytest.fixture
def productivity_data():
    data = {
        'year': [2016, 2017, 2018, 2019],
        'sector': ['A', 'A', 'A', 'A'],
        'logchange_LP': [0.05, 0.06, 0.04, 0.03],
        'logchange_TFP': [0.02, 0.03, 0.04, 0.05],
        'level_LP': [100, 105, 110, 115],
        'level_TFP': [100, 102, 106, 111]
    }
    return pd.DataFrame(data)
def test_for_plotting(productivity_data):
    """
    Test the `for_plotting` function to ensure that it correctly transforms the productivity data into a format
    suitable for plotting.

    Args:
        productivity_data (pd.DataFrame): A pandas DataFrame containing productivity data.

    Raises:
        AssertionError.
    """
    expected_output = pd.DataFrame({
        'year': [2016, 2017, 2018, 2019],
        'logchange_LP_A': [0.05, 0.06, 0.04, 0.03],
        'logchange_TFP_A': [0.02, 0.03, 0.04, 0.05],
        'level_LP_A': [100, 105, 110, 115],
        'level_TFP_A': [100, 102, 106, 111]
    })
    expected_output = expected_output.loc[:, ~expected_output.columns.duplicated()]

    output = for_plotting(productivity_data)
    assert_frame_equal(output, expected_output)
