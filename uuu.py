import requests
import re
import jsbeautifier
import js2py
#
m_url = 'http://datamining.comratings.com/exam'
session = requests.get(m_url)
print session.cookies.items()[0]
session_str = session.cookies.items()[0][1]
# session = '7fefa345d5d04ebdb1bb46fba53ff016'
print session_str
# content = session.get(m_url).content
# print content
# tem_script = re.search(r'<script>(?P<script>.*)</script>', content.decode('utf-8'), flags=re.DOTALL)

# print tem_script.group('script')
# a = '''eval(function(p,a,c,k,e,r){e=function(c){return(c<a?'':e(parseInt(c/a)))+((c=c%a)>35?String.fromCharCode(c+29):c.toString(36))};if(!''.replace(/^/,String)){while(c--)r[e(c)]=k[c]||e(c);k=[function(e){return r[e]}];e=function(){return'\\w+'};c=1};while(c--)if(k[c])p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c]);return p}('n z(a){5 b=e.o;5 c=b.u("; ");R(5 i=0;i<c.F;i++){5 d=c[i].u("=");g(a==d[0]){j d[1]}}j""}m=z(\'m\');5 7="13+/=";I=v.Z;n p(a){5 b,i,k;5 c,f,l;k=a.F;i=0;b="";M(i<k){c=a.q(i++)&T;g(i==k){b+=7.8(c>>2);b+=7.8((c&r)<<4);b+="==";A}f=a.q(i++);g(i==k){b+=7.8(c>>2);b+=7.8(((c&r)<<4)|((f&B)>>4));b+=7.8((f&C)<<2);b+="=";A}l=a.q(i++);b+=7.8(c>>2);b+=7.8(((c&r)<<4)|((f&B)>>4));b+=7.8(((f&C)<<2)|((l&Q)>>6));b+=7.8(l&V)}j b}n G(){5 w=9.N||e.K.L||e.J.L;5 h=9.O||e.K.E||e.J.E;g(w*h<=P){j D}5 x=9.S;5 y=9.U;g(x+w<=0||y+h<=0||x>=9.H.W||y>=9.H.X){j D}j Y}n s(){g(G()){}10{5 a="";a="11="+p(m.12(1,3))+"; t=/";e.o=a;a="f="+p(m)+"; t=/";e.o=a;9.v=I}}s();',62,66,'|||||var||encoderchars|charAt|window|||||document|c2|if|||return|len|c3|session|function|cookie|f1|charCodeAt|0x3|reload|path|split|location||||getCookie|break|0xf0|0xf|true|clientHeight|length|findDimensions|screen|url|body|documentElement|clientWidth|while|innerWidth|innerHeight|120000|0xc0|for|screenX|0xff|screenY|0x3f|width|height|false|href|else|c1|substr|ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'.split('|'),0,{}))'''.replace('\r\n', '')
a = '''eval(function(p,a,c,k,e,r){e=function(c){return(c<a?'':e(parseInt(c/a)))+((c=c%a)>35?String.fromCharCode(c+29):c.toString(36))};if(!''.replace(/^/,String)){while(c--)r[e(c)]=k[c]||e(c);k=[function(e){return r[e]}];e=function(){return'\\w+'};c=1};while(c--)if(k[c])p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c]);return p}('n z(a){5 b=e.o;5 c=b.u("; ");R(5 i=0;i<c.F;i++){5 d=c[i].u("=");g(a==d[0]){j d[1]}}j""}m=z(\'m\');5 7="13+/=";I=v.Z;n p(a){5 b,i,k;5 c,f,l;k=a.F;i=0;b="";M(i<k){c=a.q(i++)&T;g(i==k){b+=7.8(c>>2);b+=7.8((c&r)<<4);b+="==";A}f=a.q(i++);g(i==k){b+=7.8(c>>2);b+=7.8(((c&r)<<4)|((f&B)>>4));b+=7.8((f&C)<<2);b+="=";A}l=a.q(i++);b+=7.8(c>>2);b+=7.8(((c&r)<<4)|((f&B)>>4));b+=7.8(((f&C)<<2)|((l&Q)>>6));b+=7.8(l&V)}j b}n G(){5 w=9.N||e.K.L||e.J.L;5 h=9.O||e.K.E||e.J.E;g(w*h<=P){j D}5 x=9.S;5 y=9.U;g(x+w<=0||y+h<=0||x>=9.H.W||y>=9.H.X){j D}j Y}n s(){g(G()){}10{5 a="";a="11="+p(m.12(1,3))+"; t=/";e.o=a;a="f="+p(m)+"; t=/";e.o=a;9.v=I}}s();',62,66,'|||||var||encoderchars|charAt|window|||||document|c2|if|||return|len|c3|session|function|cookie|f1|charCodeAt|0x3|reload|path|split|location||||getCookie|break|0xf0|0xf|true|clientHeight|length|findDimensions|screen|url|body|documentElement|clientWidth|while|innerWidth|innerHeight|120000|0xc0|for|screenX|0xff|screenY|0x3f|width|height|false|href|else|c1|substr|ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'.split('|'),0,{}))'''
result = jsbeautifier.beautify(a)
var = 'var encoderchars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";'
# print result

func_list = result.split('function')
func_f1 = func_list[2]

position = func_f1.index('{') + 1
function1_js ='function' + func_f1[:position] + var + func_f1[position:]
print function1_js

function1_py = js2py.eval_js(function1_js)
c2 = function1_py(str(session_str))


c1 = function1_py(session_str[1:4])

print c1
cookies = {}
cookies['c1'] = c1
cookies['c2'] = c2
cookies['session'] = session_str
session.cookies.update(cookies)

content = requests.get(m_url, cookies=cookies).content
print content