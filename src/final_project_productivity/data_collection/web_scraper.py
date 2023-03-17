"""Functions for web scraping with Selenium"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import time
import os

def _multiselect_and_show_table_nor(driver, element_ids, labels, default_select):
    """
    Takes a Chrome webdriver activated on the particular webpage, selects specified variables from a dropdown menu, 
    navigates through different pages, and downloads a CSV file.

    Args:
        driver (webdriver.Chrome): Chrome webdriver activated on the particular webpage.
        element_ids (list): A list of element IDs on the webpage.
        labels (list): A list of variable labels that the crawler selects.
        default_select (list, optional): A list of default selected rows in the selection windows.

    Raises:
    -------
    TimeoutException: If a specific element takes too long to load.
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

    download = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, element_ids[6])))
    driver.execute_script("arguments[0].click();", download)
    time.sleep(5)



def _multiselect_and_show_table_den(driver, element_ids, deselect, labels, assets, prices, run):
    """
    Takes a Selenium WebDriver that navigates to a specific webpage and saves specified tables from each side.

    Args:
        driver: A Selenium WebDriver that navigates to a specific webpage.
        element_ids (list): A list of strings that represent element IDs of different HTML elements.
        deselect (list): A list of strings that represent rows to deselect.
        labels (list): A list of strings that represent variable labels that the crawler selects.
        assets (str or None): A string that represents an asset to select, or None if no asset should be selected.
        prices (list or None): A list of strings that represent prices to select, or None if no prices should be selected.
        run (int): An integer that represents whether to run the pivot table, and if so, how many times to run it.

    Returns:
        None. This function only navigates the web crawler to different pages on the website.
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

def _multiselect_and_show_table_swe(driver, element_ids, sectors, variables, prices):
    if prices:
        price_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, element_ids[0])))
        select = Select(price_box)
        for price in prices:
            select.select_by_visible_text(price)
    driver.implicitly_wait(10)

    sector_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, element_ids[1])))
    select = Select(sector_box)
    for sector in sectors:
        select.select_by_visible_text(sector)
    driver.implicitly_wait(10)

    if len(variables) >= 1:
        variable_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, element_ids[2])))
        select = Select(variable_box)
        for v in variables:
            select.select_by_visible_text(v)
        driver.implicitly_wait(10)

        years = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, element_ids[4])))
        driver.execute_script("arguments[0].click();", years)
        driver.implicitly_wait(10)

    else:

        years = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, element_ids[3])))
        driver.execute_script("arguments[0].click();", years)
        driver.implicitly_wait(10)

    show_table = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, element_ids[5])))
    driver.execute_script("arguments[0].click();", show_table)
    driver.implicitly_wait(10)

    pivot_manual = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, element_ids[6])))
    driver.execute_script("arguments[0].click();", pivot_manual)
    driver.implicitly_wait(10)

    if len(variables) > 2:
        upper_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, element_ids[7])))
        select = Select(upper_box)
        select.select_by_index(1)

        pivot_manual = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, element_ids[8])))
        driver.execute_script("arguments[0].click();", pivot_manual)
        driver.implicitly_wait(10)

        lower_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, element_ids[9])))
        select = Select(lower_box)
        select.select_by_index(0)
        select.deselect_by_index(1)
        driver.implicitly_wait(10)
    
    else:
        lower_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, element_ids[9])))
        select = Select(lower_box)
        select.select_by_index(1)
        driver.implicitly_wait(10)


    pivot_manual = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, element_ids[10])))
    driver.execute_script("arguments[0].click();", pivot_manual)
    driver.implicitly_wait(10)

    pivot_manual = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, element_ids[11])))
    driver.execute_script("arguments[0].click();", pivot_manual)
    driver.implicitly_wait(10)

    save_as = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, element_ids[12])))
    driver.execute_script("arguments[0].click();", save_as)
    driver.implicitly_wait(10)

    excel = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, element_ids[13])))
    driver.execute_script("arguments[0].click();", excel)
    driver.implicitly_wait(10)

    download = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, element_ids[14])))
    driver.execute_script("arguments[0].click();", download)
    driver.implicitly_wait(10)
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
        time.sleep(5)
    
    driver.quit()


def scrape_denmark(driver, element_ids_den, default_select_den, variable_names_den, assets_den, prices_den, SITES_den):
    for _ in range((len(SITES_den))):
        driver.get(SITES_den[_])
        _multiselect_and_show_table_den(driver, element_ids_den, default_select_den, variable_names_den[_], assets_den[_], prices_den[_], run=_)
        time.sleep(5)
        driver.implicitly_wait(10)
    
    driver.quit()

def scrape_sweden(driver, element_ids_swe, sectors_swe, variable_names_swe, prices_swe, SITES_swe):
    for _ in range((len(SITES_swe))):
        driver.get(SITES_swe[_])
        _multiselect_and_show_table_swe(driver, element_ids_swe, sectors_swe, variable_names_swe[_], prices_swe[_])
        time.sleep(5)
        driver.implicitly_wait(10)

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