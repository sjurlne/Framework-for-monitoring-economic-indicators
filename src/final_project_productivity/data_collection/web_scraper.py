"""Functions for web scraping with Selenium"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import time
import os

def _multiselect_and_show_table_nor(driver, element_ids, labels, default_select):
    """Takes driver that starts on different pages on the website https://www.ssb.no/en, and saves specified tables from each side
    
    Keyword arguments:
    driver: chrome driver activated on the particular webpage
    element_ids: the different elements on each website
    lables: variable labels that the crawler selects
    default_select: default selected rows in the selection windows

    Returns: nothing, as it only navigates the web crawler.
    """

    variables = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, element_ids[0])))
    
    select = Select(variables)
    for label in labels:
        select.select_by_visible_text(label)
    if default_select:
        for deselect in default_select:
            select.deselect_by_visible_text(deselect)
    
    driver.implicitly_wait(10)

    select_all_years = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, element_ids[1])))
    driver.execute_script("arguments[0].click();", select_all_years)

    driver.implicitly_wait(10)

    industry_specification = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, element_ids[2])))
    select = Select(industry_specification)
    select.select_by_value("vs__NRNaeringA38NP")

    driver.implicitly_wait(10)

    select_all_industries = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, element_ids[3])))
    driver.execute_script("arguments[0].click();", select_all_industries)

    driver.implicitly_wait(10)

    submit = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, element_ids[4])))
    driver.execute_script("arguments[0].click();", submit)
    
    driver.implicitly_wait(10)

    #pivot = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, element_ids[5])))
    #driver.execute_script("arguments[0].click();", pivot)

    driver.implicitly_wait(10)
    time.sleep(4)

    download = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, element_ids[6])))
    driver.execute_script("arguments[0].click();", download)

    time.sleep(5)

def scrape_norway(driver, element_ids, variable_names, default_select, SITES):
    """Initiate the scraper on each web site given.
    
    Keyword arguments:
    driver: chrome driver activated on the particular webpage
    element_ids: the different elements on each website
    lables: variable labels that the crawler selects
    default_select: default selected rows in the selection windows
    SITES: websites specified for scraping

    Returns: nothing, as it only initiates the web crawler.
    """
    for _ in range(3):
        driver.get(SITES[_])
        _multiselect_and_show_table_nor(driver, element_ids, variable_names[_], default_select[_])
        driver.implicitly_wait(10)
    
    driver.quit()

def remove_old_files(download_dir):
    """Remove old files in the download directory, as selenium ChromeDriver struggles with already existing file names.

    Keyword arguments:
    download_dir: directory specified for download in the selenium options.

    Returns: Nothing"""

    for file_name in os.listdir(download_dir):
        file = download_dir + "\\" + file_name
        if os.path.isfile(file):
            print('Deleting file:', file)
            os.remove(file)

def rename_new_files(download_dir, new_names):
    """Remove old files in a download directory, to have more descriptive names.

    Keyword arguments:
    download_dir: directory specified for download in the selenium options.
    new_names: new names for the files, specified.

    Returns: Nothing"""

    os.chdir(download_dir)
    files = os.listdir(download_dir)
    files = sorted(files, key=os.path.getmtime)
    for _ in range(len(files)):
        os.rename(files[_], new_names[_])