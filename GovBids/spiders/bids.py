import scrapy
import requests
import json
import psycopg2
from GovBids.items import BidItem



class BidsSpider(scrapy.Spider):
    name = 'bids'
    allowed_domains = ['bidplus.gem.gov.in/all-bids-data/']
    # start_urls = ['http://https://bidplus.gem.gov.in/all-bids-data/']


    cookies = {
        '_ga': 'GA1.3.1385757445.1688058850',
        '_gid': 'GA1.3.1613192119.1688058850',
        'csrf_gem_cookie': 'b0c2b11300c56160cba46ff314647001',
        'ci_session': '5407140729cb6c162f76a92e2dbcbf4c88fbe4dc',
        'GEMDCPROD': 'NODE2',
        'TS0106b57a': '015c77a21cfc0ce1ec28b764c46be1a8324cdb3441fdb85b600efbb049ee234fe0d2552398a6f60aa1f855a3a1ca58928f95b4963fa964585ed791d4e43e7fd8945ebd923f',
        'TS01b34dec': '015c77a21c97a18fc78cb68e0b246a2f811e2f72bafdb85b600efbb049ee234fe0d255239825cb06fede1704c2a355ca2192bc53274fef974425bbb6b518c39ac88e9b7ea6429506a1b7f46cef8a0eaaccea23e7e6',
        '_gat': '1',
        '_ga_MMQ7TYBESB': 'GS1.3.1688101181.2.0.1688101181.60.0.0',
    }
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Cookie': '_ga=GA1.3.1385757445.1688058850; _gid=GA1.3.1613192119.1688058850; csrf_gem_cookie=b0c2b11300c56160cba46ff314647001; ci_session=5407140729cb6c162f76a92e2dbcbf4c88fbe4dc; GEMDCPROD=NODE2; TS0106b57a=015c77a21cfc0ce1ec28b764c46be1a8324cdb3441fdb85b600efbb049ee234fe0d2552398a6f60aa1f855a3a1ca58928f95b4963fa964585ed791d4e43e7fd8945ebd923f; TS01b34dec=015c77a21c97a18fc78cb68e0b246a2f811e2f72bafdb85b600efbb049ee234fe0d255239825cb06fede1704c2a355ca2192bc53274fef974425bbb6b518c39ac88e9b7ea6429506a1b7f46cef8a0eaaccea23e7e6; _gat=1; _ga_MMQ7TYBESB=GS1.3.1688101181.2.0.1688101181.60.0.0',
        'Origin': 'https://bidplus.gem.gov.in',
        'Referer': 'https://bidplus.gem.gov.in/all-bids',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.58',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Microsoft Edge";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    page = 0 


    def __init__(self):
        # create connection with exsisting db
            self.con = psycopg2.connect("dbname='new_bids' user='postgres' host='localhost' port='5432' password='madhuri123'")
            self.cur = self.con.cursor()
            self.create_table()

    def create_table(self
        #create a table
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


# make a request
    def start_requests(self):

        data = {
            'payload': '{"param":{"searchBid":"","searchType":"fullText"},"filter":{"bidStatusType":"ongoing_bids","byType":"all","highBidValue":"","byEndDate":{"from":"","to":""},"sort":"Bid-End-Date-Oldest"}}',
            'csrf_bd_gem_nk': 'b0c2b11300c56160cba46ff314647001',
        }

        yield scrapy.FormRequest("https://bidplus.gem.gov.in/all-bids-data",
                formdata=data, headers = self.headers, cookies =self.cookies, method='POST',
                callback=self.parse,)
# parse and extract data
    def parse(self, response):
        print(response.text)
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
            yield data

            self.cur.execute("INSERT INTO bids_data (key,Bid,Bid_No, Ra_No, Items, Quantity, Department, Startdate, Enddate, Document) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                            (key, Bid, Bid_No, Ra_No, Items, Quantity, Department, Startdate, Enddate, Document))
            
            self.con.commit()
    #pagination
               
        if page_Count > int(1):

            for page in range(2, int(page_Count)):
                cookies = {
                    '_ga': 'GA1.3.1385757445.1688058850',
                    '_gid': 'GA1.3.1613192119.1688058850',
                    'GEMDCPROD': 'NODE1',
                    'csrf_gem_cookie': '58df56a8c3cb1db2ec61eab633c97faf',
                    'ci_session': 'c94dabb65ff9a15bf5ca53ff6d7d7ceb0591b372',
                    'TS0106b57a': '015c77a21c6df16829846b8a8c44288330c3c5228366694ea5961747c05029bf86c278bd3430f0c5f7afdd3bad2b24c9f8e1b89dfbb5406cff5d3665f9ddc03c1ce7f5acd5',
                    'TS01b34dec': '015c77a21cf2f84a179101f79dfb51a47816a308d20df11ba2ed0e04caeba883b6a8b19616b0e29410814d2c101645a6c4a209e02df20c51b70fc528bb84aa05a2a409745ba7d767366fffaa442fc6979f4c88cafb',
                    '_ga_MMQ7TYBESB': 'GS1.3.1688111865.4.1.1688112675.60.0.0',
                }

                headers = {
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8',
                    'Connection': 'keep-alive',
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    # 'Cookie': '_ga=GA1.3.1385757445.1688058850; _gid=GA1.3.1613192119.1688058850; GEMDCPROD=NODE1; csrf_gem_cookie=58df56a8c3cb1db2ec61eab633c97faf; ci_session=c94dabb65ff9a15bf5ca53ff6d7d7ceb0591b372; TS0106b57a=015c77a21c6df16829846b8a8c44288330c3c5228366694ea5961747c05029bf86c278bd3430f0c5f7afdd3bad2b24c9f8e1b89dfbb5406cff5d3665f9ddc03c1ce7f5acd5; TS01b34dec=015c77a21cf2f84a179101f79dfb51a47816a308d20df11ba2ed0e04caeba883b6a8b19616b0e29410814d2c101645a6c4a209e02df20c51b70fc528bb84aa05a2a409745ba7d767366fffaa442fc6979f4c88cafb; _ga_MMQ7TYBESB=GS1.3.1688111865.4.1.1688112675.60.0.0',
                    'Origin': 'https://bidplus.gem.gov.in',
                    'Referer': 'https://bidplus.gem.gov.in/all-bids',
                    'Sec-Fetch-Dest': 'empty',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Site': 'same-origin',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.58',
                    'X-Requested-With': 'XMLHttpRequest',
                    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Microsoft Edge";v="114"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                }

                data = f'payload=%7B%22page%22%3A{page}%2C%22param%22%3A%7B%22searchBid%22%3A%22%22%2C%22searchType%22%3A%22fullText%22%7D%2C%22filter%22%3A%7B%22bidStatusType%22%3A%22ongoing_bids%22%2C%22byType%22%3A%22all%22%2C%22highBidValue%22%3A%22%22%2C%22byEndDate%22%3A%7B%22from%22%3A%22%22%2C%22to%22%3A%22%22%7D%2C%22sort%22%3A%22Bid-End-Date-Oldest%22%7D%7D&csrf_bd_gem_nk=58df56a8c3cb1db2ec61eab633c97faf'

                print("Response of page:",page)
                try:
                    new_response =  requests.post('https://bidplus.gem.gov.in/all-bids-data', cookies=cookies, headers=headers, data = data)
                    print(response.text)
                except Exception as e:
                    print(str(e))

                json_data = new_response.json()
                    
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
                    # push data into sql server

                    self.cur.execute("INSERT INTO bids_data (key,Bid,Bid_No, Ra_No, Items, Quantity, Department, Startdate, Enddate, Document) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                            (key,Bid, Bid_No, Ra_No, Items, Quantity, Department, Startdate, Enddate, Document))

                    yield new_data
            
                    self.con.commit()









        


