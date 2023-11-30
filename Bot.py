import tkinter as tk
import logging
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import random
import time
import threading

def random_delay(min_delay, max_delay):
    delay = random.uniform(min_delay, max_delay)
    time.sleep(delay)


# service = Service(executable_path='C:\booking\booking\chromedriver.exe')
global driver

global DoneIndex
DoneIndex = 0
global pause
pause = True
global alreadyPickList
alreadyPickList = []

def get_all_dates():
    global driver
    datList = []
    date_css_selector = "span[role='button'].vc-day-content.vc-focusable:not(.is-disabled)"
    WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.CSS_SELECTOR, date_css_selector)))
    available_dates = driver.find_elements(By.CSS_SELECTOR, date_css_selector)
    # print(len(available_dates))
    for date in available_dates:
        logging.info(f"date available {date.text}")
        # print(date.text)
        
        datList.append(date.text)
    return datList

def selectOptionCaptchaSolve():
    global driver
    selectOption = "*//select"
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, selectOption))).click()
    # timeList = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "*//select//option")))
    timeList =  WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "*//select//option")))

    timeList[random.randint(1, len(timeList)-1)].click()
    #  solve captcha

    capcthAsolve = "//div[@class='captcha-solver-info' and contains(text(), 'Captcha solved!')]"

    while True:
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, capcthAsolve)))
            # print("captcha solved")
            logging.info("captcha solved")
            button_xpath = "*//button[contains(text(), 'Dalej')]"
            nextButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, button_xpath)))
            driver.execute_script("arguments[0].scrollIntoView();", nextButton)
            nextButton.click()
            break
        except:
            # print("captcha solving.....")
            logging.info("captcha solving.....")


def selectDate():
    global driver
    try:
        rightArrowXpath =  "div[role='button'].vc-arrow.is-right:not(.is-disabled)"
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, rightArrowXpath)))
        rightArrow = driver.find_element(By.CSS_SELECTOR, rightArrowXpath)
        rightArrow.click()
    
        # print("available in next month")
        logging.info("available in next month")
        random_delay(1, 3)
        
    except:
        # print("avilable in current month")
        logging.info("avilable in current month")
        
def selectSlot(avalableSlots,alreadyPickList):
    global pause
    global driver
    for slot in avalableSlots:
        if slot in alreadyPickList:
            # print(f"slot already done slot number =>  { slot }")
            logging.info(f"slot already done slot number =>  { slot }")
            continue
        else:
            driver.find_element(By.XPATH, f"//span[@class='vc-day-content vc-focusable' and text()='{slot}']").click()
            selectOptionCaptchaSolve() #  date slot done
            alreadyPickList.append(slot)
            while True:
                time.sleep(1) 
                if pause == True:
                    logging.info("pause")    
                    # print("pause")
                    continue
                else:
                    break
            run_bot()




def run_bot():
    global driver
    username = user_data_entry.get()
    # Use the retrieved username in chrome_options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(rf'--user-data-dir=C:\\Users\\{username}\\AppData\\Local\\Google\\Chrome\\User Data')
    chrome_options.add_argument(r'--incognito')
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument(r'--user-data-dir=C:\\Users\\Darakhsha Rayen\\AppData\\Local\\Google\\Chrome\\User Data')
    # chrome_options.add_argument(r'--incognito')
    # driver = webdriver.Chrome(options=chrome_options)
    # driver.maximize_window()
    global DoneIndex
    global pause
    global alreadyPickList
    driver.get("https://www.bezkolejki.eu/luwlodz")
    random_delay(2, 4)
    button_xpath = "*//button[contains(text(), 'Dalej')]"
    brak_xpath = "*//h5[contains(text(), 'Brak')]"
    appoinmentLables = "//div[@role='tabpanel'][@id='Operacja2']/div[@class='row']"
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, appoinmentLables)))   
    Alables = driver.find_elements(By.XPATH, appoinmentLables)
    if DoneIndex == 9:
        # print("done all done")
        logging.info("done all done")
        return
    for appointment in range(0,10):
        if appointment<=DoneIndex:
            # print(f"all prevous links done {appointment}")
            logging.info(f"all prevous links done {appointment}")
            continue
        random_delay(2, 4)
        Alables = driver.find_elements(By.XPATH, appoinmentLables)
        logging.info(f"link number {appointment}")
        # print(appointment)
        nextButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, button_xpath)))
        driver.execute_script("arguments[0].scrollIntoView();", nextButton)
        driver.execute_script("arguments[0].scrollIntoView();", Alables[appointment])
        Alables[appointment].click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, button_xpath)))
        # nextButton = driver.find_element(By.XPATH, button_xpath)
        driver.execute_script("arguments[0].scrollIntoView();", nextButton)
        nextButton.click()
        random_delay(2, 4)
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, brak_xpath)))
            appoinment_not_present = driver.find_element(By.XPATH, brak_xpath).text
            # print(appoinment_not_present)
            logging.info(f"No Booking Going Back !  {appoinment_not_present}")
            # print("No Booking Going back")
            DoneIndex = appointment
            driver.find_element(By.XPATH, '*//a/div[@id="step-Operacja2"]').click()
        except:
            # print("Booking available")
            logging.info("Booking available")
            selectDate()  #  date selecting checking for right arrow
            avalableSlots = get_all_dates()  # getting all available slots
            # print(f"Available slots are {avalableSlots}")
            logging.info(f"Available slots are {avalableSlots}")
            if avalableSlots == alreadyPickList:
                # print("all slots done")
                logging.info("all slots done")
                alreadyPickList = []
                DoneIndex = appointment
            selectSlot(avalableSlots,alreadyPickList)


        

        
logging.basicConfig(filename='gui_log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ConsoleRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.insert(tk.END, message)
        self.text_widget.see(tk.END)  # Scroll to the end

def run_action():
    threading.Thread(target=run_bot).start()
    logging.info("Bot started!")
    



def resume_action():
    global pause
    pause = False
    logging.info("Resume button clicked!")


root = tk.Tk()
root.title("Booking automation")

# Set window size
root.geometry("500x600")
user_data_label = tk.Label(root, text="Enter Your Username:")
user_data_label.grid(row=2, column=0, padx=10, pady=5, sticky='w')

user_data_entry = tk.Entry(root, width=50)
user_data_entry.grid(row=2, column=1, padx=10, pady=5, sticky='w')
# Create Text widget for console output
console_text = tk.Text(root, wrap='word', height=30, state=tk.DISABLED)
console_text.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

# Create a Scrollbar for the Text widget
scrollbar = tk.Scrollbar(root, command=console_text.yview)
scrollbar.grid(row=0, column=2, sticky='nsew')
console_text['yscrollcommand'] = scrollbar.set

# Redirect sys.stdout and sys.stderr to the Text widget
console_redirector = ConsoleRedirector(console_text)
sys.stdout = console_redirector
sys.stderr = console_redirector

# Create Run button
run_button = tk.Button(root, text="Run", command=run_action)
run_button.grid(row=1, column=0, padx=10, pady=10)

# Create Resume button
resume_button = tk.Button(root, text="Resume", command=resume_action)
resume_button.grid(row=1, column=1, padx=10, pady=10)

# Center buttons at the bottom
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

root.mainloop()
