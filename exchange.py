from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from time import sleep


url = 'https://bank.uz/currency'
browser = Chrome('/home/smthwsmth/Desktop/chromedriver')
browser.get(url)

button = browser.find_element(By.CSS_SELECTOR, '#best_USD > div > div > div.organization-contacts > div.bc-inner-blocks-left > a')  #нажатие кнопки "Все банки"
button.send_keys("\n") #send enter for links, buttons

#browser.execute_script("arguments[0].click();", button)
#the option above is the way to overcome error "Element is not clickable at point (X,Y)"
info = []
button = browser.find_element(By.CLASS_NAME, 'bc-inner-block-left').find_elements(By.CLASS_NAME, 'bc-inner-block-left-texts  ')
for i in button:
    info.append(f"{i.find_element(By.CLASS_NAME, 'medium-text').text.strip()}------{i.find_element(By.CLASS_NAME, 'green-date').text.strip()}")
    
print(info)
sleep(5)

