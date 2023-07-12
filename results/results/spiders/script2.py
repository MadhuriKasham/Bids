import scrapy
import requests
import json
import psycopg2
import time


class Script2Spider(scrapy.Spider):
    name = "script2"
    allowed_domains = ["bidplus.gem.gov.in"]
    # start_urls = ["https://bidplus.gem.gov.in"]

    cookies = {
        '_ga': 'GA1.3.1385757445.1688058850',
        '_gid': 'GA1.3.1060043519.1688969697',
        'GEMDCPROD': 'NODE2',
        'ci_session': 'b453a174b278ee4fb0abd2b43cda6c8147761b79',
        'csrf_gem_cookie': '8a6de10acb3bf5a5821490d985151cbf',
        'TS0106b57a': '015c77a21cc7a9916e94286e17d4dbc2780c6e57040bb01b426b3811550dd5778bb13a3bd8a467be1d03551ef8f75be39f0141909a914afbbc5c80da1d73ecbf65bf512e0a',
        'TS01b34dec': '015c77a21cd54a9729319c6e84b7532cacd63d0fd8859bb9ae65013937c191d1134d0d75ecb5d448f6d015129608d2f26ace8d365388908e45e879fe55aa2f9ef8ed4a0f6e0d0f125a3950a079962dcff6de02ef85',
        '_gat': '1',
        '_ga_MMQ7TYBESB': 'GS1.3.1689168566.21.0.1689168566.60.0.0',
    }

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Cookie': '_ga=GA1.3.1385757445.1688058850; _gid=GA1.3.1060043519.1688969697; GEMDCPROD=NODE2; ci_session=b453a174b278ee4fb0abd2b43cda6c8147761b79; csrf_gem_cookie=8a6de10acb3bf5a5821490d985151cbf; TS0106b57a=015c77a21cc7a9916e94286e17d4dbc2780c6e57040bb01b426b3811550dd5778bb13a3bd8a467be1d03551ef8f75be39f0141909a914afbbc5c80da1d73ecbf65bf512e0a; TS01b34dec=015c77a21cd54a9729319c6e84b7532cacd63d0fd8859bb9ae65013937c191d1134d0d75ecb5d448f6d015129608d2f26ace8d365388908e45e879fe55aa2f9ef8ed4a0f6e0d0f125a3950a079962dcff6de02ef85; _gat=1; _ga_MMQ7TYBESB=GS1.3.1689168566.21.0.1689168566.60.0.0',
        'Origin': 'https://bidplus.gem.gov.in',
        'Referer': 'https://bidplus.gem.gov.in/all-bids',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Microsoft Edge";v="114"',
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
        self.cur.execute(""" CREATE TABLE IF NOT EXISTS tech_data (
                key varchar(300),
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
                       '"sort":"Bid-End-Date-Latest","byStatus":"tech_evaluated"}}',
            'csrf_bd_gem_nk': '8a6de10acb3bf5a5821490d985151cbf',
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
                "INSERT INTO tech_data (key,Bid,Bid_No, Ra_No, Items, Quantity, Department, Startdate, Enddate, "
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
                    'GEMDCPROD': 'NODE3',
                    '_gid': 'GA1.3.1782717885.1689146403',
                    'ci_session': '90b40ee52ea74517bed896ad639cd932e773f04d',
                    'csrf_gem_cookie': '9d77def6714fc8118b5b0cfec803e545',
                    'TS0106b57a': '015c77a21c46f6f53169808900f0c39a29a74cab5974846d0357ed6e78f58446803398e285ee62916d7c9625994cf7e845eb26d7cb85ce1b47bb4a71f8f20ace7062eca726',
                    'TS01b34dec': '015c77a21c2eac6b0181146e261756ec120a0d6d7dfb1d1cd77314ad53ac60ce15389813baa98388f123422f4c9174dc857649af8bdba8aa4d17b0651db2f66d6c9b4771b23d73313b4a886524edcac5b9a442d2e3',
                    '_gat': '1',
                    '_ga_MMQ7TYBESB': 'GS1.3.1689172990.4.0.1689172990.60.0.0',
                }

                headers = {
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Connection': 'keep-alive',
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    # 'Cookie': '_ga=GA1.3.1331674887.1688295480; GEMDCPROD=NODE3; _gid=GA1.3.1782717885.1689146403; ci_session=90b40ee52ea74517bed896ad639cd932e773f04d; csrf_gem_cookie=9d77def6714fc8118b5b0cfec803e545; TS0106b57a=015c77a21c46f6f53169808900f0c39a29a74cab5974846d0357ed6e78f58446803398e285ee62916d7c9625994cf7e845eb26d7cb85ce1b47bb4a71f8f20ace7062eca726; TS01b34dec=015c77a21c2eac6b0181146e261756ec120a0d6d7dfb1d1cd77314ad53ac60ce15389813baa98388f123422f4c9174dc857649af8bdba8aa4d17b0651db2f66d6c9b4771b23d73313b4a886524edcac5b9a442d2e3; _gat=1; _ga_MMQ7TYBESB=GS1.3.1689172990.4.0.1689172990.60.0.0',
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
                    'payload': f'%7B%22page%22%3A{page}%2C%22param%22%3A%7B%22searchBid%22%3A%22%22%2C%22searchType%22%3A%22fullText%22%7D%2C%22filter%22%3A%7B%22bidStatusType%22%3A%22bidrastatus%22%2C%22byType%22%3A%22all%22%2C%22highBidValue%22%3A%22%22%2C%22byEndDate%22%3A%7B%22from%22%3A%22%22%2C%22to%22%3A%22%22%7D%2C%22sort%22%3A%22Bid-End-Date-Latest%22%2C%22byStatus%22%3A%22tech_evaluated%22%7D%7D',
                    'csrf_bd_gem_nk': '9d77def6714fc8118b5b0cfec803e545',
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
                "INSERT INTO tech_data (key,Bid,Bid_No, Ra_No, Items, Quantity, Department, Startdate, Enddate, "
                "Document, Status) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (key, Bid, Bid_No, Ra_No, Items, Quantity, Department, Startdate, Enddate, Document, Status))
            self.con.commit()
            # self.con.close()
            #
            # self.cur.close()
