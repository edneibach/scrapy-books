# scrapy-books
This is a scrapy project built to extract data from books.toscrape.com. It also contains a custom pipeline built to convert prices in EUR to USD, using the latest market quotations pulled from an API.

# How to run it
For starters, you will need scrapy installed. Once you have it, you will need to make a new project using:
scrapy startproject
Once you have the project folder setup in your directory of choice, you can put books.py in the spiders folder, pipelines.py in the main folder (overwriting the original one), and make sure that the pipeline is enabled in settings.py.
Once everything is properly setup, you can type this in the commandline (in the scrapy project folder, else it won't find the spider):
scrapy crawl books_spider -o (YOUR OUTPUT FILENAME HERE).csv
