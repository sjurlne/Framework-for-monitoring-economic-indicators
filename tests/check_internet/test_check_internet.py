import pytest
from final_project_productivity.check_internet import update_check
import os
from datetime import datetime, timedelta
import pandas as pd

@pytest.fixture
def temp_path():
    return os.path.dirname(os.path.abspath(__file__)) +'/temp_file.csv'
def test_update_check(temp_path):
    """Test the update_check function to ensure it correctly updates a CSV file with the current date and
    returns True if the file has not been updated in the last week, and False otherwise.

    The function first creates a temporary CSV file and ensures that it exists. It then checks if the file
    has been updated in the last week by reading the first row of the file, which should contain a boolean
    value indicating whether or not the file has been updated recently. If the file has not been updated
    in the last week, the function updates the file with the current date and returns True. Otherwise,
    the function returns False.

    Args:
        temp_path: A string representing the path to the temporary CSV file to be used in testing.

    Raises:
        AssertionError: If any of the assertions fail.
    """
    update_check(temp_path)
    assert os.path.exists(temp_path), f"Expected file {temp_path} to exist"
    df = pd.read_csv(temp_path)
    assert df.iloc[0,0] == True, "The first row of the CSV file should contain 'True', when it should as the folder did not exists, but it did no" 

    last_week = datetime.now() - timedelta(days=7, seconds=1)
    df.iloc[0,1] = last_week.strftime("%Y-%m-%d")
    df.to_csv(temp_path, index=False)
    update_check(temp_path)
    df = pd.read_csv(temp_path)
    assert df.iloc[0,0] == True, "The first row of the CSV file should contain 'True', when it has been updated more than a week ago."

    this_week = datetime.now().strftime("%Y-%m-%d")
    df.iloc[0,1] = this_week
    df.to_csv(temp_path, index=False)
    update_check(temp_path)
    df = pd.read_csv(temp_path)
    assert df.iloc[0,0] == False, "The first row of the CSV file should contain 'False', when it has been updated less than a week ago."

    os.remove(temp_path)