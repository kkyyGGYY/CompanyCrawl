import logging
import requests
from fake_useragent import UserAgent
logger = logging.getLogger(__name__)

ua = UserAgent()


def get_html(url):
    response = requests.get(url)
    return response.text


def check(proxy):
    # url = "https://www.jianshu.com/p/7f175cd60fed"
    proxies = {'https': "http://" + proxy}

    try:
        # response = requests.get(url, proxies=proxies, timeout=3)
        name = '中科软'
        headers = {
            'user-agent': ua.random
        }
        response = requests.get(
            'https://api.riskstorm.com/company/search?from=0&keyword={name}&size=1&tab_type=general'.format(
                name=name), headers=headers, proxies=proxies, timeout=5)
        return response.status_code == 200
    except Exception:
        return False


def get_proxy():
    headers = {
        'user-agent': ua.random
    }
    response = requests.get('http://tvp.daxiangdaili.com/ip/?tid=555232230231644&operator=1,2,3&num=10&protocol=https&delay=20&delay=5&filter=on', headers=headers)
    # print(response.text.split())
    proxyes = response.text.split()
    print(proxyes)
    valid_proxyes = []
    logger.info("checking proxyes validation")
    for p in proxyes:
        print(p, '---testing---')
        if check(p):
            valid_proxyes.append(p)
    return valid_proxyes


# if __name__ == '__main__':
    # import sys
    #
    # root_logger = logging.getLogger("")
    # stream_handler = logging.StreamHandler(sys.stdout)
    # formatter = logging.Formatter('%(name)-8s %(asctime)s %(levelname)-8s %(message)s', '%a, %d %b %Y %H:%M:%S', )
    # stream_handler.setFormatter(formatter)
    # root_logger.addHandler(stream_handler)
    # logger = logging.getLogger(__name__)
    # logger.setLevel(logging.DEBUG)
    # proxyes = get_proxy()
    # # print check("202.29.238.242:3128")
    # print(proxyes)
    # for p in proxyes:
    #     print(p)


if __name__ == '__main__':
    # ip = '195.214.212.160:8080'
    for ip in ['35.230.28.57:80', '119.42.114.72:8080', '195.214.212.160:8080', '188.115.185.129:8080']:
        if check(ip):
            print(ip)
        else:
            print('NOT')
