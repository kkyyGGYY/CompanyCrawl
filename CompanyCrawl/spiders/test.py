import scrapy
from fake_useragent import UserAgent
from scrapy.http import Request
import logging

# logger = logging.getLogger("test spider")
from get_company_data import Company_excel


class TestSpider(scrapy.Spider):
    ua = UserAgent()
    name = "testp"
    # allowed_domains = ["https://www.riskstorm.com"]
    website_possible_httpstatus_list = [403]
    handle_httpstatus_list = [403]

    # start_urls = (
    #     'https://api.riskstorm.com/company/search?from=0&keyword=%E4%B8%AD%E7%A7%91%E8%BD%AF&size=20&tab_type=general&type=all',
    # )

    # def start_requests(self):
    #     # companys = Company().get_company_name_list()
    #     companys = ['中科软']
    #     for company_name in companys:
    #         url = 'https://api.riskstorm.com/company/search?from=0&keyword={name}&size=1&tab_type=general'.format(name=company_name)
    #         yield Request(
    #                 url=url,
    #                 method='GET',
    #                 headers={
    #                     'User-Agent': self.ua.random,
    #                 },
    #                 # meta={
    #                 #     'company_name': company_name,
    #                 # },
    #                 callback=self.parse,
    #         )
    def start_requests(self):
        # 循环产生各个公司的URL
        # companys = Company().get_company_name_list()
        # companys = Company_excel().get_company_name_list()
        companys = ['中科软']
        # a = ['911101053066433081', '91110108MA0058M9X5', '91110108MA007KQJ0L', '91110108318308662W', '911101083067861655',
        #  '91110107399886420U', '911100005694886378', '91110107571274099K', '911101053067639678', '9111010530676410X0']

        for company_name in companys:
            # search
            url = 'https://api.riskstorm.com/company/search?from=0&keyword={name}&size=1&tab_type=general'.format(name=company_name)

            # url = 'https://api.riskstorm.com/company/91110108551385082Q/overview/events'
            # url = 'https://api.riskstorm.com/company/91110108101966816T/abstract'
            # url = 'https://api.riskstorm.com/company/{name}/alerts'.format(name=company_name)
            # url = 'https://api.riskstorm.com/company/91110108551385082Q/overview/events'

            yield Request(
                    url=url,
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
        if response.status == "429":
            req = response.request
            req.meta["change_proxy"] = True
            yield req
        else:
            # logger.info("got page: %s" % response.body)
            print(response.text)
            yield response.request
