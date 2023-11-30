from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import random
import time
def random_delay(min_delay, max_delay):
    delay = random.uniform(min_delay, max_delay)
    time.sleep(delay)
# user_name = "
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(r'--user-data-dir=C:\\Users\\Darakhsha Rayen\\AppData\\Local\\Google\\Chrome\\User Data')
chrome_options.add_argument(r'--incognito')
# service = Service(executable_path='C:\booking\booking\chromedriver.exe')
global driver
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()
global DoneIndex
DoneIndex = 0
global alreadyPickList
alreadyPickList = []

def get_all_dates():
    datList = []
    date_css_selector = "span[role='button'].vc-day-content.vc-focusable:not(.is-disabled)"
    WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.CSS_SELECTOR, date_css_selector)))
    available_dates = driver.find_elements(By.CSS_SELECTOR, date_css_selector)
    # print(len(available_dates))
    for date in available_dates:
        print(date.text)
        datList.append(date.text)
    return datList

def selectOptionCaptchaSolve():
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
            print("captcha solved")
            button_xpath = "*//button[contains(text(), 'Dalej')]"
            nextButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, button_xpath)))
            driver.execute_script("arguments[0].scrollIntoView();", nextButton)
            nextButton.click()
            break
        except:
            print("captcha solving.....")


def selectDate():
    try:
        rightArrowXpath =  "div[role='button'].vc-arrow.is-right:not(.is-disabled)"
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, rightArrowXpath)))
        rightArrow = driver.find_element(By.CSS_SELECTOR, rightArrowXpath)
        rightArrow.click()
        print("available in next month")
        random_delay(1, 3)
        
    except:
        print("avilable in current month")
        
def selectSlot(avalableSlots,alreadyPickList):
    for slot in avalableSlots:
        if slot in alreadyPickList:
            print(f"slot already done slot number =>  { slot }")
            continue
        else:
            driver.find_element(By.XPATH, f"//span[@class='vc-day-content vc-focusable' and text()='{slot}']").click()
            selectOptionCaptchaSolve() #  date slot done
            alreadyPickList.append(slot) 
            remueBot = input("press enter to continue")
            run_bot()




def run_bot():
    global DoneIndex
    global alreadyPickList
    driver.get("https://www.bezkolejki.eu/luwlodz")
    random_delay(2, 4)
    button_xpath = "*//button[contains(text(), 'Dalej')]"
    brak_xpath = "*//h5[contains(text(), 'Brak')]"
    appoinmentLables = "//div[@role='tabpanel'][@id='Operacja2']/div[@class='row']"
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, appoinmentLables)))   
    Alables = driver.find_elements(By.XPATH, appoinmentLables)
    if DoneIndex == 9:
        print("done all done")
        return
    for appointment in range(0,10):
        if appointment<=DoneIndex:
            print(f"all prevous links done {appointment}")
            continue
        random_delay(2, 4)
        Alables = driver.find_elements(By.XPATH, appoinmentLables)
        print(appointment)
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
            print(appoinment_not_present)
            print("No Booking Going back")
            DoneIndex = appointment
            driver.find_element(By.XPATH, '*//a/div[@id="step-Operacja2"]').click()
        except:
            print("Booking available")
            selectDate()  #  date selecting checking for right arrow
            avalableSlots = get_all_dates()  # getting all available slots
            print(f"Available slots are {avalableSlots}")
            if avalableSlots == alreadyPickList:
                print("all slots done")
                alreadyPickList = []
                DoneIndex = appointment
            selectSlot(avalableSlots,alreadyPickList)

run_bot()
        

        