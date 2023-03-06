import os
import pytask
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from final_project_productivity.data_collection.web_scraper import scrape_norway, remove_old_files, rename_new_files
from final_project_productivity.config import BLD
from final_project_productivity.utilities import read_yaml

#Specification and Configuration:
current_file_dir = os.path.dirname(os.path.abspath(__file__))
download_dir = os.path.join(current_file_dir, '..', '..', '..', 'bld', 'python', 'data', 'norway')
download_dir = os.path.abspath(download_dir)

specs_dir = os.path.join(current_file_dir, '..', '..', '..')
specs_dir = os.path.abspath(specs_dir)

DRIVER_PATH = "C:\Program Files (x86)\chromedriver.exe"

options = Options()
options.add_experimental_option("prefs", {"download.default_directory": download_dir,
        'download.prompt_for_download': False,
        'download.directory_upgrade': True,
        'safebrowsing.enabled': True})
options.add_argument('--headless=new')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

specs = read_yaml(f"{specs_dir}\web_scraping_specs.yml")
SITES_nor = specs['SITES_nor']
element_ids_nor = specs['element_ids_nor']
variable_names_nor = specs['variable_names_nor']
default_select_nor = specs['default_select_nor']
new_names_nor = specs['new_names_nor']

@pytask.mark.depends_on(BLD / "python" / "reports" / "internet_check.csv")
@pytask.mark.produces(
    {
        "capital_nor": BLD / "python" / "data" / "norway" / "capital_norway.xlsx",
        "hours_nor": BLD / "python" / "data" / "norway" / "hours_norway.xlsx",
        "value_added_nor": BLD / "python" / "data" / "norway" / "value_added_norway.xlsx",
    },
)
def task_collect_data(depends_on, produces):
    """
    Initializes the web crawler and collect the relevant data, 
    and puts it in the data folder.
    """
    with open(depends_on, mode='r') as file:
        reader = csv.reader(file)
        report = list(reader)
        
    is_good_connection = report[0][1] == 'True'
    if is_good_connection:
        try:
            driver = webdriver.Chrome(DRIVER_PATH, options=options)

            remove_old_files(download_dir)
            scrape_norway(driver, element_ids_nor, variable_names_nor, default_select_nor, SITES_nor)
            rename_new_files(download_dir, new_names_nor)

        except:
            raise Exception("Could not fin driver.")