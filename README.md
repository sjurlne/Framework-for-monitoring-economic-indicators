# EPP-final-project: Productivity Analysis with a Web Crawler Collecting Governmental Data
Welcome to this repository for the final project of Effective Programming Practices for Economists at the University of Bonn.

The best way to run this project is to clone it. 

1. Clone the repository: https://github.com/sjurlne/EPP-final-project.git. 
    1.1 Navigate to a folder in your powershell, and write 
    ```git clone https://github.com/sjurlne/EPP-final-project.git```

2. Activate environment by writing: 
    ```conda activate final_project``` 
    This might take some time.

There are two ways to run this project.

#### #1 Ignoring the web crawler.

Simply, by commenting out ```task_collect_data()``` in the file ```task_data_collection.py```, you may write

```pytask```

Into the console.

#### #2 Installing ChromeDriver, and using the web crawler.

Before running pytask there are a couple of steps that need to be done, in order for selenium (the web crawler package) to run. Make sure to have both Google Chrome and Python installed on your computer.

### Step-by-step:

While waiting for this to finish, you can proceed to step 3.

3. Go to https://chromedriver.chromium.org/downloads
    3.1 Check your version of chrome by clicking 
        ```Customize and control Google Chrome``` -> ```Help``` -> ```Àbout Google Chrome```

    3.2 Download the corresponding version of the ChromeDriver.

    3.3 IMPORTANT! Locate the zip folder, open it and copy the ```ChromeDriver.exe```. Locate the file