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

url = '"https://www.otomoto.pl/osobowe/mercedes-benz/gl-klasa/"'

# Actual program:

driver.get(url)