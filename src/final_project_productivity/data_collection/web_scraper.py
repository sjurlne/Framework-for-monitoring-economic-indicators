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


def _multiselect_and_show_table_den(driver, element_ids, deselect, labels, assets, prices, run):
    """Takes driver that starts on different pages on the website https://www.ssb.no/en, and saves specified tables from each side
    
    Keyword arguments:
    driver: chrome driver activated on the particular webpage
    element_ids: the different elements on each website
    lables: variable labels that the crawler selects
    default_select: default selected rows in the selection windows

    Returns: nothing, as it only navigates the web crawler.
    """

    nr = 1
    var = f'var{nr}'
    variables = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, var)))
    select = Select(variables)
    for label in labels:
        select.select_by_visible_text(label)
    driver.implicitly_wait(10)

    if assets:
        nr += 1
        var = f'var{nr}'
        select_assets = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, var)))
        select = Select(select_assets)
        select.select_by_visible_text(assets)
        driver.implicitly_wait(10)

    nr += 1
    var = f'var{nr}'
    grouping = f'grouping{nr}'
    sectors = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, grouping)))
    select = Select(sectors)
    select.select_by_visible_text("Select all")
    deselect_sectors = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, var)))
    select = Select(deselect_sectors)
    for e in deselect:
        select.deselect_by_visible_text(e)
    driver.implicitly_wait(10)

    if prices:
        nr += 1
        var = f'var{nr}'
        select_price = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, var)))
        select = Select(select_price)
        for price in prices:
            select.select_by_visible_text(price)
        driver.implicitly_wait(10)

    nr += 1
    grouping = f'grouping{nr}'
    years = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, grouping)))
    select = Select(years)
    select.select_by_visible_text("Select all")

    driver.implicitly_wait(2)

    show_table = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.NAME, element_ids[0])))
    driver.execute_script("arguments[0].click();", show_table)

    driver.implicitly_wait(10)

    pivot = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, element_ids[1])))
    driver.execute_script("arguments[0].click();", pivot)

    driver.implicitly_wait(10)

    if run in [0, 2]:
        pivot = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, element_ids[1])))
        driver.execute_script("arguments[0].click();", pivot)
    
    if run in [2]:
        pivot = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, element_ids[1])))
        driver.execute_script("arguments[0].click();", pivot)

    driver.implicitly_wait(10)

    download = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, element_ids[2])))
    select = Select(download)
    select.select_by_visible_text("Excel (*.xlsx)")

    time.sleep(5)


def scrape_norway(driver, element_ids, variable_names, default_select, SITES_nor):
    """Initiate the scraper on each web site given.
    
    Keyword arguments:
    driver: chrome driver activated on the particular webpage
    element_ids: the different elements on each website
    lables: variable labels that the crawler selects
    default_select: default selected rows in the selection windows
    SITES: websites specified for scraping

    Returns: nothing, as it only initiates the web crawler.
    """
    for _ in range(len(SITES_nor)):
        driver.get(SITES_nor[_])
        _multiselect_and_show_table_nor(driver, element_ids, variable_names[_], default_select[_])
        driver.implicitly_wait(10)
    
    driver.quit()


def scrape_denmark(driver, element_ids_den, default_select_den, variable_names_den, assets_den, prices_den, SITES_den):
    for _ in range((len(SITES_den))):
        driver.get(SITES_den[_])
        _multiselect_and_show_table_den(driver, element_ids_den, default_select_den, variable_names_den[_], assets_den[_], prices_den[_], run=_)
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