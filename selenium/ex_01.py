from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import getpass
import datetime
import os

# Init:
gecko_path = '../../drivers/geckodriver.exe'
ser = Service(gecko_path)
options = webdriver.firefox.options.Options()
options.headless = False
driver = webdriver.Firefox(options = options, service=ser)

url = 'http://campuswire.com/signin'

# Actual program:
# Send to whom?
send_to="Przemek Kurek"

time.sleep(5)

driver.get(url)

time.sleep(5)
# login
username = driver.find_element(By.XPATH, '//input[@placeholder="Email"]')
my_email = input('Please provide your email:')
username.send_keys(my_email)

time.sleep(1)
# password
password = driver.find_element(By.XPATH, '//input[@placeholder="password"]')
my_pass = getpass.getpass('Please provide your password:')
password.send_keys(my_pass)
# for static interactions small sleeps are enough
time.sleep(1)
# submit
button = driver.find_element(By.XPATH, '//button[@type="submit"]')
button.click()

time.sleep(10)
#click DMs
chat = driver.find_element(By.XPATH, '//*[text()="DMs"]')
chat.click()
time.sleep(10)
# find reciever
reciever = driver.find_element(By.XPATH, f'//h5[text()="{send_to}"]/parent::*')
reciever.click()
time.sleep(10)
# send file through input
paperclip = driver.find_element(By.XPATH, '//i[@class="far fa-paperclip"]/following-sibling::*')
paperclip.send_keys(os.path.abspath(__file__))

time.sleep(10)

# Close browser:
driver.quit()
