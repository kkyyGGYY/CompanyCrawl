import requests
from fake_useragent import UserAgent
from CompanyCrawl.settings import DAXIANG_PROXY_TID


class Proxy_IP():
    # 获取动态代理
    ua = UserAgent()
    headers = {'user-agent': ua.random}

    def judge_ip(self, ip):
        # 判断ip是否可用
        # http_url = "https://api.riskstorm.com/company/search?from=0&keyword={name}&size=1&tab_type=general".format(name='中科软')
        http_url = "https://www.baidu.com"
        proxy_url = "http://{0}".format(ip)
        try:
            proxy_dict = {
                "https": proxy_url,
            }
            response = requests.get(http_url, proxies=proxy_dict, headers=self.headers, timeout=3)
        except Exception as e:
            print("invalid ip and port", ip)
            return False
        else:
            code = response.status_code
            if code >= 200 and code < 300:
            # if code == 200:
            #     print(response.text)
                print("effective ip")
                return True
            else:
                print("invalid ip and port", ip)
                return False

    def https_proxy(self):
        # time.sleep(1)
        response = requests.get('http://tvp.daxiangdaili.com/ip/?tid={tid}&num=1&protocol=https&delay=20&filter=on&delay=5'.format(tid=DAXIANG_PROXY_TID), headers=self.headers)
        # print(response.text)
        return response.text

    def get_valid_proxy(self):
        # while True:
        ip = self.https_proxy()
        judge_re = self.judge_ip(ip)
        if judge_re:
            return "http://{0}".format(ip)
        else:
            return self.get_valid_proxy()

if __name__ == "__main__":
    ua = UserAgent()
    print(DAXIANG_PROXY_TID)
    get_ip = Proxy_IP()
    ip = get_ip.get_valid_proxy()
    print(ip)
    # print(ua.random)
    response = requests.get('https://api.riskstorm.com/company/search?from=0&keyword={name}&size=1&tab_type=general'.format(name='华软资本'), proxies={'https': ip}, headers={'user-agent': ua.random})
    print(response.text)
