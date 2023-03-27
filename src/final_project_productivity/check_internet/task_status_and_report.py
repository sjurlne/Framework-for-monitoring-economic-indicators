from final_project_productivity.check_internet.check_internet import check_internet_connection_for_selenium, update_check
from final_project_productivity.config import BLD
import csv
import pytask

@pytask.mark.produces(BLD / "python" / "reports" / "internet_check.csv")
def task_internet_check(produces):
    """
    Checks the internet connection using the `check_internet_connection_for_selenium` function and writes a report
    to a CSV file. The report is used as a condition for running the web scraper.

    Args:
        produces (str): Path to the CSV file where the report will be saved.
    """
    report = check_internet_connection_for_selenium(req_down_speed=25, req_up_speed=1)
    with open(produces, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(report)

@pytask.mark.produces(BLD / "python" / "reports" / "last_updated.csv")
def task_last_check(produces):
    """
    Checks if the data has been updated in the last 7 days, and updates a flag in the specified file accordingly.

    Args:
        produces (str): The path to the file where the flag will be stored.
    """
    update_check(produces)