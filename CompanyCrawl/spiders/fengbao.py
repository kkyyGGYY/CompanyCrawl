# -*- coding: utf-8 -*-
import scrapy
from requests import ReadTimeout, RequestException, ConnectionError
from scrapy import Request
from fake_useragent import UserAgent
import scrapy
import time
from scrapy import Request, signals
from fake_useragent import UserAgent
import json
from scrapy.xlib.pydispatch import dispatcher
from get_company_data import Company, Company_excel
from CompanyCrawl.items import CompanycrawlItem, AlertscrawlItem, EventcrawlItem, RiskscrawlItem, IndustrycrawlItem, LegalcrawlItem
import requests
from CompanyCrawl import x_token


class FengbaoSpider(scrapy.Spider):
    name = 'fengbao'
    website_possible_httpstatus_list = [403, 429]
    handle_httpstatus_list = [403, 429]
    # allowed_domains = ['https://www.riskstorm.com']
    start_urls = ['https://www.riskstorm.com/']

    def __init__(self, *a, **kw):
        # 创建Fake-Useragent
        self.ua = UserAgent()
        super(FengbaoSpider, self).__init__(*a, **kw)
        self.url = ''
        self.X_token = x_token.X_token
        # dispatcher.connect(self.spider_closed, signals.spider_closed)

        # self.init()

    def init(self):
        # 创建Mysql数据表
        command = ("CREATE TABLE IF NOT EXISTS {} ("
                   "`id` INT(8) NOT NULL AUTO_INCREMENT,"
                   "`unique_id` CHAR(25) NOT NULL UNIQUE,"
                   "`city_id` INT(9) NOT NULL,"
                   "`city_name` TEXT NOT NULL,"
                   "`date` DATE NOT NULL,"
                   "`time` TEXT NOT NULL,"
                   "`week` TEXT NOT NULL,"
                   "`cur_temperature` TEXT NOT NULL,"
                   "`max_temperature` TEXT NOT NULL,"
                   "`min_temperature` TEXT NOT NULL,"
                   "`overall` TEXT NOT NULL,"
                   "`humidity` TEXT NOT NULL,"
                   "`aqi` INT(3) DEFAULT NULL,"
                   "`aqi_pm25` INT(3) DEFAULT NULL,"
                   "`aqi_level` TEXT NOT NULL,"
                   "`weather` TEXT NOT NULL,"
                   "`wind_direction` TEXT DEFAULT NULL,"
                   "`wind_force` TEXT DEFAULT NULL,"
                   "`wind_speed` TEXT DEFAULT NULL,"
                   "`warning_level` TEXT DEFAULT NULL,"
                   "`warning_date` TEXT DEFAULT NULL,"
                   "`warning_info` TEXT DEFAULT NULL,"
                   "`remarks` TEXT DEFAULT NULL,"
                   "`other` TEXT DEFAULT NULL,"
                   "`save_data_time` TIMESTAMP NOT NULL,"
                   "`mini_weather` TEXT DEFAULT NULL,"
                   "`sk_2d_weather` TEXT DEFAULT NULL,"
                   "`dingzhi_weather` TEXT DEFAULT NULL,"
                   "PRIMARY KEY(id)"
                   ") ENGINE=InnoDB".format(self.weather_table_name))

        self.sql.create_table(command)

    # def check_status(self, response):
    #     if response.status != "200":
    #         req = response.request
    #         req.meta["change_proxy"] = True
    #         yield req
    #     else:
    #         # logger.info("got page: %s" % response.body)
    #         return response


    '''
    def start_requests(self):
        # 循环产生各个公司的URL
        # companys = Company().get_company_name_list()
        # companys = Company_excel().get_company_name_list()
        companys = ['中科软']
        for company_name in companys:
            url = 'https://api.riskstorm.com/company/search?from=0&keyword={name}&size=1&tab_type=general'.format(name=company_name)
            yield Request(
                    url=url,
                    method='GET',
                    headers={
                        'User-Agent': self.ua.random,
                        # 'x-token': self.X_token,
                    },
                    # meta={
                    #     'company_name': company_name,
                    # },
                    callback=self.company_info,
            )
            '''
    def parse(self, response):
        companys = Company().get_company_name_list()
        # companys = Company_excel().get_company_name_list()
        # companys = ['阿里', ]
        for company_name in companys:
            try:
                url = 'https://api.riskstorm.com/company/search?from=0&keyword={name}&size=1&tab_type=general'.format(
                    name=company_name)
                ct = CompanyT()
                com_json = ct.get_company_crn(company_name)['companies'][0]

                item = CompanycrawlItem()
                print(com_json)
                item['reg_no'] = com_json.get('reg_no', '')
                item['company_name'] = com_json.get('name', '')
                item['crn'] = com_json.get('crn', '')
                item['organization_type'] = com_json.get('organization_type', '')
                item['faren'] = com_json.get('法人', '')
                item['registered_capital'] = com_json.get('注册资本', '')
                item['company_type'] = com_json.get('类型', '')
                item['registration_state'] = com_json.get('登记状态', '')
                item['former_name'] = com_json.get('former_name', '')
                item['searched_by'] = com_json.get('searched_by', '')
                item['data_count'] = com_json.get('data_count', '')
                item['establishment_date'] = com_json.get('成立日期', '')
                yield item
            except:
                with open('Error_company.csv', 'a') as f:
                    f.writelines(company_name + '/n')
                continue


    def company_info(self, response):
        """获取公司基本信息"""
        com_json = json.loads(response.text)['companies'][0]
        crn = com_json['crn']
        # 创建Item
        # print(com_json['name'])
        item = {}
        item['company_name'] = com_json.get('name', '')
        item['crn'] = com_json.get('crn', '')
        item['organization_type'] = com_json.get('organization_type', '')
        item['faren'] = com_json.get('法人', '')
        item['registered_capital'] = com_json.get('注册资本', '')
        item['company_type'] = com_json.get('类型', '')
        item['registration_state'] = com_json.get('登记状态', '')
        item['former_name'] = com_json.get('former_name', '')
        item['searched_by'] = com_json.get('searched_by', '')
        item['data_count'] = com_json.get('data_count', '')
        item['establishment_date'] = com_json.get('成立日期', '')

        # json.loads(requests.get(self.url + '/abstract', )).get('abstract')

        # print(item)
        # yield item
        self.url = 'https://api.riskstorm.com/company/{crn}'.format(crn=crn)

        infs = ['industry_finance', 'risks', 'abstract', 'overview/lawsuit', 'overview/events']
        yield Request(
            url=self.url + '/abstract',
            method='GET',
            headers={
                'User-Agent': self.ua.random,
                'x-token': self.X_token,
            },
            callback=self.get_abstract,
            meta={
                'item': item,
            },
        )
        #
        # yield Request(
        #     url=url+'/abstract',
        #     method='GET',
        #     headers={
        #         'User-Agent': self.ua.random,
        #     },
        #     callback=self.dayin,
        # )
        #
        # yield Request(
        #     url=url + '/overview/lawsuit',
        #     method='GET',
        #     headers={
        #         'User-Agent': self.ua.random,
        #         'x-token': 'N8ePPERV.93910.iTfCxU0KLL4D',
        #     },
        #     callback=self.dayin,
        # )
        #
        # yield Request(
        #     url=url + '/overview/events',
        #     method='GET',
        #     headers={
        #         'User-Agent': self.ua.random,
        #     },
        #     callback=self.dayin,
        # )
        #
        # yield Request(
        #     url=url + '/risks',
        #     method='GET',
        #     headers={
        #         'User-Agent': self.ua.random,
        #         'x-token': 'N8ePPERV.93910.iTfCxU0KLL4D',
        #     },
        #     callback=self.dayin,
        # )

    def get_abstract(self, response):
        data = json.loads(response.text)
        com_item = response.meta.get('item')

        item = CompanycrawlItem()
        item['abstract'] = data.get('abstract', '')
        item['company_name'] = com_item.get('company_name', '')
        item['crn'] = com_item.get('crn', '')
        item['organization_type'] = com_item.get('organization_type', '')
        item['faren'] = com_item.get('faren', '')
        item['registered_capital'] = com_item.get('registered_capital', '')
        item['company_type'] = com_item.get('company_type', '')
        item['registration_state'] = com_item.get('registration_state', '')
        item['former_name'] = com_item.get('former_name', '')
        item['searched_by'] = com_item.get('searched_by', '')
        item['data_count'] = com_item.get('data_count', '')
        item['establishment_date'] = com_item.get('establishment_date', '')

        yield item

        yield Request(
            url=self.url + '/alerts',
            method='GET',
            headers={
                'User-Agent': self.ua.random,
                'x-token': self.X_token,
            },
            callback=self.get_alerts,
            meta={
                'crn': item['crn'],
            }
        )

    def get_alerts(self, response):
        data = json.loads(response.text)
        crn = response.meta.get('crn')

        item = AlertscrawlItem()
        item['crn'] = crn
        item['alerts'] = data.get('aggregations', '')

        yield item
        # print(item)
        yield Request(
            url=self.url + '/overview/events',
            method='GET',
            headers={
                'User-Agent': self.ua.random,
                'x-token': self.X_token,
            },
            callback=self.get_events,
            meta={
                'crn': crn,
            }
        )

    def get_events(self, response):
        data = json.loads(response.text)
        crn = response.meta.get('crn')

        item = EventcrawlItem()
        item['crn'] = crn
        item['events'] = data

        yield item
        # print(item)
        yield Request(
            url=self.url + '/risks',
            method='GET',
            headers={
                'User-Agent': self.ua.random,
                'x-token': self.X_token,
            },
            callback=self.get_risks,
            meta={
                'crn': crn,
            }
        )

    def get_risks(self, response):
        data = json.loads(response.text)
        crn = response.meta.get('crn')

        item = RiskscrawlItem()
        item['crn'] = crn
        item['risks'] = data
        yield item

        yield Request(
            url=self.url + '/legal',
            method='GET',
            headers={
                'User-Agent': self.ua.random,
                'x-token': self.X_token,
            },
            callback=self.get_legal,
            meta={
                'crn': crn,
            }
        )

    def get_legal(self, response):
        data = json.loads(response.text)
        crn = response.meta.get('crn')

        item = LegalcrawlItem()
        item['crn'] = crn
        item['legal'] = data.get('aggregations', '')
        # print(item, '=======')
        yield item

        yield Request(
            url=self.url + '/industry_finance',
            method='GET',
            headers={
                'User-Agent': self.ua.random,
                'x-token': self.X_token,
            },
            callback=self.get_industry_finance,
            meta={
                'crn': crn,
            }
        )

    def get_industry_finance(self, response):
        '''industry_finance'''

        data = json.loads(response.text)
        crn = response.meta.get('crn')

        item = IndustrycrawlItem()
        item['industry_finance'] = data
        item['crn'] = crn

        yield item

    def get_crn(self, response):
        com_json = json.loads(response.text)
        print(com_json)
        print(com_json['companies'][0]['crn'])

        # return com_json['companies'][0]['crn']

    def dayin(self, response):
        print(response.text)


class CompanyT:

    def get_proxy(self):
        ua = UserAgent()
        headers = {
            'user-agent': ua.random
        }
        # time.sleep(1)
        response = requests.get(
            'http://tvp.daxiangdaili.com/ip/?tid=555232230231644&num=1&protocol=https&delay=20&filter=on',
            headers=headers)
        return response.text

    def get_company_crn(self, name):

        # proxies = {
        #     "https": "http://{0}".format(get_proxy()),
        # }
        # headers = {
        #     'user-agent': get_random_ua()
        # }
        # print(proxies)
        while True:
            ua = UserAgent()
            proxies = {
                "https": "http://{0}".format(self.get_proxy()),
            }
            headers = {
                'user-agent': ua.random
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
                # print(com_json)
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
