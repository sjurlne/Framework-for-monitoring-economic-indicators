import numpy as np
import pandas as pd
import pytest
from final_project_productivity.config import TEST_DIR
from final_project_productivity.data_management.clean_data import _clean_data_nor, clean_and_merge_den, _clean_data_swe

@pytest.fixture
def raw_data_swe():
    return pd.DataFrame({
        'none': [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
        'year': [np.nan, np.nan,2009, 2010, 2011, 2012, 2009, 2010, 2011, 2012],
        'sector': [np.nan, np.nan, 'A', 'A', 'A', None, 'B', 'B', None, None],
        'col1': [np.nan, np.nan,'..', '..', 3, 4, '..', 1, 3, 5],
        'col2': [np.nan, np.nan,4, 5, 6, 7, 1, 1, 2, 3]
    })
def test_clean_data_swe(raw_data_swe):
    """
    Test the _clean_data_nor function with sample data.
    """
    col_names = ['none', 'year', 'sector', 'col1', 'col2']
    result = _clean_data_swe(raw_data_swe, col_names)

    expected_cols = ['year', 'sector', 'col1', 'col2']
    assert result.columns.tolist() == expected_cols
    assert len(result) == 8
    assert 'none' not in result.columns.tolist()
    assert result.iloc[-1, 1] == 'B'
    assert result.iloc[3, 1] == 'A'

@pytest.fixture
def raw_data_nor():
    return pd.DataFrame({
        'unnamed1': [None, None, 'A', 'A', None, None, 'B', 'B', None, None],
        'unnamed2': [None, None, 2009, 2010, 2011, 2012, 2009, 2010, 2011, 2012],
        'unnamed3': [None, "col1", 3, 2, 3, 4, 2, 1, 3, 5],
        'unnamed4': [None, "col2", 4, 5, 6, 7, 1, 1, 2, 3]
    })
def test_clean_data_nor(raw_data_nor):
    """
    Test the _clean_data_nor function with sample data.
    """
    expected_output = pd.DataFrame({
        'sector': ['A', 'A', 'A', 'A', 'B', 'B', 'B', 'B'],
        'year': [2009, 2010, 2011, 2012, 2009, 2010, 2011, 2012],
        'col1': [3, 2, 3, 4, 2, 1, 3, 5],
        'col2': [4, 5, 6, 7, 1, 1, 2, 3]
    })

    cleaned_data = _clean_data_nor(raw_data_nor)
    assert cleaned_data.columns.tolist() == expected_output.columns.tolist()
    assert len(cleaned_data) == len(expected_output)
    assert cleaned_data['sector'].tolist() == expected_output['sector'].tolist()

@pytest.fixture
def raw_data_den():
    return pd.DataFrame({
        'unnamed1': [np.nan, np.nan, 'A', np.nan, np.nan, np.nan, 'B', np.nan, np.nan, np.nan],
        'unnamed2': [np.nan, np.nan, 2009, 2010, 2011, 2012, 2009, 2010, 2011, 2012],
        'unnamed5': [np.nan, "col1", 3, 2, 3, 4, 2, 1, 3, 5],
    })
def test_clean_data_den(raw_data_den):
    """
    Test the _clean_data_den function with sample data.
    """
    expected_output = pd.DataFrame({
        'sector': ['A', 'A', 'A', 'A', 'B', 'B', 'B', 'B'],
        'year': [2009, 2010, 2011, 2012, 2009, 2010, 2011, 2012],
        'col1': [3, 2, 3, 4, 2, 1, 3, 5],
        })

    cleaned_data = _clean_data_nor(raw_data_den)
    assert len(cleaned_data.columns.tolist()) == len(expected_output.columns.tolist())
    assert len(cleaned_data) == len(expected_output)
    assert cleaned_data['sector'].tolist() == expected_output['sector'].tolist()