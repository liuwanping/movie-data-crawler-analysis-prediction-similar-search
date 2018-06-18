import requests
from bs4 import BeautifulSoup
import urllib
import re
from selenium import webdriver 
import time
import csv

#获取电影下载链接
def get_resource_link(bs,attri_list):   
    
    this_resourcelink_list = []

    url_div_list = bs.find_all("div", class_="downUrlList dUrlFlag ")

    for movieurl in url_div_list:
        key = movieurl.text.strip().replace('\r',' ').replace('\n',' ').replace('\t',' ')
        key = re.search(r"密码(.+?) ",key)        
        a_list = movieurl.select('a')
        for m_u in a_list:
            link = m_u["href"]
            if key!=None:
                link = link+" "+key.group().strip()
            this_resourcelink_list.append(link)
    
    t_r_l = None
    if this_resourcelink_list != []:  
        t_r_l = ", ".join(this_resourcelink_list)
    attri_list.append(t_r_l)#将下载链接加入属性列表
    
    print("get_resource_link finish")
    

#获取电影评论
def get_comment(bs,attri_list):
    
    comment_list = []
    
    comment_list_ul = bs.find_all('ul',class_="content")
    for comment in comment_list_ul:
        com = comment.text.strip()
        comment_list.append(com)#将评论加入属性列表
        
    comment_str = "".join(comment_list)
    attri_list.append(comment_str)
    
    filepath = 'F:/anaconda/Scripts/pachong/comment_data.csv'
    write_to_file(comment_list,filepath)
    print("get_comment finish")
    

    
#获取电影时长  
def get_length(bs,attri_list):

    bstext = bs.text.strip()    
    movie_length = re.search(r":(.+?)分钟",bstext)
    
    m_l = None
    if movie_length!=None:
        ml = movie_length.group()
        m_l = ml[1:len(ml)-2]

    attri_list.append(m_l)#将时长加入属性列表
    
    print("get_length finish")

#进入到电影页面里去获取电影时长，电影评论，电影下载链接
def get_inside_info(movie_url,attri_list):
    
    chromedriver = "F:/SoftPack/chromedriver.exe"#引入chromedriver.exe
    driver = webdriver.Chrome(chromedriver)
    driver.get(movie_url)#设置浏览器需要打开的url

    time.sleep(20) #加载时间较长，等待加载完毕
    
    #点击评论部分的“加载更多”进行翻页，取前三页评论
    for i in range(0,3):
        try:
            driver.find_element_by_id("loadCommentBtn").click() 
            time.sleep(5)
        except:
            break
        
    time.sleep(5) 
    
    bs = BeautifulSoup(driver.page_source, "lxml")
    
    get_length(bs,attri_list)#获取电影时长
    get_comment(bs,attri_list)#获取电影评论信息
    get_resource_link(bs,attri_list)#获取电影资源链接
    
    
    time.sleep(3)
    driver.close()
    
    print("get_inside_info finish")

def write_to_file(_list,filepath):
    with open(filepath,'a+',encoding='UTF-8',newline='') as csvfile:
        w = csv.writer(csvfile)
        w.writerow(_list)


#获取电影基本信息    
def get_movie_info(number,attri_list,comment_list):
    
    for i in range(1,101):

        #link = "http://www.pniao.com/Mov/movie/pn"+str(i)+".html"
        link = "http://www.pniao.com/Mov/movie/time/pn"+str(i)+".html"
        #link = "http://www.pniao.com/Mov/todayUp/pn"+str(i)+".html"
        r = requests.get(link)

        print(i,"返回码:",r.status_code)

        soup = BeautifulSoup(r.text,"lxml")

        movie_div_list = soup.find_all('div',class_ = 'movieFlag eachOne')
        for eachmovie in movie_div_list:
            
            print("movie"+str(number)+" is getting!!!")
            attri_list = [] #每个电影一个属性列表
            
            #获取电影的名字，年份，时长，评论，下载链接
            info_1_div = eachmovie.find_all('div',class_ = 'title')
            #print(info_1)
            for each in info_1_div:
                li_list = each.select('a')
                #print(li_list)
                for eachli in li_list:

                    title_year = eachli.text.strip()
                    n = " ".join(title_year.split()) #把电影名和电影年份拆开
                    #print(n)
                    movie_title = re.search(r"(.+?) ", n)
                    movie_year = re.search(".*\((.*)\).*",n)

                    m_n = None
                    if movie_title!=None:
                        m_n = movie_title.group().strip()                    
                    attri_list.append(m_n)#加入电影名属性

                    m_y = None
                    if movie_year!=None:
                        m_y = movie_year.group(1)
                    attri_list.append(m_y)#加入电影年份属性


                    movie_url = eachli["href"]
                    get_inside_info(movie_url,attri_list) #进入每个电影的页面去获取时长，评论，资源链接
                

            #获取电影的：导演，主演，分类，地区，豆瓣评分，观影计划人数
            info_2_div = eachmovie.find_all('div',class_='info')
            for each in info_2_div:
                eachinfo = each.text.strip().replace('\r',' ').replace('\n',' ').replace('\t',' ').split(" ")
                #print(eachinfo)
                if '导演:' in eachinfo and eachinfo[eachinfo.index('导演:')+1]!='':
                    attri_list.append(eachinfo[eachinfo.index('导演:')+1])
                else:
                    attri_list.append(None)
                if '主演:' in eachinfo and eachinfo[eachinfo.index('主演:')+1]!='':
                    attri_list.append(eachinfo[eachinfo.index('主演:')+1])
                else:
                    attri_list.append(None)
                if '分类:' in eachinfo and eachinfo[eachinfo.index('分类:')+1]!='':
                    this_genre_list = []#一个电影可能属于多个类别
                    item = eachinfo[eachinfo.index('分类:')+1]
                    while item != '' and item != '地区:':
                        this_genre_list.append(item)
                        item = eachinfo[eachinfo.index(item)+1]
                    attri_list.append(",".join(this_genre_list))#把多个类别转换成一个字符串存为一个属性
                else:
                    attri_list.append(None)            
                if '地区:' in eachinfo and eachinfo[eachinfo.index('地区:')+1]!='':
                    attri_list.append(eachinfo[eachinfo.index('地区:')+1])
                else:
                    attri_list.append(None)   
                if '豆瓣' in eachinfo and eachinfo[eachinfo.index('豆瓣')+1]!='':
                    attri_list.append(eachinfo[eachinfo.index('豆瓣')+1])
                else:
                    attri_list.append(None)
                if '+观影计划' in eachinfo:               
                    if eachinfo.index('+观影计划')+1 < len(eachinfo):                 
                        numstr = eachinfo[eachinfo.index('+观影计划')+1]
                        num = re.search(r"\d+\.?\d*",numstr).group()                        
                    else:
                        num = '0'
                    attri_list.append(num)                    
                else:                
                    attri_list.append('0')   


            #获取电影简介            
            brief_div_list = eachmovie.find_all('div',class_ = 'brief')
            for each in brief_div_list:
                brief = each.text.strip()
                attri_list.append(brief)
            
            #把这条电影数据写到文件里
            filepath = 'F:/anaconda/Scripts/pachong/movie_data.csv'
            write_to_file(attri_list,filepath)
            print("movie"+str(number)+" is getted!!!")
            number +=1

def main():      
    print("program start")
    
    attri_list = [] #每条电影数据一个属性列表，其中依次包含电影名1，电影年份2，导演3，主演4，类别5，区域6，豆瓣评分7，观看计划的人数8，简介9，资源下载链接10，电影时长11
    comment_list = [] #评论12

    number = 1
    get_movie_info(number,attri_list,comment_list)

    print("program finish")

main()