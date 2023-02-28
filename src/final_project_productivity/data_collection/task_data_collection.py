"""task for webscrapper"""
import pytask
from web_scraper.py import

def task_collect_data():
    PATH = "C:\Program Files (x86)\chromedriver.exe"

    download_dir = r"src\final_project_productivity\data\norway"

    options = Options()
    options.add_experimental_option("prefs", {"download.default_directory": download_dir,
        'download.prompt_for_download': False,
        'download.directory_upgrade': True,
        'safebrowsing.enabled': True})
    options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(PATH, options=options)