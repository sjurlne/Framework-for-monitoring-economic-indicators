import speedtest
import socket
import os
import pandas as pd
from datetime import datetime, timedelta

def check_internet_connection_for_selenium(req_down_speed=20, req_up_speed=1 ):
    """Checks the stability and speed of the internet connection, and returns a report about the results.
    
    The function performs three tests to determine the quality of the internet connection:
    
    1. Download and upload speed test using Speedtest.net library.
    2. Pinging Google's website to check the stability of the connection.
    3. Comparing the results of the speed test with the required minimum speeds for running Selenium.
    
    If the connection is stable and the speeds are above the minimum requirements for Selenium, the function returns
    a report indicating that the internet connection is good and the speeds achieved. Otherwise, the function returns
    a report indicating that the internet connection is not good enough to run Selenium and the achieved speeds.
    
    Args:
        req_down_speed (float): Required minimum download speed in Mbps for running Selenium. Default is 25 Mbps.
        req_up_speed (float): Required minimum upload speed in Mbps for running Selenium. Default is 1 Mbps.
    
    Returns:
        list: A list containing a report about the internet connection. The report is a list of sub-lists, where each
              sub-list contains two elements: a string with a description of the result, and the value of the result.
              The first element of the first sub-list indicates whether the internet connection is good or not. The
              second and third sub-lists contain the download and upload speeds achieved, respectively.
    """
    try:
        st = speedtest.Speedtest()
        download_speed = st.download() / 1000000  # convert to Mbps
        upload_speed = st.upload() / 1000000  # convert to Mbps
        print(f"Download speed: {download_speed:.2f} Mbps")
        print(f"Upload speed: {upload_speed:.2f} Mbps")

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect(('www.google.com', 80))
        sock.close()
        print("Internet connection is stable")
        
        if download_speed > req_down_speed and upload_speed > req_up_speed:
            is_good_connection = True
            print("Internet speed is good enough to run Selenium")
        else:
            is_good_connection = False
            print("Internet speed is not good enough to run Selenium")

    except speedtest.ConfigRetrievalError:
        print("Could not retrieve configuration")
        is_good_connection = False

    except speedtest.SpeedtestException:
        print("Could not connect to speedtest.net")
        is_good_connection = False

    except socket.error:
        print("Internet connection is unstable")
        is_good_connection = False
    
    report = [
        ['Internet connection is good', is_good_connection],
        ['Download speed (Mbps)', download_speed],
        ['Upload speed (Mbps)', upload_speed]
    ]

    return report

def update_check(path):
    """
    Update the status of a data file to indicate whether it was updated in the last week or not.

    Parameters:
        path : The path to the report file.

    Produces:
        The function saves the updated status to the data file.
    """
    if os.path.exists(path):
        df = pd.read_csv(path)
        last_update = datetime.strptime(df.iloc[0,1], "%Y-%m-%d")
        one_week_ago = datetime.now() - timedelta(days=7)
        if last_update <= one_week_ago:
            df.iloc[0,0] = True
        else:
            df.iloc[0,0] = False
    else:
        df = pd.DataFrame(data={"update_status":[True,], "last_update":[datetime.now().strftime("%Y-%m-%d"),]})
    df.to_csv(path, index=False)