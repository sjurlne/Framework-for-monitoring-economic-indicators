"""Functions for web scraping with Selenium"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import time
import os

def _multiselect_and_show_table(driver, element_ids, labels, default_select, new_name, download_dir):
    # sourcery skip: extract-duplicate-method

    variables = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, element_ids[0])))
    #First route:
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

    pivot = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, element_ids[5])))
    driver.execute_script("arguments[0].click();", pivot)

    driver.implicitly_wait(10)
    time.sleep(4)

    download = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, element_ids[6])))
    driver.execute_script("arguments[0].click();", download)

    time.sleep(5)


def execute_norway(driver, element_ids, variable_names, default_select, new_names, download_dir, SITES):
    for _ in range(3):
        driver.get(SITES[_])
        _multiselect_and_show_table(driver, element_ids, variable_names[_], default_select[_], new_names[_], download_dir)
        driver.implicitly_wait(10)
    
    driver.quit()

def remove_old_files(download_dir):
    
    for file_name in os.listdir(download_dir):
        file = download_dir + "\\" + file_name
        if os.path.isfile(file):
            print('Deleting file:', file)
            os.remove(file)

def rename_new_files(download_dir, new_names):
    os.chdir(download_dir)
    files = os.listdir(download_dir)
    files = sorted(files, key=os.path.getmtime)
    for _ in range(len(files)):
        os.rename(files[_], new_names[_])