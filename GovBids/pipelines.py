# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2



class GovbidsPipeline:
    def process_item(self, item, spider):
        return item

class SQLPipeline:
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
        

    def process_item(self, item, spider):
        self.cur.execute("INSERT INTO bids_data (Bid, Bid_No, Items, Quantity, Department, Startdate, Enddate, Document) values(%s, %s, %s, %s, %s, %s, %s, %s)", 
                        (item['Bid'], item['Bid_No'], item['Items'], item['Quantity'],item['Department'], item['Startdate'], item['Enddate'], item['Document'],))
        self.cur.execute("INSERT INTO bids_data values (%s, %s, %s, %s, %s, %s, %s, %s)")
        self.con.commit()
      
        return item


        

    
