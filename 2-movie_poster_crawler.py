import urllib.request
import os
from bs4 import BeautifulSoup

os.chdir(r'E:\1-graduate\3-curriculum\10-数据挖掘\poster')
url ='http://www.pniao.com/Mov/movie/pn'

links = []
name = 486


for i in range(1,50):
    print(i)
    res = urllib.request.urlopen(url+str(i)+".html")
    html = res.read()
    soup = BeautifulSoup(html,'html.parser', from_encoding='utf-8')
    result = soup.find_all('img')
    for x in result:
        links.append(x.get('data-url'))
    
    
print(links)
for link in links:
    if link!=None:
        urllib.request.urlretrieve(link, str(name)+".jpg")
        name+=1
        
print("finish")