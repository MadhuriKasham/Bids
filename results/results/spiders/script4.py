import scrapy
import requests
import json
import psycopg2
import time


class Script4Spider(scrapy.Spider):
    name = "script4"
    allowed_domains = ["bidplus.gem.gov.in"]
    # start_urls = ["https://bidplus.gem.gov.in"]

    cookies = {
        '_ga': 'GA1.3.1331674887.1688295480',
        '_gid': 'GA1.3.1782717885.1689146403',
        'GEMDCPROD': 'NODE2',
        'csrf_gem_cookie': 'ac459d27e6de5001aac3627c6edeecf1',
        'TS0106b57a': '015c77a21caa2b3c9c31661669ac8fec48e7e7b5f1a6efcce313a80d4d094047b47bb19dd8403dbaa421b6236bc3cc3322f9f268628689a0d328e5fa856003a3ae66c049e7',
        '_gat': '1',
        'ci_session': '351f030f21895342f0a32a71c9449a195b08d70b',
        'TS01b34dec': '015c77a21c064b1442d1ae2e7cd4c79e80168eaa11a94352d640ca492ef7b3fd300d4ae2af0e78348cd0cdc24e66767ad26a2cc6e7a9de402295966c6929da93d478b782aa6bd91b56918bdc0858e2ee7c20a0b77b',
        '_ga_MMQ7TYBESB': 'GS1.3.1689177506.2.1.1689178161.47.0.0',
    }

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Cookie': '_ga=GA1.3.1331674887.1688295480; _gid=GA1.3.1782717885.1689146403; GEMDCPROD=NODE2; csrf_gem_cookie=ac459d27e6de5001aac3627c6edeecf1; TS0106b57a=015c77a21caa2b3c9c31661669ac8fec48e7e7b5f1a6efcce313a80d4d094047b47bb19dd8403dbaa421b6236bc3cc3322f9f268628689a0d328e5fa856003a3ae66c049e7; _gat=1; ci_session=351f030f21895342f0a32a71c9449a195b08d70b; TS01b34dec=015c77a21c064b1442d1ae2e7cd4c79e80168eaa11a94352d640ca492ef7b3fd300d4ae2af0e78348cd0cdc24e66767ad26a2cc6e7a9de402295966c6929da93d478b782aa6bd91b56918bdc0858e2ee7c20a0b77b; _ga_MMQ7TYBESB=GS1.3.1689177506.2.1.1689178161.47.0.0',
        'Origin': 'https://bidplus.gem.gov.in',
        'Referer': 'https://bidplus.gem.gov.in/all-bids',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    # Connect to Postgres Database in local machine

    def __init__(self):
        self.con = psycopg2.connect(
            "dbname='bids final' user='postgres' host='localhost' port='5432' password='madhuri123'")
        self.cur = self.con.cursor()
        self.create_table()

    # Create a table

    def create_table(self):
        self.cur.execute(""" CREATE TABLE IF NOT EXISTS Bid_award_data (
                key varchar(300) PRIMARY KEY,
                Bid int,
                Bid_No varchar(300),
                Ra_No varchar(100),
                Items varchar(300),
                Quantity int,
                Department varchar(300),
                Startdate varchar(50),
                Enddate varchar(50),
                Document varchar(200),
                Status varchar(100));""")

    time.sleep(5)

    def start_requests(self):
        print("Crawl Initiated")
        data = {
            'payload': '{"param":{"searchBid":"","searchType":"fullText"},"filter":{"bidStatusType":"bidrastatus",'
                       '"byType":"all","highBidValue":"","byEndDate":{"from":"","to":""},'
                       '"sort":"Bid-End-Date-Latest","byStatus":"bid_awarded"}}',
            'csrf_bd_gem_nk': 'ac459d27e6de5001aac3627c6edeecf1',
        }

        yield scrapy.FormRequest("https://bidplus.gem.gov.in/all-bids-data",
                                 formdata=data,
                                 headers=self.headers,
                                 cookies=self.cookies,
                                 method='POST',
                                 callback=self.parse, )

    time.sleep(3)

    # Parse the json response here

    def parse(self, response):

        json_data = response.json()
        Total = json_data['response']['response']['numFound']
        page_Count = int((Total / 10) + 1)

        json_value = json_data['response']['response']["docs"]
        value = len(json_value)
        for val in range(0, value):
            try:
                Bid = json_value[val]['id']
            except:
                Bid = ''
            try:
                Bid_No = json_value[val]['b_bid_number_parent'][0]
            except:
                Bid_No = ''
            try:
                Ra_No = json_value[val]['b_bid_number'][0]
            except:
                Ra_No = ''
            try:
                Items = json_value[val]['b_category_name'][0]
            except:
                Items = ''
            try:
                Quantity = json_value[val]['b_total_quantity'][0]
            except:
                Quantity = ''
            try:
                Department = json_value[val]['ba_official_details_deptName'][0]
            except:
                Department = ''
            try:
                Startdate = ((json_value[val]['final_start_date_sort'][0]).split('T', 1))[0]
            except:
                Startdate = ''
            try:
                Enddate = ((json_value[val]['final_end_date_sort'][0]).split('T', 1))[0]
            except:
                Enddate = ''
            try:
                Document = f"https://bidplus.gem.gov.in/showbidDocument/{Bid}"
            except:
                Document = ''
            try:
                key = (Bid_No + Ra_No)
            except:
                key = ''

            stat = int(json_value[val]['b_buyer_status'][0])
            if stat == 0:
                Status = 'Not Evaluated'
            elif stat == 1:
                Status = 'Technical Evaluated'
            elif stat == 2:
                Status = 'Financial Evaluated'
            elif stat == 3:
                Status = 'Bid Awarded'
            else:
                Status = ''

            data = {
                'key': key,
                'Bid': Bid,
                'Bid_No': Bid_No,
                'Ra_No': Ra_No,
                'Items': Items,
                'Quantity': Quantity,
                'Department': Department,
                'Startdate': Startdate,
                'Enddate': Enddate,
                'Document': Document,
                'Status': Status
            }
            yield data

            self.cur.execute(
                "INSERT INTO Bid_award_data (key,Bid,Bid_No, Ra_No, Items, Quantity, Department, Startdate, Enddate, "
                "Document, Status) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (key, Bid, Bid_No, Ra_No, Items, Quantity, Department, Startdate, Enddate, Document, Status))

            self.con.commit()

        # Pagination starts here
        # Additional cookies and headers to bypass blockage(403)

        if page_Count > int(1):

            for page in range(2, int(page_Count)):
                print("Page moved to:", page)

                cookies = {
                    '_ga': 'GA1.3.1331674887.1688295480',
                    '_gid': 'GA1.3.1782717885.1689146403',
                    'GEMDCPROD': 'NODE2',
                    'csrf_gem_cookie': '65ca367eb89347daa7e697937b11b487',
                    'ci_session': '8e2d8b3d50e38009182582b220ac5519e3898bd3',
                    'TS0106b57a': '015c77a21c0ee56f3701c89e9f15d8b8a571a7e5b666ae3343262e30dae26715040e7b2ca484d3a7d2e0224d389627da411731c2e91c714fbda8f1ea877cec2d02af7baa78',
                    'TS01b34dec': '015c77a21ccf349a95dda9962965b6b159a0391236a94352d640ca492ef7b3fd300d4ae2af0e78348cd0cdc24e66767ad26a2cc6e73b1fe96c6e75fd2b5a649ed9483221da815b865df133125233b1f0436f03345f',
                    '_gat': '1',
                    '_ga_MMQ7TYBESB': 'GS1.3.1689177506.2.1.1689179149.60.0.0',
                }

                headers = {
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Connection': 'keep-alive',
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    # 'Cookie': '_ga=GA1.3.1331674887.1688295480; _gid=GA1.3.1782717885.1689146403; GEMDCPROD=NODE2; csrf_gem_cookie=65ca367eb89347daa7e697937b11b487; ci_session=8e2d8b3d50e38009182582b220ac5519e3898bd3; TS0106b57a=015c77a21c0ee56f3701c89e9f15d8b8a571a7e5b666ae3343262e30dae26715040e7b2ca484d3a7d2e0224d389627da411731c2e91c714fbda8f1ea877cec2d02af7baa78; TS01b34dec=015c77a21ccf349a95dda9962965b6b159a0391236a94352d640ca492ef7b3fd300d4ae2af0e78348cd0cdc24e66767ad26a2cc6e73b1fe96c6e75fd2b5a649ed9483221da815b865df133125233b1f0436f03345f; _gat=1; _ga_MMQ7TYBESB=GS1.3.1689177506.2.1.1689179149.60.0.0',
                    'Origin': 'https://bidplus.gem.gov.in',
                    'Referer': 'https://bidplus.gem.gov.in/all-bids',
                    'Sec-Fetch-Dest': 'empty',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Site': 'same-origin',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
                    'X-Requested-With': 'XMLHttpRequest',
                    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                }

                data = {
                    'payload': f'%7B%22page%22%3A{page}%2C%22param%22%3A%7B%22searchBid%22%3A%22%22%2C%22searchType%22%3A%22fullText%22%7D%2C%22filter%22%3A%7B%22bidStatusType%22%3A%22bidrastatus%22%2C%22byType%22%3A%22all%22%2C%22highBidValue%22%3A%22%22%2C%22byEndDate%22%3A%7B%22from%22%3A%22%22%2C%22to%22%3A%22%22%7D%2C%22sort%22%3A%22Bid-End-Date-Latest%22%2C%22byStatus%22%3A%22bid_awarded%22%7D%7D',
                    'csrf_bd_gem_nk': '65ca367eb89347daa7e697937b11b487',
                }

                # print(data)
                yield scrapy.FormRequest("https://bidplus.gem.gov.in/all-bids-data",
                                         formdata=data,
                                         headers=headers,
                                         cookies=cookies,
                                         method='POST',
                                         dont_filter=True,
                                         callback=self.parse_page, )

    # each page would be parsed here
    time.sleep(5)

    def parse_page(self, response):

        json_data = response.json()
        # print(json_data)

        json_value = json_data['response']['response']["docs"]

        value = len(json_value)
        for val in range(0, value):
            try:
                Bid = json_value[val]['id']
            except:
                Bid = ''
            try:
                Bid_No = json_value[val]['b_bid_number_parent'][0]
            except:
                Bid_No = ''
            try:
                Ra_No = json_value[val]['b_bid_number'][0]
            except:
                Ra_No = ''
            try:
                Items = json_value[val]['b_category_name'][0]
            except:
                Items = ''
            try:
                Quantity = json_value[val]['b_total_quantity'][0]
            except:
                Quantity = ''
            try:
                Department = json_value[val]['ba_official_details_deptName'][0]
            except:
                Department = ''
            try:
                Startdate = ((json_value[val]['final_start_date_sort'][0]).split('T', 1))[0]
            except:
                Startdate = ''
            try:
                Enddate = ((json_value[val]['final_end_date_sort'][0]).split('T', 1))[0]
            except:
                Enddate = ''
            try:
                Document = f"https://bidplus.gem.gov.in/showbidDocument/{Bid}"
            except:
                Document = ''
            try:
                key = (Bid_No + Ra_No)
            except:
                key = ''

            stat = int(json_value[val]['b_buyer_status'][0])
            if stat == 0:
                Status = 'Not Evaluated'
            elif stat == 1:
                Status = 'Technical Evaluated'
            elif stat == 2:
                Status = 'Financial Evaluated'
            elif stat == 3:
                Status = 'Bid Awarded'
            else:
                Status = ''

            new_data = {
                'key': key,
                'Bid': Bid,
                'Bid_No': Bid_No,
                'Ra_No': Ra_No,
                'Items': Items,
                'Quantity': Quantity,
                'Department': Department,
                'Startdate': Startdate,
                'Enddate': Enddate,
                'Document': Document,
                'Status': Status
            }
            yield new_data

            #     # Pushing data on server postgres
            #
            self.cur.execute(
                "INSERT INTO Bid_award_data (key,Bid,Bid_No, Ra_No, Items, Quantity, Department, Startdate, Enddate, "
                "Document, Status) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (key, Bid, Bid_No, Ra_No, Items, Quantity, Department, Startdate, Enddate, Document, Status))
            self.con.commit()
            # self.con.close()
            #
            # self.cur.close()
