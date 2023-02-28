"""Functions for web scraping with Selenium"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import os

def _multiselect_and_show_table(driver, element_ids, labels, default_select, new_name):

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

    download = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, element_ids[6])))
    driver.execute_script("arguments[0].click();", download)

    time.sleep(10)
    os.chdir(download_dir)
    files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
    newest = files[-1]
    os.rename(newest, new_name)

def execute_norway(driver):
    for _ in range(3):
        driver.get(SITES[_])
        _multiselect_and_show_table(driver, element_ids, variable_names[_], default_select[_], new_names[_])
        time.sleep(5)
        driver.implicitly_wait(10)
    
    driver.quit()