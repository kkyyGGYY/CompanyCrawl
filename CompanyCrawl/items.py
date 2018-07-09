# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from w3lib.html import remove_tags

from .models.models import CompanyType

from .models.models import CompanyType, LegalType, AlertType, EventType, IndustryType, RiskType
from elasticsearch_dsl.connections import connections
es = connections.create_connection(CompanyType._doc_type.using)


def gen_suggests(index, info_tuple):
    # 根据字符串权重生成建议
    used_words = set()  # 去重
    suggests = []
    for text, weight in info_tuple:
        if text:
            # 调用es分析字符串
            words = es.indices.analyze(index=index, analyzer='ik_max_word', params={'filter': ['lowercase']}, body=text)
            analyzed_words = set([r['token'] for r in words["tokens"] if len(r['token']) > 1])
            new_words = analyzed_words - used_words
        else:
            new_words = set()

        if new_words:
            suggests.append({"input": list(new_words), "weight": weight})

    return suggests


class CompanycrawlItem(scrapy.Item):
    # 定义公司模型
    # flag = scrapy.Field()
    # page = scrapy.Field()

    # normal
    company_name = scrapy.Field()
    establishment_date = scrapy.Field()
    crn = scrapy.Field()
    organization_type = scrapy.Field()
    faren = scrapy.Field()
    registered_capital = scrapy.Field()
    company_type = scrapy.Field()
    registration_state = scrapy.Field()
    former_name = scrapy.Field()
    searched_by = scrapy.Field()
    data_count = scrapy.Field()
    reg_no = scrapy.Field()
    # abstract = scrapy.Field()

    # risks = scrapy.Field()
    # lawsuits = scrapy.Field()
    # industry_finance = scrapy.Field()
    def save_to_es(self):
        company = CompanyType()

        company.establishment_date = self['establishment_date']
        company.company_name = self['company_name']
        company.crn = self['crn']
        company.organization_type = self['organization_type']
        company.faren = self['faren']
        company.registered_capital = self['registered_capital']
        company.company_type = self['company_type']
        company.registration_state = self['registration_state']
        if self['former_name'] == []:
            company.former_name = ''
        company.former_name = self['former_name']
        company.searched_by = self['searched_by']
        company.data_count = str(self['data_count'])
        # company.abstract = self['abstract']

        company.suggest = gen_suggests(CompanyType._doc_type.index, [(company.company_name, 10)])

        company.save()

        return


class RiskscrawlItem(scrapy.Item):
    crn = scrapy.Field()
    risks = scrapy.Field()

    def save_to_es(self):

        risk = RiskType()
        risk.crn = self['crn']
        risk.risks = str(self['risks'])

        risk.save()
        return


class AlertscrawlItem(scrapy.Item):
    crn = scrapy.Field()
    alerts = scrapy.Field()

    def save_to_es(self):
        alerts = AlertType()
        alerts.crn = self['crn']
        alerts.alerts = str(self['alerts'])

        alerts.save()
        return


class IndustrycrawlItem(scrapy.Item):
    crn = scrapy.Field()
    industry_finance = scrapy.Field()

    def save_to_es(self):
        industry_finance = IndustryType()
        industry_finance.crn = self['crn']
        industry_finance.industry_finance = str(self['industry_finance'])

        industry_finance.save()
        return


class EventcrawlItem(scrapy.Item):
    crn = scrapy.Field()
    events = scrapy.Field()

    def save_to_es(self):
        events = EventType()
        events.crn = self['crn']
        events.events = str(self['events'])

        events.save()
        return


class LegalcrawlItem(scrapy.Item):
    crn = scrapy.Field()
    legal = scrapy.Field()

    def save_to_es(self):
        legal = LegalType()
        legal.crn = self['crn']
        legal.legal = str(self['legal'])

        legal.save()
        return
