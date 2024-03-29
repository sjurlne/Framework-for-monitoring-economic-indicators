# EPP-final-project: Productivity Analysis with a Web Crawler Collecting Data From Public Statistical Websites.

[![image](https://img.shields.io/badge/Python-3.11.0-gray)]()
[![image](https://img.shields.io/badge/platform-win32-gray)]()
[![image](https://img.shields.io/badge/ChromeDriver-Chromium-gray)](https://chromedriver.chromium.org/downloads)
[![image](https://img.shields.io/badge/Selenium-4.7.2-green)](https://www.selenium.dev/)
[![image](https://img.shields.io/badge/pytask-0.3.1-green)](https://pytask-dev.readthedocs.io/en/stable/)
[![image](https://img.shields.io/badge/pytest-v7.2.2-green)](https://docs.pytest.org/en/7.2.x/)

Welcome to this repository for the final project of Effective Programming Practices for Economists at the University of Bonn.

*I came up with the idea of making a framework for monitoring economic indicators after my internship at the Norwegian Ministry of Finance, as I saw that economist dealing with several economic indicators, variables, sectors and years collected from external sources, could be voulnerable to human errors. As the collection of new datapoints each months demands that the user remember several statistical settings like variables, sectors and years, they might spend unnecessary time struggling with both remembering which, and inserting it in the correct position. Also continuously updated datasets at most statistical databases (read updated back in time) make it hard to discover which of these change.* 

The best way to take advantage of this project is to clone it. You should follow the steps in order to generate
desired output.

1. Clone the repository: https://github.com/sjurlne/EPP-final-project.git to a desired folder. Navigate to a folder in your powershell (if windows),
    and write  

    ```git clone https://github.com/sjurlne/EPP-final-project.git```  

    and then  

    ```cd .\EPP-final-project\``` 


2. Install and activate environment by writing:

    ```conda env create -f environment.yml```

    ```conda activate productivity```  

    This might take some time.


3. Installing ChromeDriver, and using the web crawler.

    Before running pytask there are a couple of steps that need to be done, in order for selenium (the web crawler package) to run. Make sure to have both [Google Chrome](https://www.google.com/chrome/), [Python](https://www.python.org/downloads/) and [Anaconda](https://www.anaconda.com/products/distribution) installed on your computer.

    ### Step-by-step:

    1. Open this [link](https://chromedriver.chromium.org/downloads). 
    
    2. Check your version of chrome by clicking the three dots in the upper right corner in your Google Chrome.  
        ```Customize and control Google Chrome``` -> ```Help``` -> ```About Google Chrome```  
        You should consider to update if possible, which will make it easier to find the corresponding driver.

    3. Download the corresponding version of the ChromeDriver. This is the version that matches with the first three numbers in both the driver and chrome, e.g. 110.

    4. Locate the zip folder that you just downloaded, open it and copy the file called ```ChromeDriver.exe```.
         
        If you are on a windows computer, paste it such that it corresponds with "C:\Program Files (x86)\chromedriver.exe".  
       
        If you are not on a windows computer, you want to save the location to a known directory, and change the variable   ```DRIVER_PATH``` in line 11 in ```task_data_collection.py```  
        from:  
        ```11 DRIVER_PATH = "C:\Program Files (x86)\chromedriver.exe"```   
        to your known location of the driver.

4. After following all steps above, the last job would be to write ```pytask```  


Note: To secure the download of files, and general stability of the web crawler, there is an internet check, and if your system does not pass the check, the project will not be able to complete. Follow the error messages, and use the report internet_check.csv, to locate the issue.

## Credits

This project was created with [cookiecutter](https://github.com/audreyr/cookiecutter)
and the
econ-project-templates](https://github.com/OpenSourceEconomics/econ-project-templates).
