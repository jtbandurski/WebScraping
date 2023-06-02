import scrapy

class Car(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    generation = scrapy.Field()
    prod_year = scrapy.Field()
    mileage = scrapy.Field()
    fuel = scrapy.Field()
    cubic_capacity = scrapy.Field()
    power = scrapy.Field()
    gearbox = scrapy.Field()
    drive_type = scrapy.Field()
    body_type = scrapy.Field()
    doors_num = scrapy.Field()
    seats_num = scrapy.Field()
    color = scrapy.Field()


class OtomotoSpider(scrapy.Spider):
    name = "otomoto"
    allowed_domains = ["otomoto.pl"]

    start_urls = ["https://www.otomoto.pl/osobowe/mercedes-benz/gl-klasa/"]
                #  "https://www.otomoto.pl/osobowe/mercedes-benz/gl-klasa?page=2"]
                #   "https://www.otomoto.pl/osobowe/mercedes-benz/gl-klasa?page=3",
                #   "https://www.otomoto.pl/osobowe/mercedes-benz/gl-klasa?page=4",
                #   "https://www.otomoto.pl/osobowe/mercedes-benz/gl-klasa?page=5"]


    def parse(self, response):
        xpath = '//main//article//h2//@href'
        links = response.xpath(xpath)
        
        for l in links[:2]:
            url = response.urljoin(l.extract())
            yield scrapy.Request(url, callback=self.parse_offer)

    def parse_offer(self, response):

        benz = Car()

        name_xpath = '//div[@class = "offer-summary"]/span[1]/div/following-sibling::text()'
        benz['name'] = response.xpath(name_xpath).get().strip()

        price_xpath = '//span[@class = "offer-price__number"]/text()'
        benz['price'] = response.xpath(price_xpath).get().strip()

        currency_xpath = '//span[@class = "offer-price__currency"]/text()'
        benz['currency'] = response.xpath(currency_xpath).get().strip()

        gen_xpath = '//span[contains(text(), "Generacja")]/following-sibling::div/a/text()'
        benz['generation'] = response.xpath(gen_xpath).get().strip()

        year_xpath = '//span[contains(text(), "Rok produkcji")]/following-sibling::div/text()'
        benz['prod_year'] = response.xpath(year_xpath).get().strip()
 
        mileage_xpath = '//span[contains(text(), "Przebieg")]/following-sibling::div/text()'
        benz['mileage'] = response.xpath(mileage_xpath).get().strip()

        fuel_xpath = '//span[contains(text(), "Rodzaj paliwa")]/following-sibling::div/a/text()'
        benz['fuel'] = response.xpath(fuel_xpath).get().strip()

        cubic_xpath = '//span[contains(text(), "Pojemność skokowa")]/following-sibling::div/text()'
        benz['cubic_capacity'] = response.xpath(cubic_xpath).get().strip()

        power_xpath = '//span[contains(text(), "Moc")]/following-sibling::div/text()'
        benz['power'] = response.xpath(power_xpath).get().strip()

        gearbox_xpath = '//span[contains(text(), "Skrzynia biegów")]/following-sibling::div/a/text()'
        benz['gearbox'] = response.xpath(gearbox_xpath).get().strip()

        drive_xpath = '//span[contains(text(), "Napęd")]/following-sibling::div/a/text()'
        benz['drive_type'] = response.xpath(drive_xpath).get().strip()

        body_xpath = '//span[contains(text(), "Typ nadwozia")]/following-sibling::div/a/text()'
        benz['body_type'] = response.xpath(body_xpath).get().strip()

        doors_xpath = '//span[contains(text(), "Liczba drzwi")]/following-sibling::div/a/text()'
        benz['doors_num'] = response.xpath(doors_xpath).get().strip()

        seats_xpath = '//span[contains(text(), "Liczba miejsc")]/following-sibling::div/text()'
        benz['seats_num'] = response.xpath(seats_xpath).get().strip()

        color_xpath = '//span[contains(text(), "Kolor")]/following-sibling::div/a/text()'
        benz['color'] = response.xpath(color_xpath).get().strip()

        yield benz

    def close(self, reason):
        start_time = self.crawler.stats.get_value('start_time')
        finish_time = self.crawler.stats.get_value('finish_time')
        print("Total run time: ", finish_time-start_time)



