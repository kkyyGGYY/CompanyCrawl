import requests
from fake_useragent import UserAgent
from lxml import etree
import re
import json


class Search:
    def get_data(self, code):
        DATA = {'Name': '', 'PERation': '', 'PBRation': '', 'Worth': '', 'Code': '', 'JPERation': '', 'DPERation': '', 'PS': ''}
        ua = UserAgent()
        if len(code) == 6:
            if code <= '400000':
                try:
                    url2 = 'http://data.eastmoney.com/stockdata/{code}.html'.format(code=code)
                    response = requests.get(url=url2, headers={'user-agent': ua.random}).text
                    a = etree.HTML(response)
                    s_list = a.xpath("//script/text()")
                    # name = a.xpath("//title")[0].text.encode('latin').decode('gb2312')
                    # print(s_list[-2].encode('latin').decode('gb2312'))
                    v = s_list[-2]
                    tem = re.search(r'"Data":(?P<data>.*?),{"', v, flags=re.DOTALL)
                    data = tem.group('data')[1:].encode('utf-8')
                    data = eval(str(data, 'utf-8'))
                    name = data['Name'].encode('latin').decode('gb2312')
                    data['Name'] = name
                    for v in DATA.keys():
                        DATA[v] = data.get(v, '')
                    # print(data)

                except:
                    DATA = {'Error': 'incorrect code'}
                # print(data)
            else:
                try:
                    url1 = 'http://xinsanban.eastmoney.com/api/QuoteCenter/stock/GetCwzb?code={code}'.format(code=code)
                    response = requests.get(url1, headers={'user-agent': ua.random}).text
                    a = json.loads(response)['result']
                    data = json.dumps(a)
                    data = eval(data)[0]
                    url3 = 'http://xinsanban.eastmoney.com/api/QuoteCenter/stock/Get5dang?code={code}'.format(code=code)
                    response2 = requests.get(url3, headers={'user-agent': ua.random}).text
                    name = json.loads(response2)['result']
                    name = eval(json.dumps(name))[0]['Name']
                    data['Name'] = name
                    # print(data)
                    DATA['Name'] = name
                    DATA['Worth'] = data['CMVALUE']
                    # DATA['PS'] =
                    # DATA['DPERation']
                    # DATA['JPERation']
                    DATA['PBRation'] = data['PBMRQ']
                    DATA['Code'] = code
                    DATA['PERation'] = data['PELYR']
                except:
                    DATA = {'Error': 'incorrect code'}
        else:
            DATA = {'Error': 'incorrect code'}
        return DATA

if __name__ == '__main__':
    s = Search()
    code = '002453'
    print(s.get_data(code))
    print(s.get_data('430044'))
