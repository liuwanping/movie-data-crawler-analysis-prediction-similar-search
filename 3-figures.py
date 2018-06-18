# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pygal_maps_world.maps


plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

#从文件里读取数据
movie_repeat_df = pd.DataFrame(pd.read_csv('F:/anaconda/Scripts/pachong/data/data.csv',encoding = 'gb18030'))
movie_df = movie_repeat_df.drop_duplicates() 


#统计各个国家电影平均分并画出世界地图
def get_country_score_map(): 
    country_score_df = movie_df.groupby("地区")["评分"].mean().sort_values(ascending=False) #获得各个国家的电影平均分，并使其降序排列
    country_dict = dict(zip(list(country_score_df.index),list(country_score_df)))
    print(country_dict)
    #8.5-8.9
    country_score0 = {'bw': 8.6, 'kz': 8.6, 'si': 8.6}
    #8.0-8.4
    country_score1 = {'br': 8.475, 'gr': 8.299999999999999, 'ir': 8.254545454545454,'ge': 8.2, 'dz': 8.2, 'hr': 8.2,'lu': 8.2,  'dk': 8.158333333333333, 'cz': 8.127272727272727, 'lb': 8.1, 'uy': 8.1, 'co': 8.1, 'sk': 8.1, 'se': 8.016666666666666}
    #7.5-7.9
    country_score2 = {'ru': 7.9864864864864895, 'ie': 7.984615384615385, 'in': 7.966666666666664, 'de': 7.925000000000002, 'at': 7.925, 'is': 7.9, 'gb': 7.8829545454545435, 'fi': 7.869230769230769, 'pl': 7.8687499999999995, 'fr': 7.863999999999998, 'ro': 7.859999999999999, 'cl': 7.85, 'jp': 7.80064724919094, 'pe': 7.8, 'it': 7.753846153846154, 'tw': 7.747368421052633, 'au': 7.718750000000001, 'vn': 7.7, 'il': 7.7, 'mx': 7.688888888888889, 'us': 7.673662551440326, 'ar': 7.672727272727272, 'ch': 7.633333333333333, 'yu': 7.6000000000000005, 'pt': 7.55, 'ph': 7.5}
    #<7.4
    country_score3 = {'ca': 7.462499999999999, 'be': 7.45, 'tr': 7.375000000000001, 'ee': 7.333333333333333, 'nl': 7.32, 'th': 7.3166666666666655, 'kr': 7.229268292682926, 'es': 7.220689655172414, 'bg': 7.2, 'hu': 7.159999999999999, 'cn': 7.06666666666667, 'hk': 7.0609929078014195,'no': 6.975, 'nz': 6.9, 've': 6.7, 'rs': 5.3, 'sg': 5.1}
    
    wm = pygal_maps_world.maps.World()
    wm.title = '各个国家电影平均分'
    wm.add('8.5分-8.9分',country_score0)
    wm.add('8.0分-8.4分',country_score1)
    wm.add('7.5分-7.9分',country_score2)
    wm.add('7.4分以下',country_score3)
    wm.render_to_file('F:/anaconda/Scripts/pachong/figures/各个国家平均分.svg')
get_country_score_map()


#统计一个国家各个分数段的电影
def get_country_movnum():
    china_df = movie_df.loc[movie_df["地区"] == "中国大陆"]#把中国的电影选出来
    ser1 = china_df.groupby("评分")["电影名"].count()#统计各个分数段的电影数量
    score = list(ser1.index)#横轴各个分数
    num = list(ser1)#纵轴电影数量
    plt.bar(score,num, width=0.3 , color='moccasin')
    plt.title('中国各个分数的电影数量')
    plt.xlabel('评分')
    plt.ylabel('电影数量')
    plt.savefig('F:/anaconda/Scripts/pachong/figures/中国各个分数的电影数量.png',bbox_inches = 'tight')
    plt.show()
get_country_movnum()


#统计全球及几个国家随年份变化的电影评分趋势
def get_rating_year():
    world_rating_ser = movie_df.groupby("年份")["评分"].mean()#全球电影平均分随时间变化
    year1 = list(world_rating_ser.index)
    world_trend = list(world_rating_ser)

    china_df = movie_df.loc[movie_df["地区"] == "中国大陆"]#中国电影平均分随时间变化
    china_rating_ser = china_df.groupby("年份")["评分"].mean()
    year2 = list(china_rating_ser.index)
    china_trend = list(china_rating_ser)
    
    uk_df = movie_df.loc[movie_df["地区"] == "英国"]#英国电影平均分随时间变化
    uk_rating_ser = uk_df.groupby("年份")["评分"].mean()
    year4 = list(uk_rating_ser.index)
    uk_trend = list(uk_rating_ser)
    
    plt.plot(year1[-20:],world_trend[-20:],color='red',label='全球')
    plt.plot(year2[-20:],china_trend[-20:],color='orange',label='中国大陆')
    plt.plot(year4[-20:],uk_trend[-20:],color='teal',label='英国')
    
    plt.title('全球及各国家电影评分随时间变化情况')
    plt.xlabel('年份')
    plt.ylabel('评分的平均分')
    plt.legend() # 显示图例
    plt.grid() # 显示网格
    plt.savefig('F:/anaconda/Scripts/pachong/figures/全球及各国家电影评分随时间变化情况.png')
    plt.show()
get_rating_year()


#统计各个年份导演的数量
def get_director_year():
    director_ser = movie_df.groupby("年份")["导演"].value_counts()#统计各个年份全球导演数量
    year_dire = {}
    for each in list(director_ser.index):
        if each[0] in year_dire:
            year_dire[each[0]] += 1
        else:
            year_dire[each[0]] = 1 
    year = list(year_dire.keys())
    direcnum = list(year_dire.values()) 
    
    china_df = movie_df.loc[movie_df["地区"] == "中国大陆"]#把中国的电影选出来
    china_director_ser = china_df.groupby("年份")["导演"].value_counts()#统计各个年份中国导演数量
    year_dire1 = {}
    for each in list(china_director_ser.index):
        if each[0] in year_dire1:
            year_dire1[each[0]] += 1
        else:
            year_dire1[each[0]] = 1 
    year1 = list(year_dire1.keys())
    direcnum1 = list(year_dire1.values()) 
    
    uk_df = movie_df.loc[movie_df["地区"] == "英国"]#把英国的电影选出来
    uk_director_ser = uk_df.groupby("年份")["导演"].value_counts()#统计各个年份英国导演数量
    year_dire2 = {}
    for each in list(uk_director_ser.index):
        if each[0] in year_dire2:
            year_dire2[each[0]] += 1
        else:
            year_dire2[each[0]] = 1 
    year2 = list(year_dire2.keys())
    direcnum2 = list(year_dire2.values()) 
    
    plt.plot(year[-20:],direcnum[-20:],color='red',label='全球')
    plt.plot(year1[-20:],direcnum1[-20:],color='orange',label='中国大陆')
    plt.plot(year2[-20:],direcnum2[-20:],color='royalblue',label='英国')
    
    plt.title('各地区导演数量随时间变化情况')
    plt.xlabel('年份')
    plt.ylabel('导演数量')
    plt.legend() # 显示图例 
    plt.grid() # 显示网格
    plt.savefig('F:/anaconda/Scripts/pachong/figures/各地区导演数量随时间变化情况.png')
    plt.show()
get_director_year()


#统计各个导演拍电影数量，按照倒叙排列
def director_movnum():   
    director_num_ser = movie_df.groupby("导演").count()#统计各个年份全球导演数量
    top_director_num_ser = director_num_ser.loc[director_num_ser["电影名"] >= 7 ].sort_index(axis = 0,ascending = False,by = '电影名')  
    direc = list(reversed(list(top_director_num_ser.index)))
    mov_num = list(reversed(list(top_director_num_ser["电影名"])))
    
    #（1）统计每个导演的电影数量，先选中(1)执行，画出一个图
    fig, ax = plt.subplots()
    ax.barh(direc, mov_num)
    labels = ax.get_xticklabels()
    plt.setp(labels, rotation=45, horizontalalignment='right')
    ax.set(xlabel='电影数量', ylabel='导演',title='各导演拍电影数量大比拼')
    plt.savefig('F:/anaconda/Scripts/pachong/figures/各导演拍电影数量大比拼.png')

    #（2）统计每个导演的评分，绘制上面是评分，下面是数量的柱状图，再选中(2)执行画出另一个图
    direc_score_ser = movie_df.groupby("导演")["评分"].mean()
    mov_score = []
    for each in direc:
        mov_score.append(direc_score_ser[each])
    plt.bar(direc,np.array(mov_score),facecolor='#9999ff',edgecolor='white',label='电影评分')
    plt.bar(direc,-np.array(mov_num),facecolor='#ff9999',edgecolor='white',label='电影数量')
    for x,y in zip(direc,mov_score):
        plt.text(x,y,'%.0f' % y,ha='center',va='bottom') #ha=horizonal alignment
    for x,y in zip(direc,mov_num):
        plt.text(x,-y,'-%.0f' % y,ha='center',va='top') #ha=horizonal alignment
    plt.xticks(())
    plt.yticks(())
    plt.title('各导演的电影评分与电影数量大比拼')
    plt.savefig('F:/anaconda/Scripts/pachong/figures/各导演的电影评分与电影数量大比拼.png',bbox_inches = 'tight')
    plt.show()
director_movnum()


#统计各个时长段电影的数量
def get_movnum_length():
    length = ['70-79分钟','80-89分钟','90-99分钟','100-109分钟','110-109分钟','110-109分钟','110-119分钟','120-129分钟','130-139分钟','140分钟以上']
    length_num = []
    length_num.append(len(movie_df.loc[(movie_df["时长"]>=str(70)) & (movie_df["时长"]<str(79))]))
    length_num.append(len(movie_df.loc[(movie_df["时长"]>=str(80)) & (movie_df["时长"]<str(89))]))
    length_num.append(len(movie_df.loc[(movie_df["时长"]>=str(90)) & (movie_df["时长"]<str(99))]))
    length_num.append(len(movie_df.loc[(movie_df["时长"]>=str(100)) & (movie_df["时长"]<str(109))]))
    length_num.append(len(movie_df.loc[(movie_df["时长"]>=str(110)) & (movie_df["时长"]<str(119))]))
    length_num.append(len(movie_df.loc[(movie_df["时长"]>=str(120)) & (movie_df["时长"]<str(129))]))
    length_num.append(len(movie_df.loc[(movie_df["时长"]>=str(130)) & (movie_df["时长"]<str(139))]))
    length_num.append(len(movie_df.loc[movie_df["时长"]>str(140)]))
    plt.bar(range(1,9),np.array(length_num),color='lightgreen')
    plt.xticks(range(1,9),length,rotation=90)  ## 可以设置坐标字 
    plt.title('各时长段电影的数量')
    plt.xlabel('时长')
    plt.ylabel('电影数量')
    plt.savefig('F:/anaconda/Scripts/pachong/figures/各时长段电影的数量.png',bbox_inches = 'tight')
    plt.show()
get_movnum_length()


#统计各种类型电影占比，画出饼状图
def genre_percent():
    genre_num ={'剧情':0,'喜剧':0,'爱情':0,'惊悚':0,'动画':0,'动作':0,'同性':0,'其他':0}
    cat_df = movie_df.dropna(subset=["分类"])["分类"]
    for each in cat_df:
        if '剧情' in each:
            genre_num['剧情'] +=1
        if '喜剧' in each:
            genre_num['喜剧'] +=1
        if '爱情' in each:
            genre_num['爱情'] +=1
        if ('惊悚' in each) or ('恐怖' in each):
            genre_num['惊悚'] +=1
        if '动作' in each:
            genre_num['动作'] +=1
        if '动画' in each:
            genre_num['动画'] +=1
        if '同性' in each:
            genre_num['同性'] +=1
        else:
            genre_num['其他'] +=1
    labels = '剧情','喜剧','爱情','惊悚','动画','动作','同性','其他'
    explode = [0, 0, 0, 0, 0.1, 0, 0.1, 0]#突出动画和同性
    colors=['cornflowerblue','lightblue','lightskyblue','royalblue','blue','dodgerblue','darkblue','lightsteelblue']
    plt.pie(list(genre_num.values()), labels=labels,explode=explode,colors=colors,labeldistance = 1.1,shadow = False)
    plt.axis('equal')
    plt.title('不同类型电影大比拼')
    plt.savefig('F:/anaconda/Scripts/pachong/figures/不同类型电影大比拼.png',bbox_inches = 'tight')
    plt.show()
genre_percent()



#各国拍摄动画电影大比拼
def carton_counrtry_percent():
    cat_dropna_df = movie_df.dropna(subset=["分类"])
    cun_lovenum = {}
    for indexs in cat_dropna_df.index:
        if '动画' in cat_dropna_df.loc[indexs].values[7]:
            if cat_dropna_df.loc[indexs].values[8] in cun_lovenum.keys():
                cun_lovenum[cat_dropna_df.loc[indexs].values[8]] +=1
            else:
                cun_lovenum[cat_dropna_df.loc[indexs].values[8]] = 1

    cun_lovenum_top = sorted(cun_lovenum.items(),key = lambda x:x[1],reverse = True)
    print(dict(cun_lovenum_top[0:7]))
    labels = '日本','美国','中国大陆','奥地利','英国','加拿大','法国'   
    lovenum = list(dict(cun_lovenum_top[0:7]).values())
    colors=['hotpink','violet','orchid','pink','palevioletred','mediumvioletred','deeppink']
    plt.pie(lovenum, labels=labels,colors=colors,labeldistance = 1.1,shadow = False,startangle=60)
    plt.axis('equal')
    plt.title('各国拍摄动画类电影大比拼')
    plt.tight_layout(pad=0.1, w_pad=0.5, h_pad=1.0)
    plt.savefig('F:/anaconda/Scripts/pachong/figures/各国拍摄动画类电影大比拼.png',bbox_inches = 'tight')
    plt.show()
carton_counrtry_percent()


#同性类的电影数量随时间变化
def lgbt_year():
    lgbt_df = movie_df.groupby("年份").count()
    year_lgbtnum = {}
    movie_dropna_df = movie_df.dropna(subset=["分类"])#去掉分类为空的
    for eachyear in list(lgbt_df.index):
        thisyear_df = movie_dropna_df.loc[ movie_df["年份"] == eachyear]
        for eachindex in thisyear_df.index:
            if '同性' in thisyear_df.loc[eachindex].values[7]:          
                if eachyear in year_lgbtnum:
                    year_lgbtnum[eachyear] += 1
                else:
                    year_lgbtnum[eachyear] = 1
    for eachyear in list(lgbt_df.index):
        if eachyear not in year_lgbtnum.keys():
            year_lgbtnum[eachyear] = 0 
    year20_lgbtnum = sorted(year_lgbtnum.items(),key = lambda x:x[0],reverse = True)
    print(year20_lgbtnum[0:20])
    year20_lgbtnum_list = []
    for each in year20_lgbtnum[0:20]:
        year20_lgbtnum_list.append(each[1])
    print(year20_lgbtnum_list)
    plt.plot(range(1999,2019),sorted(year20_lgbtnum_list),color='hotpink')
    plt.title('近20年同性题材电影变化趋势')
    plt.xlabel('年份')
    plt.ylabel('电影数量')
    plt.savefig('F:/anaconda/Scripts/pachong/figures/近20年同性题材电影变化趋势.png')
    plt.show()
lgbt_year()


#统计各分数段电影数量
def movnum_percent():
    movie_repeat_df = pd.DataFrame(pd.read_csv('F:/anaconda/Scripts/pachong/data/data.csv',encoding = 'gb18030',keep_default_na=False))#加一个参数，把NAN变成空，否则老是报错
    movie_df = movie_repeat_df.drop_duplicates() 
    m1 = movie_df.loc[(movie_df["评分"]>=str(9))]
    m2 = movie_df.loc[(movie_df["评分"]>=str(8))]
    m3 = movie_df.loc[(movie_df["评分"]>=str(7))]
    m4 = movie_df.loc[(movie_df["评分"]>=str(6))]
    m5 = movie_df.loc[(movie_df["评分"]<str(6))]
    n1 = len(m1)
    n2 = len(m2)-len(m1)
    n3 = len(m3)-len(m2)
    n4 = len(m4)-len(m3)
    n5 = len(m5)
    n_list = []
    n_list.append(n1)
    n_list.append(n2)
    n_list.append(n3)
    n_list.append(n4)
    n_list.append(n5)
    print(n_list)
    labels = '9分以上','8分-8.9分','7分-7.9分','6分-6.9分','6分以下'   
    colors=['darkgreen','seagreen','darkolivegreen','forestgreen','limegreen']
    plt.pie(n_list, labels=labels,colors=colors,labeldistance = 1.1,shadow = False,startangle=60)
    plt.axis('equal')
    plt.title('各分数段电影占比')
    plt.tight_layout(pad=0.1, w_pad=0.5, h_pad=1.0)
    plt.savefig('F:/anaconda/Scripts/pachong/figures/各分数段电影占比.png',bbox_inches = 'tight')
    plt.show()
movnum_percent()


#统计2018年top10电影
def get_top2018():
    movie_repeat_df = pd.DataFrame(pd.read_csv('F:/anaconda/Scripts/pachong/data/data.csv',encoding = 'gb18030',keep_default_na=False))
    movie_df = movie_repeat_df.drop_duplicates(['电影名']) 
    thisyear = movie_df.loc[(movie_df["年份"] == "2018")].sort_values(by="评分" , ascending=False)
    name = [""]
    score = ["8"]
    name = name + (list(reversed(list(thisyear['电影名'])[0:10])))
    score = score + (list(reversed(list(thisyear['评分'])[0:10])))
#    name = ['超感猎杀：完结特别篇 ','机动战士高达THE ORIGIN 赤色彗星诞生','头号玩家','燃烧','信笺故事','红海行动','爱你，西蒙','养家之人','爱在记忆消逝前','现在去见你']
#    score = [9.4,9.1,8.9,8.8,8.6,8.5,8.4,8.3,8.2,8.2]
    fig, ax = plt.subplots()
    ax.barh(list(reversed(name)), list(reversed(score)))
    labels = ax.get_xticklabels()
    plt.setp(labels, horizontalalignment='right')
    ax.set_xticks(range(0,11))   
    ax.set(xlabel='评分',title='2018年到目前为止的top10电影')
    plt.savefig('F:/anaconda/Scripts/pachong/figures/2018年到目前为止的top10电影.png')
get_top2018()


#统计电影受欢迎度和评分之间的关系
def get_popu_rating():
    x_values = list(movie_df["计划观看人数"])
    y_values = list(movie_df["评分"])    
    plt.scatter(x_values,y_values,s = 10)
    plt.title("电影受欢迎度与评分之间的关系")
    plt.xlabel("计划观看人数")
    plt.ylabel("电影评分")
    plt.show()
    plt.savefig('F:/anaconda/Scripts/pachong/figures/电影受欢迎度与评分之间的关系.png',bbox_inches = 'tight')
get_popu_rating()






