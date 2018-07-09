from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic.base import View
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
# from com_search.get_info import Search as Search_1
# from com_search.models import CompanyType
import json
# Create your views here.


class SearchSuggest(View):
    def get(self, request):
        key_words = request.GET.get('s','')
        # print(key_words, '===============')
        re_datas = []
        com_datas = []
        if key_words:

            es = Elasticsearch(hosts=["127.0.0.1"])
            s = Search(index='zntg_2').using(es).query('match', company_name=key_words)
            for i in s:
                re_datas.append(i.company_name)
            res = s.execute()

            # s = CompanyType.search()
            # s = s.suggest('my_suggest', key_words, completion={
            #     "field": "suggest", "fuzzy": {
            #         "fuzziness": 2
            #     },
            #     "size": 10
            # })
            # suggestions = s.execute_suggest()
            # for match in suggestions.my_suggest[0].options:
            # for match in suggestions.my_suggest[0].options:
            #     source = match._source
            #     com_datas.append(str(source))
            #     re_datas.append(source["company_name"])
                # print(source)
            # print(re_datas)
            # # print(suggestions['my_suggest'][0])
            # # print(suggestions['my_suggest'][0]['options'])
            # print(json.dumps(re_datas))
            # print(com_datas)
            # print(json.dumps(com_datas))
        return HttpResponse(json.dumps(re_datas), content_type="application/json")


class SearchDetail(View):
    def get(self, request):
        key_words = request.GET.get('q', '')
        # print(key_words, '===============')
        data = {}
        if key_words:
            es = Elasticsearch(hosts=["127.0.0.1"])
            s = Search(index='zntg_2').using(es).query('match', company_name=key_words)
            for i in s[0]:
                # print(i.company_name)
                # for k in ['company_name', 'crn', 'former_name', 'organization_type', 'faren', 'registered_capital', 'company_type', 'registration_state', 'searched_by', 'data_count']:

                data['company_name'] = i.company_name
                data['crn'] = i.crn
                try:
                    data['former_name'] = str(i.former_name)
                except:
                    pass
                data['organization_type'] = i.organization_type
                data['faren'] = i.faren
                data['registered_capital'] = i.registered_capital
                data['company_type'] = i.company_type
                data['registration_state'] = i.registration_state
                data['searched_by'] = str(i.searched_by)
                data['data_count'] = i.data_count
        # print(data)
        return HttpResponse(json.dumps(data), content_type="application/json")


class CodeSearch(View):
    def get(self, request):
        key_words = request.GET.get('code', '')
        print(key_words)
        search = Search_1()
        data = search.get_data(key_words)
        # text = {'code': key_words}
        # print(json.dumps(text))
        print(data)
        return JsonResponse(data)



if __name__ == '__main__':
    # client = Elasticsearch(hosts=["127.0.0.1"])
    # 创建相关实例
    es = Elasticsearch(hosts=["127.0.0.1"])
    # using参数是指定Elasticsearch实例对象，index指定索引，可以缩小范围，index接受一个列表作为多个索引，且也可以用正则表示符合某种规则的索引都可以被索引，如index=["bank", "banner", "country"]又如index=["b*"]后者可以同时索引所有以b开头的索引，search中同样可以指定具体doc-type
    # s = Search(using=client, index="zntg_5")
    # q = {"query": {"match": {"name": "easy"}}}
    # res = es.Search(body=q)
    # print(res)
    s = Search(index='zntg_2').using(es).query('match', company_name='延安一正启源科技发展股份有限公司')
    # for i in s[0]:
    #     print(i.company_name)
    #     print(i.company_type)
    res = s.execute()
    # print(res)
    # res = es.get(index="zntg_5", doc_type="company", id='AWQ7fKZzZ2odEMYJXOY0')
    # print(res["hits"]["hits"][0]['_source'])
    a = res["hits"]["hits"][0]['_source']
    print(a['former_name'])
