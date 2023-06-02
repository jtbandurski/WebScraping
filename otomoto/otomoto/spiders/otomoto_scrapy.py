import scrapy
import time

# start = time.timer()
# end = time.timer()

# print(end-start)

class Offer(scrapy.Item):
    link = scrapy.Field()

class Car(scrapy.Item):
    prod_year = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    # name = scrapy.Field()
    # prod_year = scrapy.Field()
    # version = scrapy.Field()
    # generation = scrapy.Field()
    # fuel = scrapy.Field()
    # power = scrapy.Field()
    # gearbox = scrapy.Field()
    # drive_type = scrapy.Field()
    # city_fuel_consump = scrapy.Field()
    # body_type = scrapy.Field()
    # doors_num = scrapy.Field()
    # seats_num = scrapy.Field()
    # color = scrapy.Field()
    # mileage = scrapy.Field()
    # cubic_capacity = scrapy.Field()


class OtomotoSpider(scrapy.Spider):
    name = "otomoto"
    allowed_domains = ["https://www.otomoto.pl/"]

    # start_urls = ["https://www.otomoto.pl/osobowe/mercedes-benz/gl-klasa/",
    #               "https://www.otomoto.pl/osobowe/mercedes-benz/gl-klasa?page=2",
    #               "https://www.otomoto.pl/osobowe/mercedes-benz/gl-klasa?page=3",
    #               "https://www.otomoto.pl/osobowe/mercedes-benz/gl-klasa?page=4",
    #               "https://www.otomoto.pl/osobowe/mercedes-benz/gl-klasa?page=5"]

    # def parse(self, response):
    #     xpath = '//main//article//h2//@href'
    #     selection = response.xpath(xpath)
        
    #     for s in selection:
    #         l = Offer()
    #         l['link'] = s.get()
    #         yield l

    start_urls = ["https://www.otomoto.pl/osobowe/oferta/mercedes-benz-gl-ID6Frmih.html"]

    def parse(self, response):

        benz = Car()

        year_xpath = '//body/div[4]/main/div[1]/div[1]/div[2]/div[1]/div[1]/div[3]/div[1]/ul//span[contains(text(), "Rok produkcji")]/following-sibling::div/text()'
        benz['prod_year'] = response.xpath(year_xpath).get().strip()

        price_xpath = '//span[@class = "offer-price__number"]/text()'
        benz['price'] = response.xpath(price_xpath).get().strip()

        currency_xpath = '//span[@class = "offer-price__currency"]/text()'
        benz['currency'] = response.xpath(currency_xpath).get().strip()


        
        yield benz



