from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import importlib
from results.spiders.script1 import Script1Spider
from results.spiders.script2 import Script2Spider
from results.spiders.script3 import Script3Spider
from results.spiders.script4 import Script4Spider


def main():
    global spider
    print("1. results")
    print("2. Tech Evaluated")
    print("3. Financial Evaluated")
    print("4. Bid_Awarded")

    spider_name = int(input("Enter the number associated with the spider you want to run: "))
    settings = get_project_settings()
    if spider_name == 1:
        process = CrawlerProcess(settings)
        process.crawl(Script1Spider)
        process.start()
    elif spider_name == 2:
        process = CrawlerProcess(settings)
        process.crawl(Script2Spider)
        process.start()
    elif spider_name == 3:
        process = CrawlerProcess(settings)
        process.crawl(Script3Spider)
        process.start()
    elif spider_name == 4:
        process = CrawlerProcess(settings)
        process.crawl(Script4Spider)
        process.start()


if __name__ == '__main__':
    main()
