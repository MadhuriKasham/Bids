import scrapy
import json
import psycopg2
from GovBids.items import BidItem



class BidsSpider(scrapy.Spider):
    name = 'bids'
    allowed_domains = ['bidplus.gem.gov.in']
    # start_urls = ['http://https://bidplus.gem.gov.in/all-bids-data/']

    def __init__(self):
            self.con = psycopg2.connect("dbname='bids' user='postgres' host='localhost' port='5432' password='madhuri123'")
            self.cur = self.con.cursor()
            self.create_table()

    def create_table(self):
        self.cur.execute(""" CREATE TABLE IF NOT EXISTS bids_data (
            Bid int,
            Bid_No varchar(100),
            Items varchar(300),
            Quantity int,
            Department varchar(300),
            Startdate date,
            Enddate date,
            Document varchar(200));""")



    def start_requests(self):
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

        data = {
            'payload': '{"param":{"searchBid":"","searchType":"fullText"},"filter":{"bidStatusType":"ongoing_bids","byType":"all","highBidValue":"","byEndDate":{"from":"","to":""},"sort":"Bid-End-Date-Oldest"}}',
            'csrf_bd_gem_nk': 'b0c2b11300c56160cba46ff314647001',
        }

        yield scrapy.FormRequest("https://bidplus.gem.gov.in/all-bids-data",
                formdata=data, headers = headers, cookies =cookies, method='POST',
                callback=self.parse,)

    def parse(self, response):
        # print(response.text)
        json_data = response.json()
        Total = json_data['response']['response']['numFound']
        page_Count = (Total/10)+1
        json_value = json_data['response']['response']["docs"]
        value = len(json_value)
        for val in range(0, value):
            Bid = json_value[val]['id']
            Bid_No = json_value[val]['b_bid_number'][0]
            Items = json_value[val]['b_category_name'][0]
            Quantity = json_value[val]['b_total_quantity'][0]
            Department = json_value[val]['ba_official_details_deptName'][0]
            Startdate = ((json_value[val]['final_start_date_sort'][0]).split('T',1))[0]
            Enddate = ((json_value[val]['final_end_date_sort'][0]).split('T',1))[0]
            Document = f"https://bidplus.gem.gov.in/showbidDocument/{Bid}"

            data = {
                'Bid' :Bid,
                'Bid_No' : Bid_No,
                'Items' : Items,
                'Quantity' :Quantity,
                'Department' : Department,
                'Startdate' : Startdate,
                'Enddate' : Enddate,
                'Document' : Document
            }

            self.cur.execute("INSERT INTO bids_data (Bid, Bid_No, Items, Quantity, Department, Startdate, Enddate, Document) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",
                            (Bid, Bid_No, Items, Quantity, Department, Startdate, Enddate, Document))
            
    
            # self.cur.execute("INSERT INTO bids_data (Bid, Bid_No, Items, Quantity, Department, Startdate, Enddate, Document) values(%s, %s, %s, %s, %s, %s, %s, %s)")
            self.con.commit()

            # bid_item = BidItem()
            

            # # yield {
            # bid_item['Bid']= Bid,
            # bid_item['Bid_No'] = Bid_No,
            # bid_item['Items'] = Items,
            # bid_item['Quantity'] = Quantity,
            # bid_item['Department'] = Department,
            # bid_item['Startdate']= Startdate,
            # bid_item['Enddate'] = Enddate,
            # bid_item['Document'] = Document,
            
            yield data

            # }


        


