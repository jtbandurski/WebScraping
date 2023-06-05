import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

start = time.time()

# Limiting parameter
limit_100 = True

# URLs to scrape
sites = [
    "https://www.otomoto.pl/osobowe/mercedes-benz/gl-klasa/",
    "https://www.otomoto.pl/osobowe/mercedes-benz/gl-klasa?page=2",
    "https://www.otomoto.pl/osobowe/mercedes-benz/gl-klasa?page=3",
    "https://www.otomoto.pl/osobowe/mercedes-benz/gl-klasa?page=4",
    "https://www.otomoto.pl/osobowe/mercedes-benz/gl-klasa?page=5"
]

# Actual program:
links_list = []

# Iterate over given sites
for site in sites:
    response = requests.get(site)
    soup = BeautifulSoup(response.content, "html.parser")
    
    # if cookies pop up, accept them
    cookies_button = soup.select_one("#onetrust-accept-btn-handler")
    if cookies_button:
        requests.get(cookies_button["href"])
        time.sleep(5)
    
    # find all objects with offers
    links = soup.select('main article[data-variant="regular"] h2 a')
    for link in links:
        # get all links to offers
        links_list.append(link["href"])
        
        # if limit_100 is enabled, stop after reaching 100 links
        if limit_100 and len(links_list) == 100:
            break
    
    # stop iterating if the limit is reached
    if limit_100 and len(links_list) == 100:
        break

# Create output dataframe
df = pd.DataFrame(
    columns=['price', 'mileage', 'power', 'prod_year', 'seats_num', 'fuel', 'color', 'link']
)

# Iterate over offer links
for link in links_list:
    response = requests.get(link)
    soup = BeautifulSoup(response.content, "html.parser")
    
    row = [None] * 8  # Initialize the row with None values
    
    # price
    price_element = soup.select_one("span.offer-price__number")
    if price_element:
        txt = price_element.get_text(strip=True)
        row[0] = int(''.join([s for s in txt.split() if s.isdigit()]))

    # mileage
    mileage_element = soup.select_one("span:-soup-contains('Przebieg') + div")
    if mileage_element:
        txt = mileage_element.get_text(strip=True)
        row[1] = int(''.join([s for s in txt.split() if s.isdigit()]))

    # power
    power_element = soup.select_one("span:-soup-contains('Moc') + div")
    if power_element:
        txt = power_element.get_text(strip=True)
        row[2] = int(''.join([s for s in txt.split() if s.isdigit()]))

    # production year
    prod_year_element = soup.select_one("span:-soup-contains('Rok produkcji') + div")
    if prod_year_element:
        row[3] = int(prod_year_element.get_text(strip=True))

    # number of seats
    seats_num_element = soup.select_one("span:-soup-contains('Liczba miejsc') + div")
    if seats_num_element:
        row[4] = int(seats_num_element.get_text(strip=True))

    # fuel
    fuel_element = soup.select_one("span:-soup-contains('Rodzaj paliwa') + div a")
    if fuel_element:
        row[5] = fuel_element.get_text(strip=True)

    # color
    color_element = soup.select_one("span:-soup-contains('Kolor') + div a")
    if color_element:
        row[6] = color_element.get_text(strip=True)

    # link
    row[7] = link
    
    # add new row to df
    df.loc[len(df)] = row

    time.sleep(5)
    
# save as csv
df.to_csv("offers.csv", index=False, header=True)

end = time.time()

# save time measurement
with open('running_time.txt', 'w') as f:
    f.write('Running time of BeautifulSoup scraper:\n')
    f.write(f"{round(end - start, 2)} seconds")
