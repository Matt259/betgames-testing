import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.common.exceptions import WebDriverException
from termcolor import colored

#Initializes the page and driver on which the tests will occur. 
def initialize_startup(browser_selection):
    try:
        if browser_selection == "1":
            driver = webdriver.Chrome(ChromeDriverManager().install())
                
        elif browser_selection == "2":
            driver = webdriver.Firefox(GeckoDriverManager().install())
                
        elif browser_selection == "3":
            driver = webdriver.Edge(EdgeChromiumDriverManager().install())
                
        driver.get('https://demo.betgames.tv/')
        time.sleep(5)   #Wait for the page to load
        
        iframe = driver.find_element(By.ID, "betgames_iframe")  
        driver.switch_to.frame(iframe)
        
        return driver
    #If the browser selected doesnt exist or gets closed mid init
    except WebDriverException:
        print(colored(f"Failed to start this browser, please make sure the browser isn't closing. Try again.", "red"))
        return None
    except NotADirectoryError:
        print(colored("You do not have this browser installed.", "red"))
        return None
    