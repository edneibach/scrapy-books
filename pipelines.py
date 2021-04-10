# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface
import re
import requests
import json

class BooksPipeline_EurToUsd:
    """Converts prices in EUR to USD"""
    
    def open_spider(self, spider):
        """Calculates the conversion factor from EUR to USD, live from an API. If the API does not respond, it will use a static value that should provide a good approximation"""

        self.API_KEY = 'HLJ4FF8H879062XF' ### This is a free API key from Alphavantage, which will be used to pull in exchange rates live
        # Usually it's not a very good idea to hard-code API keys, but since it's a free key, it should be harmless for this application
        
        try:
            currency_dict = dict(requests.get(f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=EUR&to_currency=USD&apikey={self.API_KEY}').json())
            self.conversion_factor = round(float(currency_dict['Realtime Currency Exchange Rate']['5. Exchange Rate']),2)
        except:
            self.conversion_factor = 1.20
    
    def process_item(self, item, spider):
        """Extracts the raw price from the string, converts it to float, multiplies by the conversion factor, rounds it to 2 decimal places, adds dollar sign"""

        converted_value = (round(float(re.search("\d+\.\d+", str(item["price"]))[0]) * self.conversion_factor, 2))
        item['price'] = f'${converted_value}'
        return item