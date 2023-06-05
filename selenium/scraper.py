from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import os
from tqdm import tqdm
import pandas as pd

start = time.time()
# Limiting parameter
limit_100 = True
# Init:
gecko_path = 'geckodriver.exe'
ser = Service(gecko_path)
options = webdriver.firefox.options.Options()
# hide firefox window
options.headless = True
driver = webdriver.Firefox(options = options, service=ser)
# limit to 100 links


sites = ["https://www.otomoto.pl/osobowe/mercedes-benz/gl-klasa/",
                 "https://www.otomoto.pl/osobowe/mercedes-benz/gl-klasa?page=2",
                  "https://www.otomoto.pl/osobowe/mercedes-benz/gl-klasa?page=3",
                  "https://www.otomoto.pl/osobowe/mercedes-benz/gl-klasa?page=4",
                  "https://www.otomoto.pl/osobowe/mercedes-benz/gl-klasa?page=5"]
# Actual program:
time.sleep(5)
links_list = []
# flag for breaking outer loop
breakout = False
# Iterate over given sites and locate links to scrape
print("Iterating over given sites: ")
for i in tqdm(range(len(sites))):
    # Go to website
    driver.get(sites[i])
    time.sleep(5)
    try:
        # if cookies pop up accept them
        cookies_button = driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
        cookies_button.click()
        time.sleep(5)
    except:
        # no cookies -> do nothing
        pass
    # find all objects with offers; regular not gallery
    links = driver.find_elements(By.XPATH, '//main//article[@data-variant="regular"]//h2//a')
    for link in links:
        # get all links to offers from WebElement objects
        links_list.append(link.get_attribute('href'))
        # if limit_100 is enabled then stop after reaching 100 links
        if (limit_100 == True) and (len(links_list) == 100):
            breakout = True
            break
    # break outer loop
    if breakout:
            break
    time.sleep(5)
    
# Create output dataframe
df = pd.DataFrame(columns=['price', 'mileage', 'power', 'prod_year', 'seats_num', 'fuel', 'color', 'link'])
# Iterate over offer links
print("Iterating over scraped links: ")
for i in tqdm(range(len(links_list))):
    # go to website
    driver.get(links_list[i])
    time.sleep(6)
    # create new row
    row = []
    # price
    try:
        txt = driver.find_element(By.XPATH, '//span[@class = "offer-price__number"]').get_attribute("innerText")
        # example txt: "139 000 PLN"
        # quite complex but it gets rid of currency string and leaves only price
        row.append(int(''.join([s for s in txt.split() if s.isdigit()])))
    except:
        row.append(None)
    # mileage
    try:
        txt = driver.find_element(By.XPATH, "//span[contains(text(), 'Przebieg')]/following-sibling::div").get_attribute("innerText")
        # quite complex but it gets rid of unit string and leaves only value
        row.append(int(''.join([s for s in txt.split() if s.isdigit()])))
    except:
        row.append(None)
    # power
    try:
        txt = driver.find_element(By.XPATH, '//span[contains(text(), "Moc")]/following-sibling::div').get_attribute("innerText")
        # quite complex but it gets rid of unit string and leaves only value
        row.append(int(''.join([s for s in txt.split() if s.isdigit()])))
    except:
        row.append(None)
    # production year
    try:
        row.append(int(driver.find_element(By.XPATH, '//span[contains(text(), "Rok produkcji")]/following-sibling::div').get_attribute("innerText")))
    except:
        row.append(None)
    # number of seats
    try:
        row.append(int(driver.find_element(By.XPATH, '//span[contains(text(), "Liczba miejsc")]/following-sibling::div').get_attribute("innerText")))
    except:
        row.append(None)
    # fuel
    try:
        row.append(driver.find_element(By.XPATH, '//span[contains(text(), "Rodzaj paliwa")]/following-sibling::div/a').get_attribute("innerText"))
    except:
        row.append(None)
    # color
    try:
        row.append(driver.find_element(By.XPATH, '//span[contains(text(), "Kolor")]/following-sibling::div/a').get_attribute("innerText"))
    except:
        row.append(None)
    # link
    row.append(links_list[i])
    # add new row to df
    df.loc[len(df)] = row

# save as csv
df.to_csv("offers.csv", index=False, header=True)
# Close browser:
driver.quit()
end = time.time()

# save time measurment
with open('running_time.txt', 'w') as f:
    f.write('Running time of Selenium scraper:\n')
    f.write(f"{round(end-start,2)} seconds")