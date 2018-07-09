import scrapy
from fake_useragent import UserAgent
from requests import ReadTimeout, RequestException
from scrapy.http import Request
import logging
from get_company_data import Company, Company_excel
from CompanyCrawl.tools import proxy_daxiang
import requests
import json


# logger = logging.getLogger("test spider")
from get_company_data import Company_excel


class TestSpider(scrapy.Spider):
    ua = UserAgent()
    name = "test"
    # allowed_domains = ["https://www.riskstorm.com"]
    website_possible_httpstatus_list = []
    handle_httpstatus_list = []

    def get_proxy(self):
        headers = {
            'user-agent': self.ua.random
        }
        # time.sleep(1)
        response = requests.get(
            'http://tvp.daxiangdaili.com/ip/?tid=555232230231644&num=1&protocol=https&delay=20&filter=on',
            headers=headers)
        return response.text

    def get_company_crn(self, name):
        while True:
            proxies = {
                "https": "http://{0}".format(self.get_proxy()),
            }
            headers = {
                'user-agent': self.ua.random
            }
            print(proxies)
            try:
                response = requests.get(
                    'https://api.riskstorm.com/company/search?from=0&keyword={name}&size=1&tab_type=general'.format(
                        name=name), headers=headers, proxies=proxies, timeout=3)
                # t = response.elapsed.microseconds
                # print(response.text)
                # print(t)
                com_json = json.loads(response.text)
                print(com_json)
                return com_json

            except ReadTimeout:
                print('Timeout')
                # get_company_crn(name)
            except ConnectionError:
                print('Connection error')
                # get_company_crn(name)
            except RequestException:
                print('Error')
            except:
                print('invalid proxy')
    def start_requests(self):
        # 循环产生各个公司的URL
        # companys = Company().get_company_name_list()
        companys = Company_excel().get_company_name_list()
        # companys = ['中科软', '小米']
        for company_name in companys:
            json_item = self.get_company_crn(company_name)
            print(json_item)
            # 没有该公司，或公司名有误
            if json_item['companies_amount'] == 0:
                with open('wrong_company.csv', 'a') as f:
                    f.writelines(company_name)
                continue
            crn = json_item['companies'][0]['crn']
            # ip = proxy_daxiang.Proxy_IP()
            # search
            # url = 'https://api.riskstorm.com/company/search?from=0&keyword={name}&size=1&tab_type=general'.format(name=company_name)
            #
            # url = 'https://api.riskstorm.com/company/91110108551385082Q/overview/events'

            # url = 'https://api.riskstorm.com/company/91110108101966816T/industry_finance'  # 不要代理

            # url = 'https://api.riskstorm.com/company/91110108551385082Q/legal?size=5'  # 有X-token不需要代理

            # url = 'https://api.riskstorm.com/company/91110108551385082Q/risks'  # 有X-token不需要代理
            # url = 'https://api.riskstorm.com/company/search?from=0&keyword={name}&size=1&tab_type=general'.format(name=company_name)

            url = 'https://api.riskstorm.com/company/{crn}'.format(crn=crn)
            yield Request(
                    url=url + '/industry_finance',
                    method='GET',
                    headers={
                        'User-Agent': self.ua.random,
                        'x-token': 'N8ePPERV.93910.iTfCxU0KLL4D',
                    },
                    # meta={
                    #     'company_name': company_name,
                    # },
                    callback=self.parse,
                    dont_filter=True,
            )

    def parse(self, response):
        if response.status in ['429', '403']:
            req = response.request
            req.meta["change_proxy"] = True
            # print(response.text)
            yield req
        else:
            # logger.info("got page: %s" % response.body)

            print(response.text)
            # yield response.request
