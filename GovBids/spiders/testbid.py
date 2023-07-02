import scrapy
import requests
import json
import psycopg2
import time


class TestbidSpider(scrapy.Spider):
    name = "testbid"
    allowed_domains = ["bidplus.gem.gov.in"]
    # start_urls = ["//bidplus.gem.gov.in/all-bids-data/"]

    # pass Cookies and Headers to request
    # frequently change 'csrf_bd_gem_nk' in the  parameter data

    cookies = {
        'GEMDCPROD': 'NODE1',
        '_ga': 'GA1.3.1331674887.1688295480',
        '_gid': 'GA1.3.750245447.1688295480',
        'csrf_gem_cookie': '8da4121f289149f45e2c48d550fa6c6b',
        'ci_session': '28af8ad75e11eba7d1410c550b2254aae1617510',
        'TS0106b57a': '015c77a21c3115e48f3115af991c86ad0882160cd978808eed38740764e5e97548e4c987ae739745a7058b3db41123c82c41839128c93d261ada9329f9a86c106817855777',
        'TS01b34dec': '015c77a21cb7504c7293b7b803344726759475f043a94ef00203aab613bcdf29d7e23a681320f339cfbcf1f37b8da1506369c6191dda5f3ff01465d62c7cc4f83266945c300fddde90dc1cdf2a1a44f88905547826',
        '_ga_MMQ7TYBESB': 'GS1.3.1688295480.1.1.1688296335.60.0.0',
    }

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Cookie': 'GEMDCPROD=NODE1; _ga=GA1.3.1331674887.1688295480; _gid=GA1.3.750245447.1688295480; csrf_gem_cookie=8da4121f289149f45e2c48d550fa6c6b; ci_session=28af8ad75e11eba7d1410c550b2254aae1617510; TS0106b57a=015c77a21c3115e48f3115af991c86ad0882160cd978808eed38740764e5e97548e4c987ae739745a7058b3db41123c82c41839128c93d261ada9329f9a86c106817855777; TS01b34dec=015c77a21cb7504c7293b7b803344726759475f043a94ef00203aab613bcdf29d7e23a681320f339cfbcf1f37b8da1506369c6191dda5f3ff01465d62c7cc4f83266945c300fddde90dc1cdf2a1a44f88905547826; _ga_MMQ7TYBESB=GS1.3.1688295480.1.1.1688296335.60.0.0',
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
            self.con = psycopg2.connect("dbname='bids final' user='postgres' host='localhost' port='5432' password='madhuri123'")
            self.cur = self.con.cursor()
            self.create_table()

    # Create a table 

    def create_table(self):
        self.cur.execute(""" CREATE TABLE IF NOT EXISTS bids_data (
            key varchar(300),
            Bid int,
            Bid_No varchar(300),
            Ra_No varchar(100),
            Items varchar(300),
            Quantity int,
            Department varchar(300),
            Startdate date,
            Enddate date,
            Document varchar(200));""")
        
    time.sleep(5)


    # Initial request hit to website

    def start_requests(self):

        print("Crawl Initiated")

        data = {
            'payload': '{"param":{"searchBid":"","searchType":"fullText"},"filter":{"bidStatusType":"ongoing_bids","byType":"all","highBidValue":"","byEndDate":{"from":"","to":""},"sort":"Bid-End-Date-Oldest"}}',
            'csrf_bd_gem_nk': '8da4121f289149f45e2c48d550fa6c6b'
            
        }

        yield scrapy.FormRequest("https://bidplus.gem.gov.in/all-bids-data",
                formdata=data, 
                headers = self.headers, 
                cookies =self.cookies, 
                method='POST',
                callback=self.parse,)
    
    time.sleep(3)

    # Parse the json response here

    def parse(self, response):

        json_data = response.json()
        Total = json_data['response']['response']['numFound']
        page_Count = int((Total/10)+1)
             
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
                Startdate = ((json_value[val]['final_start_date_sort'][0]).split('T',1))[0]
            except:
                Startdate = ''
            try:
                Enddate = ((json_value[val]['final_end_date_sort'][0]).split('T',1))[0]
            except:
                Enddate = ''
            try:
                Document = f"https://bidplus.gem.gov.in/showbidDocument/{Bid}"
            except:
                Document = ''
            try:
                key = (Bid_No+Ra_No)
            except:
                key = ''


            data = {
                'key' : key,
                'Bid' :Bid,
                'Bid_No' : Bid_No,
                'Ra_No' : Ra_No,
                'Items' : Items,
                'Quantity' :Quantity,
                'Department' : Department,
                'Startdate' : Startdate,
                'Enddate' : Enddate,
                'Document' : Document
            }
            yield 
            
            # Push the data onto postgres server

            self.cur.execute("INSERT INTO bids_data (key,Bid,Bid_No, Ra_No, Items, Quantity, Department, Startdate, Enddate, Document) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                            (key, Bid, Bid_No, Ra_No, Items, Quantity, Department, Startdate, Enddate, Document))
            
            
            self.con.commit()

        # Pagination starts here
        # Additional cookies and headers to bypass blockage(403)
        
        if page_Count > int(1):

            for page in range(2, int(page_Count)):

                print("Page moved to:", page)

                cookies = {
                    'GEMDCPROD': 'NODE1',
                    '_ga': 'GA1.3.1331674887.1688295480',
                    '_gid': 'GA1.3.750245447.1688295480',
                    'csrf_gem_cookie': '8da4121f289149f45e2c48d550fa6c6b',
                    'ci_session': '28af8ad75e11eba7d1410c550b2254aae1617510',
                    'TS0106b57a': '015c77a21c3115e48f3115af991c86ad0882160cd978808eed38740764e5e97548e4c987ae739745a7058b3db41123c82c41839128c93d261ada9329f9a86c106817855777',
                    'TS01b34dec': '015c77a21cb7504c7293b7b803344726759475f043a94ef00203aab613bcdf29d7e23a681320f339cfbcf1f37b8da1506369c6191dda5f3ff01465d62c7cc4f83266945c300fddde90dc1cdf2a1a44f88905547826',
                    '_gat': '1',
                    '_ga_MMQ7TYBESB': 'GS1.3.1688295480.1.1.1688296335.60.0.0',
                }

                headers = {
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Connection': 'keep-alive',
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    # 'Cookie': 'GEMDCPROD=NODE1; _ga=GA1.3.1331674887.1688295480; _gid=GA1.3.750245447.1688295480; csrf_gem_cookie=8da4121f289149f45e2c48d550fa6c6b; ci_session=28af8ad75e11eba7d1410c550b2254aae1617510; TS0106b57a=015c77a21c3115e48f3115af991c86ad0882160cd978808eed38740764e5e97548e4c987ae739745a7058b3db41123c82c41839128c93d261ada9329f9a86c106817855777; TS01b34dec=015c77a21cb7504c7293b7b803344726759475f043a94ef00203aab613bcdf29d7e23a681320f339cfbcf1f37b8da1506369c6191dda5f3ff01465d62c7cc4f83266945c300fddde90dc1cdf2a1a44f88905547826; _gat=1; _ga_MMQ7TYBESB=GS1.3.1688295480.1.1.1688296335.60.0.0',
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
                    'payload': f'%7B%22page%22%3A{page}%2C%22param%22%3A%7B%22searchBid%22%3A%22%22%2C%22searchType%22%3A%22fullText%22%7D%2C%22filter%22%3A%7B%22bidStatusType%22%3A%22ongoing_bids%22%2C%22byType%22%3A%22all%22%2C%22highBidValue%22%3A%22%22%2C%22byEndDate%22%3A%7B%22from%22%3A%22%22%2C%22to%22%3A%22%22%7D%2C%22sort%22%3A%22Bid-End-Date-Oldest%22%7D%7D',
                    'csrf_bd_gem_nk': '8da4121f289149f45e2c48d550fa6c6b',
                }
 
                print(data)
                yield scrapy.FormRequest("https://bidplus.gem.gov.in/all-bids-data",
                    formdata=data, 
                    headers = headers, 
                    cookies =cookies, 
                    method='POST', 
                    dont_filter = True,
                    callback=self.parse_page,)
    time.sleep(5)

    # each page would be parsed here
                
    def parse_page(self, response):

        json_data = response.json()
            
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
                Startdate = ((json_value[val]['final_start_date_sort'][0]).split('T',1))[0]
            except:
                Startdate = ''
            try:
                Enddate = ((json_value[val]['final_end_date_sort'][0]).split('T',1))[0]
            except:
                Enddate = ''
            try:
                Document = f"https://bidplus.gem.gov.in/showbidDocument/{Bid}"
            except:
                Document = ''
            try:
                key = (Bid_No+Ra_No)
            except:
                key = ''

            new_data = {
                'key' : key,
                'Bid' :Bid,
                'Bid_No' : Bid_No,
                'Ra_No' : Ra_No,
                'Items' : Items,
                'Quantity' :Quantity,
                'Department' : Department,
                'Startdate' : Startdate,    
                'Enddate' : Enddate,
                'Document' : Document
            }

            # Pushing data on server postgres

            self.cur.execute("INSERT INTO bids_data (key,Bid,Bid_No, Ra_No, Items, Quantity, Department, Startdate, Enddate, Document) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (key,Bid, Bid_No, Ra_No, Items, Quantity, Department, Startdate, Enddate, Document))

            yield new_data
    
            self.con.commit()
    

    # def start_requests(self):
      
            
    #         for  i in range(2, 5):
    #             print("Page move to", i)
   
    #             data = {
    #                 'payload': f'%7B%22page%22%3A{i}%2C%22param%22%3A%7B%22searchBid%22%3A%22%22%2C%22searchType%22%3A%22fullText%22%7D%2C%22filter%22%3A%7B%22bidStatusType%22%3A%22ongoing_bids%22%2C%22byType%22%3A%22all%22%2C%22highBidValue%22%3A%22%22%2C%22byEndDate%22%3A%7B%22from%22%3A%22%22%2C%22to%22%3A%22%22%7D%2C%22sort%22%3A%22Bid-End-Date-Oldest%22%7D%7D',
    #                 'csrf_bd_gem_nk': 'b0e285d1274a1218cbfb093012df88aa',
    #             }
 
    #             print(data)
    #             yield scrapy.FormRequest("https://bidplus.gem.gov.in/all-bids-data",
    #                 formdata=data, 
    #                 headers = self.headers, 
    #                 cookies =self.cookies, 
    #                 method='POST', 
    #                 dont_filter = True,
    #                 callback=self.parse,)
            

    # def parse(self, response):
    #     print(response.text)
