from final_project_productivity.check_internet.check_internet import check_internet_connection_for_selenium, update_check
from final_project_productivity.config import BLD
import pandas as pd
import csv
import pytask

down_speed = 10
up_speed = 1

@pytask.mark.produces(BLD / "python" / "reports" / "last_updated.csv")
def task_last_check(produces):
    """
    Checks if the data has been updated in the last 7 days, and updates a flag in the specified file accordingly.

    Args:
        produces (str): The path to the file where the flag will be stored.
    """
    update_check(produces)

@pytask.mark.depends_on(BLD / "python" / "reports" / "last_updated.csv")
@pytask.mark.produces(BLD / "python" / "reports" / "internet_check.csv")
def task_internet_check(produces, depends_on):
    """
    Checks the internet connection using the `check_internet_connection_for_selenium` function and writes a report
    to a CSV file. The report is used as a condition for running the web scraper.

    Args:
        produces (str): Path to the CSV file where the report will be saved.
    """
    last_update = pd.read_csv(depends_on, header=None, names=None)
    need_update = last_update.iloc[1, 0] == "True"

    if need_update:
        report = check_internet_connection_for_selenium(req_down_speed=down_speed, req_up_speed=up_speed)
        #if report[0][1] == False:
        #    raise LookupError("Internet check did not pass, and project can not complete.")
        with open(produces, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(report)