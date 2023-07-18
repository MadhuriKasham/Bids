import requests
from lxml import html
import psycopg2


class tenders:

    def __init__(self):
        self.con = psycopg2.connect(
            "dbname='Tenders' user='postgres' host='localhost' port='5432' password='madhuri123'")
        self.cur = self.con.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute(""" CREATE TABLE IF NOT EXISTS tenders_data (
                e_publish_date varchar(300),
                closing_date varchar(100),
                opening_date varchar(100),
                tender_id varchar(100),
                tender_url varchar(500),
                org_name varchar(500),
                corri_gen varchar(300),
                emd varchar(50));""")

        self.cur.execute(""" CREATE TABLE IF NOT EXISTS tenders_data_mpp (
                        e_publish_date varchar(300),
                        closing_date varchar(100),
                        opening_date varchar(100),
                        tender_id varchar(100),
                        tender_url varchar(500),
                        org_name varchar(500),
                        corri_gen varchar(300),
                        emd varchar(50));""")

    def commit(self, e_publish_date, closing_date, opening_date, tender_id, tender_url, org_name, corri_gen, emd):
        self.cur.execute(
            "INSERT INTO tenders_data (e_publish_date, closing_date, opening_date, tender_id, tender_url, org_name, "
            "corri_gen, emd) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",
            (e_publish_date, closing_date, opening_date, tender_id, tender_url, org_name, corri_gen, emd))
        self.con.commit()

    def commit_mpp(self, e_publish_date, closing_date, opening_date, tender_id, tender_url, org_name, corri_gen, emd):
        self.cur.execute(
            "INSERT INTO tenders_data_mpp (e_publish_date, closing_date, opening_date, tender_id, tender_url, org_name,"
            "corri_gen, emd) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",
            (e_publish_date, closing_date, opening_date, tender_id, tender_url, org_name, corri_gen, emd))
        self.con.commit()

    def cpp_tenders(self):

        print('cpp tenders crawl initiated')

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                      '*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': 'SSESS4e4a4d945e1f90e996acd5fb569779de=LOgSfzYkciUvpmGnYavPI-87TM1FncDSc_Kz9jVe0yM; '
                      '_ga=GA1.1.36191685.1689577827; cookieWorked=yes; '
                      '_ga_3WG6J8KXPN=GS1.1.1689588827.3.1.1689589206.0.0.0',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/114.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        response = requests.get("https://eprocure.gov.in/cppp/latestactivetendersnew/cpppdata", headers=headers)

        # data = response.text
        # print(data)
        html_data = html.fromstring(response.content)
        print('Response generated:', response)
        # print(html_data)
        initial = int(2)
        last1 = int(100)
        last = int(html_data.xpath('(//div[@class="pagination"]/a/text())[last()-1]')[0])
        print(last)

        for k in range(2, 12):
            print("Number range:", k)
            try:
                e_publish_date = html_data.xpath(f"//table[@id ='table']/descendant::tr[{k}]/child::td[2]/text()")[0]
            except:
                e_publish_date = ''
            try:
                closing_date = html_data.xpath(f"//table[@id ='table']/descendant::tr[{k}]/child::td[3]/text()")[0]
            except:
                closing_date = ''
            try:
                opening_date = html_data.xpath(f"//table[@id ='table']/descendant::tr[{k}]/child::td[4]/text()")[0]
            except:
                opening_date = ''
            try:
                tender_id = html_data.xpath(f"//table[@id ='table']/descendant::tr[{k}]/child::td[5]/text()")[0]
            except:
                tender_id = ''
            try:
                tender_url = html_data.xpath(f"//table[@id ='table']/descendant::tr[{k}]/child::td[5]/a/@href")[0]
            except:
                tender_url = ''
            try:
                org_name = html_data.xpath(f"///table[@id ='table']/descendant::tr[{k}]/child::td[6]/text()")[0]
            except:
                org_name = ''
            try:
                corri_gen = html_data.xpath(f"//table[@id ='table']/descendant::tr[{k}]/child::td[7]/text()")[0]
            except:
                corri_gen = 'None'

            print(e_publish_date)
            print(closing_date)
            print(opening_date)
            print(tender_id)
            print(tender_url)
            print(org_name)
            print(corri_gen)

            emd = 'None'

            self.commit(e_publish_date, closing_date, opening_date, tender_id, tender_url, org_name, corri_gen, emd)

        for j in range(initial, last1):
            print("Page has moved to", j)

            page_response = requests.get(f"https://eprocure.gov.in/cppp/latestactivetendersnew/cpppdata?page={j}",
                                         headers=headers)

            page_data = html.fromstring(page_response.content)

            for i in range(2, 12):
                print("Number range:", i)

                try:
                    e_publish_date = page_data.xpath(f"//table[@id ='table']/descendant::tr[{i}]/child::td[2]/text()")[
                        0]
                except:
                    e_publish_date = ''
                try:
                    closing_date = page_data.xpath(f"//table[@id ='table']/descendant::tr[{i}]/child::td[3]/text()")[0]
                except:
                    closing_date = ''
                try:
                    opening_date = page_data.xpath(f"//table[@id ='table']/descendant::tr[{i}]/child::td[4]/text()")[0]
                except:
                    opening_date = ''
                try:
                    tender_id = page_data.xpath(f"//table[@id ='table']/descendant::tr[{i}]/child::td[5]/text()")[0]
                except:
                    tender_id = ''
                try:
                    tender_url = page_data.xpath(f"//table[@id ='table']/descendant::tr[{i}]/child::td[5]/a/@href")[0]
                except:
                    tender_url = ''
                try:
                    org_name = page_data.xpath(f"///table[@id ='table']/descendant::tr[{i}]/child::td[6]/text()")[0]
                except:
                    org_name = ''
                try:
                    corri_gen = page_data.xpath(f"//table[@id ='table']/descendant::tr[{i}]/child::td[7]/text()")[0]
                except:
                    corri_gen = ''

                print(e_publish_date)
                print(closing_date)
                print(opening_date)
                print(tender_id)
                print(tender_url)
                print(org_name)
                print(corri_gen)

                emd = 'None'

                self.commit(e_publish_date, closing_date, opening_date, tender_id, tender_url, org_name, corri_gen, emd)

    def mmp_tenders(self):
        print('mmp tenders crawl initiated')

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                      '*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': 'SSESS4e4a4d945e1f90e996acd5fb569779de=LOgSfzYkciUvpmGnYavPI-87TM1FncDSc_Kz9jVe0yM; '
                      '_ga=GA1.1.36191685.1689577827; cookieWorked=yes; '
                      '_ga_3WG6J8KXPN=GS1.1.1689588827.3.1.1689589206.0.0.0',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/114.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        response = requests.get("https://eprocure.gov.in/cppp/latestactivetendersnew/mmpdata", headers=headers)

        # data = response.text
        # print(data)
        html_data = html.fromstring(response.content)
        print('Response generated:', response)
        # print(html_data)
        initial = int(2)
        last1 = int(100)
        last = int(html_data.xpath('(//div[@class="pagination"]/a/text())[last()-1]')[0])
        print(last)

        for k in range(2, 12):
            print("Number range:", k)
            try:
                e_publish_date = html_data.xpath(f"//table[@id ='table']/descendant::tr[{k}]/child::td[2]/text()")[0]
            except:
                e_publish_date = ''
            try:
                closing_date = html_data.xpath(f"//table[@id ='table']/descendant::tr[{k}]/child::td[3]/text()")[0]
            except:
                closing_date = ''
            try:
                opening_date = html_data.xpath(f"//table[@id ='table']/descendant::tr[{k}]/child::td[4]/text()")[0]
            except:
                opening_date = ''
            try:
                tender_id = html_data.xpath(f"//table[@id ='table']/descendant::tr[{k}]/child::td[5]/text()")[0]
            except:
                tender_id = ''
            try:
                tender_url = html_data.xpath(f"//table[@id ='table']/descendant::tr[{k}]/child::td[5]/a/@href")[0]
            except:
                tender_url = ''
            try:
                org_name = html_data.xpath(f"///table[@id ='table']/descendant::tr[{k}]/child::td[6]/text()")[0]
            except:
                org_name = ''
            try:
                corri_gen = html_data.xpath(f"//table[@id ='table']/descendant::tr[{k}]/child::td[7]/text()")[0]
            except:
                corri_gen = 'None'

            print(e_publish_date)
            print(closing_date)
            print(opening_date)
            print(tender_id)
            print(tender_url)
            print(org_name)
            print(corri_gen)

            emd = 'None'

            self.commit_mpp(e_publish_date, closing_date, opening_date, tender_id, tender_url, org_name, corri_gen, emd)

        for j in range(initial, last1):
            print("Page has moved to", j)

            page_response = requests.get(f"https://eprocure.gov.in/cppp/latestactivetendersnew/mmpdata?page={j}",
                                         headers=headers)

            page_data = html.fromstring(page_response.content)

            for i in range(2, 12):
                print("Number range:", i)

                try:
                    e_publish_date = page_data.xpath(f"//table[@id ='table']/descendant::tr[{i}]/child::td[2]/text()")[
                        0]
                except:
                    e_publish_date = ''
                try:
                    closing_date = page_data.xpath(f"//table[@id ='table']/descendant::tr[{i}]/child::td[3]/text()")[0]
                except:
                    closing_date = ''
                try:
                    opening_date = page_data.xpath(f"//table[@id ='table']/descendant::tr[{i}]/child::td[4]/text()")[0]
                except:
                    opening_date = ''
                try:
                    tender_id = page_data.xpath(f"//table[@id ='table']/descendant::tr[{i}]/child::td[5]/text()")[0]
                except:
                    tender_id = ''
                try:
                    tender_url = page_data.xpath(f"//table[@id ='table']/descendant::tr[{i}]/child::td[5]/a/@href")[0]
                except:
                    tender_url = ''
                try:
                    org_name = page_data.xpath(f"///table[@id ='table']/descendant::tr[{i}]/child::td[6]/text()")[0]
                except:
                    org_name = ''
                try:
                    corri_gen = page_data.xpath(f"//table[@id ='table']/descendant::tr[{i}]/child::td[7]/text()")[0]
                except:
                    corri_gen = ''

                print(e_publish_date)
                print(closing_date)
                print(opening_date)
                print(tender_id)
                print(tender_url)
                print(org_name)
                print(corri_gen)

                emd = 'None'

                self.commit_mpp(e_publish_date, closing_date, opening_date, tender_id, tender_url, org_name, corri_gen, emd)


the_object = tenders()
print('Please enter 1. cpp to crawl central tenders'
      '2. mmp to crawl state tenders')

user_input = str(input())
if user_input == str('cpp'):
    the_object.cpp_tenders()
else:
    the_object.mmp_tenders()
