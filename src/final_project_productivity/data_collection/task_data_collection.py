from final_project_productivity.data_collection.web_scraper import scrape_norway, scrape_denmark, remove_old_files, rename_new_files
from final_project_productivity.utilities import read_yaml
from final_project_productivity.config import BLD
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pytask
import os
import pandas as pd

#Path configuration:
DRIVER_PATH = "C:\Program Files (x86)\chromedriver.exe"

current_file_dir = os.path.dirname(os.path.abspath(__file__))
download_dir_nor = os.path.join(current_file_dir, '..', '..', '..', 'bld', 'python', 'data', 'norway')
download_dir_nor = os.path.abspath(download_dir_nor)
download_dir_den = os.path.join(current_file_dir, '..', '..', '..', 'bld', 'python', 'data', 'denmark')
download_dir_den = os.path.abspath(download_dir_den)

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

#Tasks
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
    },
)
def task_collect_data(depends_on, produces):
    """
    Initializes the web crawler and collect the relevant data, 
    and puts it in the data folder.
    """
    internet_status = pd.read_csv(depends_on["internet"], header=None, names=None)
    good_connection = internet_status.iloc[0,1] == "True"

    last_update = pd.read_csv(depends_on["need_update"], header=None, names=None)
    need_update = last_update.iloc[1,0] == "True"
        
    if good_connection and need_update:
        try:
            options = Options()
            options.add_experimental_option("prefs", {"download.default_directory": download_dir_nor,
                    'download.prompt_for_download': False,
                    'download.directory_upgrade': True,
                    'safebrowsing.enabled': True})
            options.add_argument('--headless=new')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')

            driver = webdriver.Chrome(DRIVER_PATH, options=options)
            remove_old_files(download_dir_nor)
            scrape_norway(driver, element_ids_nor, variable_names_nor, default_select_nor, SITES_nor)
            rename_new_files(download_dir_nor, new_names_nor)

            options.add_experimental_option("prefs", {"download.default_directory": download_dir_den})
            driver = webdriver.Chrome(DRIVER_PATH, options=options)
            remove_old_files(download_dir_den)
            scrape_denmark(driver, element_ids_den, default_select_den, variable_names_den, assets_den, prices_den, SITES_den)
            rename_new_files(download_dir_den, new_names_den)

        except:
            raise Exception("Could not run driver.")