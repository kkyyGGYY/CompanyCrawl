from django.db import models

# Create your models here.
from datetime import datetime
from elasticsearch_dsl import DocType, Date, Integer, Keyword, Text
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Completion
from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer

# Define a default Elasticsearch client
connections.create_connection(hosts=['localhost'])


class CustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return {}

ik_analyzer = CustomAnalyzer('ik_max_word', filter=['lowercase'])


class CompanyType(DocType):

    # company_name_suggest = Completion(analyzer=ik_analyzer, search_analyzer=ik_analyzer)
    suggest = Completion(analyzer=ik_analyzer, search_analyzer=ik_analyzer)
    # crn_suggest = Completion(analyzer=ik_analyzer, search_analyzer=ik_analyzer)

    company_name = Text(analyzer='ik_max_word', search_analyzer="ik_max_word", fields={'company_name': Keyword()})
    crn = Text()

    former_name = Text()
    organization_type = Text()
    faren = Text()
    registered_capital = Text()
    company_type = Text()
    registration_state = Text()
    searched_by = Text()
    data_count = Text()
    # abstract = Text()

    # risks = Text()
    # lawsuits = Text()
    # industry_finance = Text()

    class Meta:
        index = 'zntg_5'
        doc_type = 'company'
    #
    # def save(self, ** kwargs):
    #     self.lines = len(self.body.split())
    #     return super(Article, self).save(** kwargs)

    # def is_published(self):
    #     return datetime.now() < self.published_from


class RiskType(DocType):
    crn = Text(analyzer='ik_max_word', search_analyzer="ik_max_word", fields={'crn': Keyword()})

    risks = Text()

    class Meta:
        index = 'zntg_2'
        doc_type = 'risk'


class AlertType(DocType):
    crn = Text(analyzer='ik_max_word', search_analyzer="ik_max_word", fields={'crn': Keyword()})

    alerts = Text()

    class Meta:
        index = 'zntg_2'
        doc_type = 'alert'


class IndustryType(DocType):
    crn = Text(analyzer='ik_max_word', search_analyzer="ik_max_word", fields={'crn': Keyword()})

    industry_finance = Text()

    class Meta:
        index = 'zntg_2'
        doc_type = 'industry'


class EventType(DocType):
    crn = Text(analyzer='ik_max_word', search_analyzer="ik_max_word", fields={'crn': Keyword()})

    events = Text()

    class Meta:
        index = 'zntg_2'
        doc_type = 'event'


class LegalType(DocType):
    crn = Text(analyzer='ik_max_word', search_analyzer="ik_max_word", fields={'crn': Keyword()})

    legal = Text()

    class Meta:
        index = 'zntg_2'
        doc_type = 'legal'

if __name__ == '__main__':
    CompanyType.init()
    RiskType.init()
    EventType.init()
    AlertType.init()
    IndustryType.init()
    LegalType.init()
