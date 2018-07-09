#coding:utf-8
import requests
import re
import jsbeautifier
import js2py

host_url = 'http://www.pbc.gov.cn/'
dest_url = 'http://www.pbc.gov.cn/eportal/fileDir/defaultCurSite/resource/cms/2015/07/2010s09.htm'
r = requests.session()
content = r.get(dest_url).content
re_script = re.search(r'<script type="text/javascript">(?P<script>.*)</script>', content.decode('utf-8'), flags=re.DOTALL)
script = re_script.group('script')
script = script.replace('\r\n', '')
res = jsbeautifier.beautify(script)
with open('x.js', 'w') as f:
    f.write(res)

jscode_list = res.split('function')
var_ = jscode_list[0]
var_list = var_.split('\n')
template_js = var_list[3]
template_py = js2py.eval_js(template_js)
function1_js = 'function' + jscode_list[1]
position = function1_js.index('{') +1
function1_js = function1_js[:position]+ var_ +function1_js[position:]
function1_py = js2py.eval_js(function1_js)
cookie1 = function1_py(str(template_py))
cookies = {}
cookies['wzwstemplate'] = cookie1
function3_js = 'function' + jscode_list[3]
position = function3_js.index('{') +1
function3_js = function3_js[:position]+ var_ +function3_js[position:]
function3_py = js2py.eval_js(function3_js)
middle_var = function3_py()
cookie2 = function1_py(middle_var)
cookies['wzwschallenge'] = cookie2
dynamicurl = js2py.eval_js(var_list[0])
print(r.cookies.items())
r.cookies.update(cookies)
# print(cookies)
# temp = r.cookies.items()
# temp_c = dict(temp)
# cookies_ = {}
# for k, v in temp_c.items():
#     cookies_[k] = v
# print(cookies_)
print(dynamicurl)
# response = requests.get(url=host_url+dynamicurl, cookies=cookies)
# print(response.text)
content = r.get(host_url+dynamicurl).text

print(content)
