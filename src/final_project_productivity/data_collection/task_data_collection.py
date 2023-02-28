"""task for webscrapper"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from final_project_productivity.data_collection.web_scraper import execute_norway
from final_project_productivity.data_collection.web_scraper import rename_new_files
from final_project_productivity.data_collection.web_scraper import remove_old_files

import pytask #??
##from final_project_productivity.config import SRC DOESNT WORK

PATH = "C:\Program Files (x86)\chromedriver.exe"
#download_dir = r"src\final_project_productivity\data\norway"
download_dir = r"C:\Users\sjurl\OneDrive\Dokumenter\02 - Skole\Effective Programming\FinalProject\final_project_productivity\src\final_project_productivity\data\norway"


SITES = ["https://www.ssb.no/en/statbank/table/09170/", #Value Added
         "https://www.ssb.no/en/statbank/table/09174/", #Hours
         "https://www.ssb.no/en/statbank/table/09181/" #Capital
         ]

element_ids = ["ctl00_ContentPlaceHolderMain_VariableSelector1_VariableSelector1_VariableSelectorValueSelectRepeater_ctl01_VariableValueSelect_VariableValueSelect_ValuesListBox", #Variable Names
               "ctl00_ContentPlaceHolderMain_VariableSelector1_VariableSelector1_VariableSelectorValueSelectRepeater_ctl02_VariableValueSelect_VariableValueSelect_SelectAllButton", #YEARS
               "ctl00_ContentPlaceHolderMain_VariableSelector1_VariableSelector1_VariableSelectorValueSelectRepeater_ctl03_VariableValueSelect_VariableValueSelect_GroupingDropDown", #dropdown industry
               "ctl00_ContentPlaceHolderMain_VariableSelector1_VariableSelector1_VariableSelectorValueSelectRepeater_ctl03_VariableValueSelect_VariableValueSelect_SelectAllButton",
               "ctl00_ContentPlaceHolderMain_VariableSelector1_VariableSelector1_ButtonViewTable", #View Tables
               "ctl00_ctl00_ContentPlaceHolderMain_ImageButtonpivotCCW", #Pivot Table
               "ctl00_ctl00_ContentPlaceHolderMain_ShortcutFileFileTypeExcelX"] #download

variable_names = [["Value added at basic prices. Constant 2015 prices (NOK million)", "Compensation of employees. Current prices (NOK million)"], 
                  ["Total hours worked for employees and self-employed (million workhours)"],
                  ["Fixed assets. Constant 2015 prices (NOK million)", "Gross fixed capital formation. Current prices (NOK million)", "Consumption of fixed capital. Current prices (NOK million)"]
                  ]

default_select = [["Output at basic values. Current prices (NOK million)"],
                  ["Wages and salaries (NOK million)"],
                  []
                  ]

new_names = ["value_added_norway.xlsx", #Value Added
             "hours_norway.xlsx", #Capital Stocks
             "capital_norway.xlsx"
             ]

def task_collect_data():
    """
    Initializes the web crawler and collect the relevant data, 
    and puts it in the data folder.
    """
    options = Options()
    options.add_experimental_option("prefs", {"download.default_directory": download_dir,
        'download.prompt_for_download': False,
        'download.directory_upgrade': True,
        'safebrowsing.enabled': True})
    options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    print("NOTE: Errors might occur to indicate that the web page we are trying to access could not be retrieved due to network issues.")
    print("Typical errors are -failed to fetch- and -Not implemented!-")

    remove_old_files(download_dir)

    driver = webdriver.Chrome(PATH, options=options)
    execute_norway(driver, element_ids, variable_names, default_select, new_names, download_dir, SITES)
    rename_new_files(download_dir, new_names)

