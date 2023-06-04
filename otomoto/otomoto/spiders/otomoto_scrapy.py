import scrapy


class Car(scrapy.Item):


    # The car class contains data of interest
    # To keep the order of columns, setting.py is modified (FEED_EXPORT_FIELDS attribute dictates the order)
    price = scrapy.Field()
    prod_year = scrapy.Field()
    mileage = scrapy.Field()
    fuel = scrapy.Field()
    power = scrapy.Field()
    seats_num = scrapy.Field()
    color = scrapy.Field()
    link = scrapy.Field()


class OtomotoSpider(scrapy.Spider):


    # Boolean parameter for limiting the number of scraped offers to 100
    limit_100 = True


    # Keeping count of scraped offers to stop at 100
    counter = 0


    # Name of the scraper
    name = "otomoto"


    # Allowed domain
    allowed_domains = ["otomoto.pl"]


    # Scraping the five pages of offers - each has over 20 offers, so the user can choose whether to go beyond 100
    start_urls = ["https://www.otomoto.pl/osobowe/mercedes-benz/gl-klasa/",
                  "https://www.otomoto.pl/osobowe/mercedes-benz/gl-klasa?page=2",
                  "https://www.otomoto.pl/osobowe/mercedes-benz/gl-klasa?page=3",
                  "https://www.otomoto.pl/osobowe/mercedes-benz/gl-klasa?page=4",
                  "https://www.otomoto.pl/osobowe/mercedes-benz/gl-klasa?page=5"]


    def parse(self, response):


        # The xpath of an offer (data-variant attribute helps distinguish between ads and regular offers)
        xpath = '//main//article[@data-variant="regular"]//h2//@href'
        links = response.xpath(xpath)


        # If limit_100 is set to True, the number of links is limited to 100
        if self.limit_100 == True:
            for l in links:
                if self.counter < 100:
                    self.counter += 1
                    url = response.urljoin(l.extract())
                    yield scrapy.Request(url, callback=self.parse_offer)
                else:
                    break
        else:
            for l in links:
                url = response.urljoin(l.extract())

                # The content of the link is requested with callback to parse_offer that contains instructions for scraping it
                yield scrapy.Request(url, callback=self.parse_offer)           


    def parse_offer(self, response):


        # Creating an object of car class, which attributes will be filled with scraped data
        benz = Car()


        # Price
        price_xpath = '//span[@class = "offer-price__number"]/text()'
        # Only the digits are extracted - because thousands are sometimes seperated by whitespace, they need to be combined
        try:
            benz['price'] = response.xpath(price_xpath).re(r"\d+")[0] + response.xpath(price_xpath).re(r"\d+")[1]
        except:
            try:
                # On the occasion that there is no second element, only the first one is taken
                benz['price'] = response.xpath(price_xpath).re_first(r"\d+")
            except:
                benz['price'] = None


        # Year of production
        year_xpath = '//span[contains(text(), "Rok produkcji")]/following-sibling::div/text()'
        try:
            # Here, strip() is used to get rid of newlines and other whitespace characters that surround the content
            benz['prod_year'] = response.xpath(year_xpath).get().strip()
        except:
            benz['prod_year'] = None


        # Mileage
        mileage_xpath = '//span[contains(text(), "Przebieg")]/following-sibling::div/text()'
        try:
            benz['mileage'] = response.xpath(mileage_xpath).re(r"\d+")[0] + response.xpath(mileage_xpath).re(r"\d+")[1]
        except:
            try:
                benz['mileage'] = response.xpath(mileage_xpath).re_first(r"\d+")
            except:
                benz['mileage'] = None


        #Fuel
        fuel_xpath = '//span[contains(text(), "Rodzaj paliwa")]/following-sibling::div/a/text()'
        try:
            benz['fuel'] = response.xpath(fuel_xpath).get().strip()
        except:
            benz['fuel'] = None


        # Power
        power_xpath = '//span[contains(text(), "Moc")]/following-sibling::div/text()'
        try:
            benz['power'] = response.xpath(power_xpath).re_first(r"\d+")
        except:
            benz['power'] = None


        # Number of seats
        seats_xpath = '//span[contains(text(), "Liczba miejsc")]/following-sibling::div/text()'
        try:
            benz['seats_num'] = response.xpath(seats_xpath).get().strip()
        except:
            benz['seats_num'] = None


        # Color
        color_xpath = '//span[contains(text(), "Kolor")]/following-sibling::div/a/text()'
        try:
            benz['color'] = response.xpath(color_xpath).get().strip()
        except:
            benz['color'] = None


        # Link to the offer
        benz['link'] = response.url


        yield benz


    # Saving the execution time of the spider when closing
    def close(self):

        # Extracting  start and finish time with the crawler.stats attribute
        start = self.crawler.stats.get_value('start_time')
        end = self.crawler.stats.get_value('finish_time')


        with open('running_time.txt', 'w') as f:
            f.write('Running time of Scrapy spider:\n')
            f.write(f"{round((end-start).seconds + (end-start).microseconds/1000000, 2)} seconds")