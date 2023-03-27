from final_project_productivity.data_collection.web_scraper import scrape_norway, scrape_denmark, remove_old_files, rename_new_files, scrape_sweden, success
from final_project_productivity.utilities import read_yaml
from final_project_productivity.config import BLD
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pytask
import os
import pandas as pd

#Path configurations:
DRIVER_PATH = "C:\Program Files (x86)\chromedriver.exe"

current_file_dir = os.path.dirname(os.path.abspath(__file__))
download_dir_nor = os.path.join(current_file_dir, '..', '..', '..', 'bld', 'python', 'data', 'norway')
download_dir_nor = os.path.abspath(download_dir_nor)
download_dir_den = os.path.join(current_file_dir, '..', '..', '..', 'bld', 'python', 'data', 'denmark')
download_dir_den = os.path.abspath(download_dir_den)
download_dir_swe = os.path.join(current_file_dir, '..', '..', '..', 'bld', 'python', 'data', 'sweden')
download_dir_swe = os.path.abspath(download_dir_swe)

specs_dir = os.path.join(current_file_dir, '..')
specs_dir = os.path.abspath(specs_dir)

#Specification for each country
specs = read_yaml(f"{specs_dir}\web_scraping_specs.yml")

SITES_nor = specs['SITES_nor']
element_ids_nor = specs['element_ids_nor']
variable_names_nor = specs['variable_names_nor']
default_select_nor = specs['default_select_nor']
new_names_nor = specs['new_names_nor']

SITES_den = specs['SITES_den']
element_ids_den = specs['element_ids_den']
variable_names_den = specs['variable_names_den']
default_select_den = specs['default_select_den']
assets_den = specs['assets_den']
prices_den = specs['prices_den']
new_names_den = specs['new_names_den']

SITES_swe = specs['SITES_swe']
element_ids_swe = specs['element_ids_swe']
variable_names_swe = specs['variable_names_swe']
sectors_swe = specs['sectors_swe']
prices_swe = specs['prices_swe']
new_names_swe = specs['new_names_swe']

@pytask.mark.depends_on(
    {
        "internet" : BLD / "python" / "reports" / "internet_check.csv",
        "need_update" : BLD / "python" / "reports" / "last_updated.csv"
        },
)
@pytask.mark.produces(
    {
        "capital_nor": BLD / "python" / "data" / "norway" / "capital_norway.xlsx",
        "hours_nor": BLD / "python" / "data" / "norway" / "hours_norway.xlsx",
        "value_added_nor": BLD / "python" / "data" / "norway" / "value_added_norway.xlsx",

        "capital_den": BLD / "python" / "data" / "denmark" / "capital_denmark.xlsx",
        "capital2_den": BLD / "python" / "data" / "denmark" / "capital2_denmark.xlsx",
        "hours_den": BLD / "python" / "data" / "denmark" / "hours_denmark.xlsx",
        "value_added_den": BLD / "python" / "data" / "denmark" / "value_added_denmark.xlsx",

        "capital_swe": BLD / "python" / "data" / "sweden" / "capital_sweden.xlsx",
        "capital2_swe": BLD / "python" / "data" / "sweden" / "capital2_sweden.xlsx",
        "hours_swe": BLD / "python" / "data" / "sweden" / "hours_sweden.xlsx",
        "value_added_swe": BLD / "python" / "data" / "sweden" / "value_added_sweden.xlsx"
    },
)

def task_collect_data(depends_on, produces):
    """
    Initializes the web crawler and collects the relevant data, and puts it in the data folder.

    Args:
        depends_on (dict): A dictionary containing the file paths of the files that this task depends on.
        produces (dict): Not used, as Selenium doe not read the path, but needed for Pytask to work.

    Raises:
        Exception: If the Chrome webdriver cannot be run, or the driver does not complete its scraping.
    """
    internet_status = pd.read_csv(depends_on["internet"], header=None, names=None)
    good_connection = internet_status.iloc[0, 1] == "True"

    last_update = pd.read_csv(depends_on["need_update"], header=None, names=None)
    need_update = last_update.iloc[1, 0] == "True"

    if good_connection and need_update:
        drivers = {
            'nor': (download_dir_nor, element_ids_nor, variable_names_nor, default_select_nor, SITES_nor),
            'den': (download_dir_den, element_ids_den, default_select_den, variable_names_den, assets_den, prices_den, SITES_den),
            'swe': (download_dir_swe, element_ids_swe, sectors_swe, variable_names_swe, prices_swe, SITES_swe)
        }

        driver_errors = []
        for driver_name, driver_args in drivers.items():
            try:
                options = Options()
                options.add_experimental_option("prefs", {"download.default_directory": driver_args[0],
                                                           'download.prompt_for_download': False,
                                                           'download.directory_upgrade': True,
                                                           'safebrowsing.enabled': True})
                options.add_argument('--headless=new')
                options.add_argument('--disable-gpu')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument("--log-level=3")
                options.add_argument("--silent")

                driver = webdriver.Chrome(DRIVER_PATH, options=options)
                remove_old_files(driver_args[0])
                if driver_name == 'nor':
                    scrape_norway(driver, driver_args[1], driver_args[2], driver_args[3], driver_args[4])
                elif driver_name == 'den':
                    scrape_denmark(driver, driver_args[1], driver_args[2], driver_args[3], driver_args[4], driver_args[5], driver_args[6])
                elif driver_name == 'swe':
                    scrape_sweden(driver, driver_args[1], driver_args[2], driver_args[3], driver_args[4], driver_args[5])
                rename_new_files(driver_args[0], eval('new_names_' + driver_name))
            except:
                driver_errors.append(driver_name)
                continue
            finally:
                driver.quit()

        if driver_errors:
            driver_error_str = ', '.join(driver_errors)
            raise Exception("Could not run driver(s): {}. Note that statistical web sites frequently get updated which can lead to variations in website performance.".format(driver_error_str))


        else:
            success(depends_on["need_update"]) 

    else:
        for key, value in produces.items():
            if not os.path.exists(value):
                raise LookupError("Necessary raw data files have not been generated. You might want to check your internet connection, or lower the internet requirements in task_status_and_report.")