
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchWindowException
from termcolor import colored
import sector
import time
from __init__ import initialize_startup

#Allows for browser selection
def browser_selection_prompt():
    while True:
        print("1. Chrome;")
        print("2. Firefox;")
        print("3. Edge;")
        
        browser_input = input("Select the browser(use the numbers on the left) that you want to run the test on: ")
        if browser_input in ("1", "2", "3"):
            return browser_input
        else:
            print(colored("Incorrect input, try again.", "red"))

#Validates whether the selected browser exists
def browser_validation():
    while True:
        browser_selection = browser_selection_prompt()
        driver = initialize_startup(browser_selection)
        if driver is not None:
            return driver
        

def start_prompt():
    test_done = False #Flag whether atleast one test was done.
    test_results = {'Coefficient appliance tests': {'successes': 0, 'fails': 0},
                    'Betslip buttons tests': {'successes': 0, 'fails': 0},
                    'Winnings tests': {'successes': 0, 'fails': 0}}
    
    while True:
        print("-"*60)
        print("1. Test if the sector roulette assigns the proper Coefficient;")
        print("2. Test if the betslip fields buttons work as intended(Numbered buttons should add that much into the amount while the C should clear it);")
        print("3. Test whether the possible win is calculated correctly;")
        print("4. Exit;")
            
        user_input = input("Select the test or exit by the numbers on the left: ")
        print("-"*60)  
        if user_input == "4":
            break
          
        elif user_input in ("1", "3"):
            driver = browser_validation()
            print("Might take a moment.")
            
            try: 
                #Waits till the buttons become clickable
                sector_kof = WebDriverWait(driver, 40).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/main/div[2]/div[1]/div[1]/div[1]/div")))
                sector_kof_text = float(sector_kof.text.split(" ")[1])
                timer = int(driver.find_element(By.CLASS_NAME, "Hjo7b3noUWzyBdAtzMyc").text)
                
                #Waits if the timer is below 5 as it errors out sometimes with low timer 
                if timer < 5:
                    time.sleep(45)
                    print("Will need to wait around 45 seconds for a new timer to come up.")
                #All of the roulette options(buttons)
                sector_buttons = driver.find_elements(By.CLASS_NAME, "RBfdfT0Ix_iKoPjpITfX")
                
                if user_input == "1":
                    test_successes, test_fails = sector.kof_match_test(driver, sector_buttons, sector_kof_text)
                    if test_successes > 0 or test_fails > 0:
                        test_results['Coefficient appliance tests']['successes'] += test_successes
                        test_results['Coefficient appliance tests']['fails'] += test_fails
                        test_done = True
                    
                else:
                    result = sector.check_winnings(driver, sector_buttons, sector_kof_text)
                    if result:
                        test_results['Winnings tests']['successes'] += 1
                        test_done = True
                    elif result == False:
                        test_results['Winnings tests']['fails'] += 1
                        test_done = True
                
                time.sleep(5) 
                driver.quit()
            except (NoSuchWindowException, AttributeError):
                print(colored("Closed the browser while trying to do the test.", "red"))
                
        elif user_input == "2": 

            driver = browser_validation()
            test_successes, test_fails = bet_input_field_prompt(driver)
            if test_successes > 0 or test_fails > 0:
                test_results['Betslip buttons tests']['successes'] += test_successes
                test_results['Betslip buttons tests']['fails'] += test_fails
                test_done = True
            time.sleep(5) 
            driver.quit()
                
        else:
            print(colored("Incorrect input, try again.", "red"))
    
    if test_done:
        print_results(test_results)
        
def print_results(test_results):
    for key in test_results:
        successes = test_results[key]['successes']
        fails = test_results[key]['fails']
        total = successes + fails
        print("-"*40)
        print(f"\n{key} total: {total}")
        print(f"Successes: {successes}")
        print(f"Fails: {fails}")  
        
def bet_input_field_prompt(driver):
    test_successes = 0
    test_fails = 0
    try:
        input_field = driver.find_element(By.ID, "amount-input")
        while True:
            
            #All the buttons within the betslip as well as their text values
            money_buttons = driver.find_elements(By.CLASS_NAME, "bet-slip-amount-button")
            button_values = []

            print("-"*88)
            for index, money_button in enumerate(money_buttons, start=1):
                btn_text = money_button.text
                print(f"{index}. {btn_text};")
                button_values.append(btn_text[1:] if btn_text.startswith("+") else btn_text)    #append all the text values of the buttons
            
            print("8. Back;")
            print("Regarding the C button, a random number will get inserted and then cleared.")
            button_test = input("Which amount button would you like to test? Use the leftest numbers as input options: ")
            print("-"*88)
            
            input_field.send_keys(Keys.CONTROL, "a", Keys.DELETE)   #Clear input field in case of accidental input 
            
            if button_test == "8":
                break
                
            elif button_test in ("1","2","3","4","5","6","7"):   
                if button_test == "7":
                    test_s, test_f = sector.bet_input_field_test(button_test, money_buttons, input_field, value_buttons=False)  
                else:
                    test_s, test_f = sector.bet_input_field_test(button_test, money_buttons, input_field, button_values = button_values)   
                test_successes += test_s
                test_fails +=test_f
                
            else:
                print(colored("Bad input, try again.", "red"))
                
            time.sleep(2)
            
    #Exception if the browser gets closed
    except NoSuchWindowException:
        print(colored("Exiting.", "red"))
    return test_successes, test_fails
        
