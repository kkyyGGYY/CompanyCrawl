import requests
import re
import jsbeautifier
import js2py

m_url = 'http://www.pbc.gov.cn/eportal/fileDir/defaultCurSite/resource/cms/2015/07/2010s09.htm'
session = requests.session()
content = session.get(m_url).content
tem_script = re.search(r'<script type="text/javascript">(?P<script>.*)</script>', content.decode('utf-8'), flags=re.DOTALL)
print tem_script.group('script')
result = jsbeautifier.beautify(tem_script.group('script').replace('\r\n', ''))

print result

js_code_list = result.split('function')
print js_code_list
var_ = js_code_list[0]
print var_
var_list = var_.split('\n')
template_js = var_list[3]
print template_js
template_py = js2py.eval_js(template_js)
print template_py
function1_js = 'function' + js_code_list[1]
print function1_js
position = function1_js.index('{') +1
print position
function1_js = function1_js[:position]+ var_ +function1_js[position:]
print '--', function1_js, '--'
function1_py = js2py.eval_js(function1_js)
print function1_py
cookie1 = function1_py(str(template_py))
print cookie1
# cookies = {}
# cookies['wzwstemplate'] = cookie1
# function3 = 'function' + js_code_list[3]
# position = function3.index('{') + 1
# function3 = function3[:position] + var_ + function3[position:]
# function3_py = js2py.eval_js(function3)
# middle_var = function3_py()
# cookie2 = function1_py(middle_var)
# cookies['wzwschallenge'] = cookie2
# fin_url = js2py.eval_js(var_list[0])
#
# session.cookies.update(cookies)
# url = 'http://www.pbc.gov.cn/'
# new_url = url + fin_url[1:]
# print new_url
# content = session.get(new_url).content.decode('gbk')
# print content
