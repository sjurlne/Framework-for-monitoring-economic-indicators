# EPP-final-project: Productivity Analysis with a Web Crawler Collecting Governmental Data
Welcome to this repository for the final project of Effective Programming Practices for Economists at the University of Bonn.

The best way to take advantage of this project is to clone it. You should follow the steps in order to generate
desired output.

1. Clone the repository: https://github.com/sjurlne/EPP-final-project.git. 
    1.1 Navigate to a folder in your powershell, and write 
    ```git clone https://github.com/sjurlne/EPP-final-project.git```

2. Activate environment by writing: 
    ```conda activate final_project``` 
    This might take some time.


3. Installing ChromeDriver, and using the web crawler.

    Before running pytask there are a couple of steps that need to be done, in order for selenium (the web crawler package) to run. Make sure to have both Google Chrome and Python installed on your computer.

    ### Step-by-step:

    1. Go to https://chromedriver.chromium.org/downloads
    
    2. Check your version of chrome by clicking 
        ```Customize and control Google Chrome``` -> ```Help``` -> ```Àbout Google Chrome```

    3. Download the corresponding version of the ChromeDriver.

    4. IMPORTANT! Locate the zip folder, open it and copy the ```ChromeDriver.exe```. If you are on a windows
    computer, locate the file in "C:\Program Files (x86)\chromedriver.exe". If you are not on a windows, you want to save the location to a known directory, and change the variable ```DRIVER_PATH``` in line 11 in ```task_data_collection.py``` from:

    ```11 DRIVER_PATH = "C:\Program Files (x86)\chromedriver.exe"```

    to your known location of the driver.