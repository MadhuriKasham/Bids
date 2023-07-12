import scrapy
import requests
import json
import psycopg2
import time


class Script3Spider(scrapy.Spider):
    name = "script3"
    allowed_domains = ["bidplus.gem.gov.in"]
    # start_urls = ["https://bidplus.gem.gov.in"]

    cookies = {
        '_ga': 'GA1.3.1331674887.1688295480',
        'GEMDCPROD': 'NODE3',
        '_gid': 'GA1.3.1782717885.1689146403',
        'csrf_gem_cookie': '9d77def6714fc8118b5b0cfec803e545',
        'ci_session': '03c85f2e1d5e28f8d0fbab2e50577c5ad4d6e256',
        'TS0106b57a': '015c77a21c955471ab7891616069820f6ed9559a64a559b7c1361cb2a2dee5e8c26827fb398005209a54e9d5de77ceec0b8564a03714b3dc46a188cf5909c0dc2a98144c3b',
        'TS01b34dec': '015c77a21c893f5e8e205cfa0629b72a27bd74e198fb1d1cd77314ad53ac60ce15389813baa98388f123422f4c9174dc857649af8bdba8aa4d17b0651db2f66d6c9b4771b2639303ffe3b8f5aa7c28b7e82ed4225e',
        '_gat': '1',
        '_ga_MMQ7TYBESB': 'GS1.3.1689172990.4.1.1689173894.57.0.0',
    }

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://bidplus.gem.gov.in',
        'Referer': 'https://bidplus.gem.gov.in/all-bids',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/114.0.0.0 Safari/537.36',
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
        self.cur.execute(""" CREATE TABLE IF NOT EXISTS fin_data (
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
                       '"sort":"Bid-End-Date-Latest","byStatus":"fin_evaluated"}}',
            'csrf_bd_gem_nk': '9d77def6714fc8118b5b0cfec803e545',
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
                "INSERT INTO fin_data (key,Bid,Bid_No, Ra_No, Items, Quantity, Department, Startdate, Enddate, "
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
                    'csrf_gem_cookie': 'c2ec0cadf2e01129f1fa7d5ed2292f90',
                    'ci_session': '0eda87cea4894c1d3c4891389ca3918601b106d1',
                    'GEMDCPROD': 'NODE2',
                    'TS0106b57a': '015c77a21ca90c13608eed3f9fd947c06c1602f61da94352d640ca492ef7b3fd300d4ae2af38bc8f8ed024b5a454f7039c30c3fd87212eb6fb8b1880b3cdd542eb2d2e2cf2',
                    'TS01b34dec': '015c77a21c7f78c8894c7459846049dbeef30bc771a94352d640ca492ef7b3fd300d4ae2af0e78348cd0cdc24e66767ad26a2cc6e7d5e2888719ad3bf7564ae733ad0a2f4aee832fbd6a8301c54920bb02b97305cd',
                    '_gat': '1',
                    '_ga_MMQ7TYBESB': 'GS1.3.1689174414.1.0.1689174414.60.0.0',
                }

                headers = {
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Connection': 'keep-alive',
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    # 'Cookie': '_ga=GA1.3.1331674887.1688295480; _gid=GA1.3.1782717885.1689146403; csrf_gem_cookie=c2ec0cadf2e01129f1fa7d5ed2292f90; ci_session=0eda87cea4894c1d3c4891389ca3918601b106d1; GEMDCPROD=NODE2; TS0106b57a=015c77a21ca90c13608eed3f9fd947c06c1602f61da94352d640ca492ef7b3fd300d4ae2af38bc8f8ed024b5a454f7039c30c3fd87212eb6fb8b1880b3cdd542eb2d2e2cf2; TS01b34dec=015c77a21c7f78c8894c7459846049dbeef30bc771a94352d640ca492ef7b3fd300d4ae2af0e78348cd0cdc24e66767ad26a2cc6e7d5e2888719ad3bf7564ae733ad0a2f4aee832fbd6a8301c54920bb02b97305cd; _gat=1; _ga_MMQ7TYBESB=GS1.3.1689174414.1.0.1689174414.60.0.0',
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
                    'payload': f'%7B%22page%22%3A{page}%2C%22param%22%3A%7B%22searchBid%22%3A%22%22%2C%22searchType%22%3A%22fullText%22%7D%2C%22filter%22%3A%7B%22bidStatusType%22%3A%22bidrastatus%22%2C%22byType%22%3A%22all%22%2C%22highBidValue%22%3A%22%22%2C%22byEndDate%22%3A%7B%22from%22%3A%22%22%2C%22to%22%3A%22%22%7D%2C%22sort%22%3A%22Bid-End-Date-Latest%22%2C%22byStatus%22%3A%22fin_evaluated%22%7D%7D',
                    'csrf_bd_gem_nk': 'c2ec0cadf2e01129f1fa7d5ed2292f90',
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
                "INSERT INTO fin_data (key,Bid,Bid_No, Ra_No, Items, Quantity, Department, Startdate, Enddate, "
                "Document, Status) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (key, Bid, Bid_No, Ra_No, Items, Quantity, Department, Startdate, Enddate, Document, Status))
            self.con.commit()
            # self.con.close()
            #
            # self.cur.close()

