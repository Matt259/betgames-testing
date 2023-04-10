from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchWindowException
from termcolor import colored
import random
import time


def kof_match_test(driver, sector_buttons, sector_kof_text):
    test_successes = 0
    test_fails = 0
    test_index = -1
    ran_out = False #flag to wait for the roulette to be played again in cases where it stops playing mid test
    sector_buttons_txt = driver.find_elements(By.CLASS_NAME, "i5kOCf6aVVpNQgj1FqpS")
    
    print("-"*50)  
    print(f"| Test will run {len(sector_buttons)} times for each unique button. |")
    print("-"*60)
    
    while test_index != 18:
        try:
            #This block checks whether the timer has ran out and if so waits for it to appear
            if ran_out:
                WebDriverWait(driver, 40).until(EC.visibility_of_element_located((By.CLASS_NAME, "Hjo7b3noUWzyBdAtzMyc")))
                ran_out = False
                
            for index in range(len(sector_buttons)):
                if index <= test_index: #Checks for the last ran test.
                    continue
                
                sector_buttons[index].click()
                betslip_kof = driver.find_element(By.XPATH, "/html/body/div/main/div[2]/div[2]/div[1]/div[2]/div/div[2]/div/strong").text
                betslip_kof_text = float(betslip_kof)
                
                if sector_kof_text == betslip_kof_text:
                    
                    if len(sector_buttons_txt[index].text.strip()) == 0:    #Last button is the trophy one so it really doesnt have a test to it, thus I assigned it.
                        print(colored(f"| Button Trophy value equates to Betslips value. {betslip_kof_text} = {sector_kof_text}", "green"))
                    else:
                        print(colored(f"| Button {sector_buttons_txt[index].text} value equates to Betslip value. {betslip_kof_text} = {sector_kof_text}", "green"))
                    test_successes += 1
                    
                else:
                    print(colored(f"Button {sector_buttons_txt[index].text} value does not equate to Betslip value. {betslip_kof_text} != {sector_kof_text}", "red"))
                    test_fails += 1
                    
                time.sleep(2)
                test_index = index
                
        #Exception for when the browser suddenly closes
        except NoSuchWindowException:
            print("-"*60)
            print(colored("Failed to find the browser window. Breaking out of the test.", "red"))
            print("-"*60)
            return 0,0
        #Exception in cases when timer runs out.
        except Exception:
            print(colored("Timer has ran out, wait a moment before the game gets played again.", "yellow"))
            ran_out = True
        
    print("-"*60)
    print(colored(f"| Test batch finished with {test_successes} successes and {test_fails} failures. |", "green"))
    print("-"*57)  
    return test_successes, test_fails

def bet_input_field_test(button_test, money_buttons, input_field, value_buttons = True, button_values = None):
    try:
        test_successes = 0
        test_fails = 0
        print("-"*55)
        print("| The test will run 3 times, meaning 3 button clicks. |") 
            
        if value_buttons:
            print("-"*101) 
                
            for test_index in range(1, 4):
                    money_buttons[int(button_test)-1].click()
                    input_value = float(input_field.get_attribute("value"))
                    button_value = float(button_values[int(button_test)-1])
                        
                    if input_value == button_value*test_index:
                        print(colored(f"| The {test_index} test was a success. Input fields value {input_value} is equal to buttons value {button_value} multiplied by {test_index}. ", "green"))
                        test_successes += 1
                    else:
                        print(colored(f"| The {test_index} test was failed. Input fields value {input_value} is not equal to buttons value {button_value} multiplied by {test_index}. ", "red"))
                        test_fails += 1
                        
                    time.sleep(2)   
            print("-"*101)  
                
        else:
            print("-"*84) 
                
            for test_index in range(4):    
                if test_index > 0:
                    input_post_insert = float(input_field.get_attribute("value"))
                    print(f"| Input field post insert: {input_post_insert} ")
                    money_buttons[int(button_test)-1].click()
                    input_post_clear = float(input_field.get_attribute("value"))
                            
                    if input_post_clear == 0.00:
                        print(colored(f"| The {test_index} test was a success. Input field value({input_post_clear}) after clear butto equates to 0.0 ", "green"))
                        test_successes += 1
                    else:
                        print(colored(f"| The {test_index} test was a failure. Input field value({input_post_clear}) after clear button does not equates to 0.0 ", "red"))
                        test_fails += 1
                    print("-"*84)       
                if test_index == 3:
                        break       
                    
                random_number = random.randint(1, 9)  
                print(f"| The inserted random number: {float(random_number)} ") 
                time.sleep(2)
                input_field.send_keys(Keys.CONTROL, "a", Keys.DELETE)
                input_field.send_keys(str(random_number))
                time.sleep(2)   
                
        print(colored(f"| Test batch finished with {test_successes} successes and {test_fails} failures. |", "green"))
        print("-"*56)  
        
    #Exception for when the browser gets closed
    except NoSuchWindowException:
        print(colored("Failed to find the browser window. Breaking out of the test.", "red"))
        print("-"*84)
        return 0,0
        
    return test_successes, test_fails
        
def check_winnings(driver, sector_buttons, sector_kof_text):
    try:
        input_field = driver.find_element(By.ID, "amount-input")
        
        sector_random_button = random.choice(sector_buttons)
        sector_random_button.click()

        random_number = random.randint(1, 9)  
        input_field.send_keys(Keys.CONTROL, "a", Keys.DELETE)
        input_field.send_keys(str(random_number))

        win_amount = driver.find_element(By.CSS_SELECTOR, '[data-qa="text-tax-possible-win"]').text
        win_amount = float(win_amount.replace("€", ""))
        input_value = float(input_field.get_attribute("value"))
        
        print("-"*58)
        print(f"Win amount: {win_amount}")
        print(f"Coefficient: {sector_kof_text}")
        print(f"Bet money: {input_value}")
        
        if win_amount == input_value*sector_kof_text:
            print(colored(f"Test is a success as {sector_kof_text} * {input_value} = the win amount at {win_amount}.", "green"))
            print("-"*58)
            return True
        else:
            print(colored(f"Test is a failure as {sector_kof_text} * {input_value} is not = to the win amount at {win_amount}.", "red"))
            print("-"*58)
            return False
        
    #Exception for when the browser gets closed
    except NoSuchWindowException:
        print(colored("Failed to find the browser window.", "red"))
        return None   