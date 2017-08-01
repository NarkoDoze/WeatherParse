#-*- coding: euc-kr -*-
import datetime
import requests
import re as regex
import json
import sys
d = datetime.date(2015, 12, 10)
dic = {}
li = [
    'weather', 'visible', 'cloud', 'mcloud', 'tempe', 'dew', 'stempe', 'rain', 'snow', 'humid', 'winddir', 'windspd', 'seapress'
]
while(True):
    ex = False
    d += datetime.timedelta(days=1)
    if d == datetime.date(2017, 7, 31):
        break
    print(d.isoformat())
    r = requests.get("http://www.kma.go.kr/weather/observation/currentweather.jsp?tm="+ d.isoformat().replace("-",".") +".23:00&type=t99&mode=0&auto_man=m&stn=152")
    s = ">"+str(d.day)+".(.*?)H</a></td>\r\n\t\t<td>(.*?)</td>\r\n\t\t\r\n\t\t<td>(.*?)</td>\r\n\t\t<td>(.*?)</td>\r\n\t\t<td>(.*?)</td>\r\n\t\t<td>(.*?)</td>\r\n\t\t<td>(.*?)</td>\r\n\t\t<td>(.*?)</td>\r\n\t\t<td>(.*?)</td>\r\n\t\t\r\n\t\t\t<td>(.*?)</td>\r\n\t\t\r\n\t\t<td>(.*?)</td>\r\n\t\t<td>(.*?)</td>\r\n\t\t<td>(.*?)</td>\r\n\t\t<td>(.*?)</td>"

    find = regex.findall(s, r.content.decode("euc-kr"))
    dic[d.isoformat().replace("-", "")] = [None]*24
    if not find:
        s = ">" + str(d.day) + ".(.*?)H</a></td>\r\n\t\t<td>(.*?)</td>\r\n\t\t\r\n\t\t<td>(.*?)</td>\r\n\t\t<td>(.*?)</td>\r\n\t\t<td>(.*?)</td>\r\n\t\t<td>(.*?)</td>\r\n\t\t<td>(.*?)</td>\r\n\t\t<td>(.*?)</td>\r\n\t\t<td>(.*?)</td>\r\n\t\t\r\n\t\t<td>(.*?)</td>\r\n\t\t<td>(.*?)</td>\r\n\t\t<td>(.*?)</td>\r\n\t\t<td>(.*?)</td>"
        find = regex.findall(s, r.content.decode("euc-kr"))
        ex = True

    for tu in find:
        l = [t if t != '&nbsp;' else '' for t in list(tu)]
        if ex:
            l = l[0:9] + [""] + l[9:13]
        try:
            dic[d.isoformat().replace("-", "")][int(l[0])] = {a: l[i+1] for i, a in enumerate(li)}
        except:
            sys.exit()

with open("weather.json", 'w', encoding='utf-8') as f:
    json.dump(dic, f, ensure_ascii=False, indent=4, separators=[',', ':'])