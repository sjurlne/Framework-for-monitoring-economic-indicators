# EPP-final-project: Productivity Analysis with a Web Crawler Collecting Governmental Data
Welcome to this repository for the final project of Effective Programming Practices for Economists at the University of Bonn.

The best way to take advantage of this project is to clone it. You should follow the steps in order to generate
desired output.

1. Clone the repository: https://github.com/sjurlne/EPP-final-project.git. Navigate to a folder in your powershell,
    and write 
    ```git clone https://github.com/sjurlne/EPP-final-project.git```

2. Activate environment by writing: 
    ```conda activate final_project```.
    This might take some time.


3. Installing ChromeDriver, and using the web crawler.

    Before running pytask there are a couple of steps that need to be done, in order for selenium (the web crawler package) to run. Make sure to have both [Google Chrome](https://www.google.com/chrome/) and [Python](https://www.python.org/downloads/) installed on your computer.

    ### Step-by-step:

    1. Open this [link](https://chromedriver.chromium.org/downloads). 
    
    2. Check your version of chrome by clicking the three dots in the upper right corner in your Google Chrome.  
        ```Customize and control Google Chrome``` -> ```Help``` -> ```Àbout Google Chrome```  

    3. Download the corresponding version of the ChromeDriver.

    4. Locate the zip folder that you just donwlaoded, open it and copy the file called ```ChromeDriver.exe```.   
    If you are on a windows computer, paste it such that it corresponds with "C:\Program Files (x86)\chromedriver.exe".   
    If you are not on a windows computer, you want to save the location to a known directory, and change the variable   ```DRIVER_PATH``` in line 11 in ```task_data_collection.py``` from:  
    ```11 DRIVER_PATH = "C:\Program Files (x86)\chromedriver.exe"```   
    to your known location of the driver.

4. After following all steps above, the last job would be to write ```pytask```  