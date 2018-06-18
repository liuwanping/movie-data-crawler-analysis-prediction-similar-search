# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from scipy import spatial #用来计算两个向量间的余弦相似度
import pymongo



#找到所有类别
def find_generos(x):
    generos = []
    for index, row in x.iterrows():
        gen_list = row['分类'].replace(" ", "").split(',')
        for i in gen_list:
            if i not in generos:
                generos.append(i)
    print(generos)

#找到电影评分的最大值，最小值，平均值
def rating_info(movie_dict): 
    ratings = []
    for i in movie_dict:
        ratings.append(movie_dict[i][1])
    print("the average is: ", np.mean(ratings))
    print("the minumum is: ", np.min(ratings))
    print("the max is: ", np.max(ratings))

#找到电影评分的最大值，最小值，平均值
def popularity_info(movie_dict):
    popularity = []
    for i in movie_dict:
        popularity.append(movie_dict[i][2])
    print("the average is: ", np.mean(popularity))
    print("the minumum is: ", np.min(popularity))
    print("the max is: ", np.max(popularity))

#把一个电影的多个分类用一个向量表示
def get_gen_vector(gen):
    gen_vector = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    gen_list = gen.split(',')
    for i in gen_list:
        if '剧情' in gen_list:
            gen_vector[0] = 1
        if '爱情' in gen_list:
            gen_vector[1] = 1
        if '短片' in gen_list:
            gen_vector[2] = 1
        if '恐怖' in gen_list:
            gen_vector[3] = 1
        if '悬疑' in gen_list:
            gen_vector[4] = 1
        if '动作' in gen_list:
            gen_vector[5] = 1
        if '喜剧' in gen_list:
            gen_vector[6] = 1
        if '歌舞' in gen_list:
            gen_vector[7] = 1
        if '犯罪' in gen_list:
            gen_vector[8] = 1
        if '惊悚' in gen_list:
            gen_vector[9] = 1
        if '家庭' in gen_list:
            gen_vector[10] = 1
        if '情色' in gen_list:
            gen_vector[11] = 1
        if '西部' in gen_list:
            gen_vector[12] = 1
        if '音乐' in gen_list:
            gen_vector[13] = 1
        if '科幻' in gen_list:
            gen_vector[14] = 1
        if '同性' in gen_list:
            gen_vector[15] = 1
        if '冒险' in gen_list:
            gen_vector[16] = 1
        if '传记' in gen_list:
            gen_vector[17] = 1
        if '战争' in gen_list:
            gen_vector[18] = 1
        if '历史' in gen_list:
            gen_vector[19] = 1
        if '武侠' in gen_list:
            gen_vector[20] = 1
        if '奇幻' in gen_list:
            gen_vector[21] = 1
        if '舞台剧' in gen_list:
            gen_vector[22] = 1
        if '动画' in gen_list:
            gen_vector[23] = 1
        if '运动' in gen_list:
            gen_vector[24] = 1
        if '黑色电影' in gen_list:
            gen_vector[25] = 1
        if '儿童' in gen_list:
            gen_vector[26] = 1
        if '灾难' in gen_list:
            gen_vector[27] = 1
        if '古装' in gen_list:
            gen_vector[28] = 1
    return gen_vector


#对所有电影进行整理，获得其电影名，评分，计划观看人数，分类向量，movID,下载链接
def movie_dict(x):
    movies_dict = {}
    movie_id = 0
    for index, row in x.iterrows():
        gen_vector = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        gen_vector = get_gen_vector(row['分类'])
        title = row['电影名']
        vote_average = row['评分']
        popularity = row['计划观看人数'] 
        link = row['下载链接']
        if np.linalg.norm(gen_vector) != 0:
            movie_id += 1
            movies_dict[title] = (title, vote_average, popularity, gen_vector, movie_id, link)
    return movies_dict

#计算两个电影之间的距离
def get_distance(movie1, movie2):
    gen_movie1 = movie1[3]
    gen_movie2 = movie2[3]
    movie1_rating = movie1[1] / 10
    movie2_rating = movie2[1] / 10
    movie1_popular = movie1[2] / 1225
    movie2_popular = movie2[2] / 1225
    distance_popular = abs(movie1_popular - movie2_popular)
    distance_rating = abs(movie1_rating - movie2_rating)
    distance_gen = spatial.distance.cosine(gen_movie1, gen_movie2)
    distance = (0.5 * distance_gen) + (0.3 * distance_rating) + (0.2 * distance_popular)
    return distance



#找到某部电影最近的5个邻居
def neighbors(movie_dict, N): 
    neighbors = pd.DataFrame(columns=['电影名','距离','下载链接',"movID"])
    counter = 0
    for i in movie_dict:
        counter += 1
        title = movie_dict[i][0]
        link = movie_dict[i][5]
        distance = get_distance(movie_dict[N], movie_dict[i])
        movID = movie_dict[i][4]
        #print(distance)
        neighbors.loc[counter] = [title, distance,link,movID]
    neighbors = neighbors.sort_values(by=['距离'])
    return neighbors.head(6)

#控制台交互部分，找到一部电影的五个最近的邻居
def search_neighbors():
    movietitle = input("请输入想要查找的电影名：")
    if movietitle not in movie_dict.keys():
        print("没有这部电影")
        return
    print()
    print("正在拼命查找...")   
    x = neighbors(movie_dict, movietitle)
    print()
    for each in x.index:
        if x.loc[each]["电影名"] == movietitle:
            print("相似的电影有：")
            print("***************************************************")
        else:
            print(x.loc[each]["电影名"],"，距离为：",x.loc[each]["距离"],"链接为：")
    print("***************************************************")

#把每个电影的movID,电影名，下载链接，5个邻居的movID作为一条记录写入数据库，为微信公众号检索用
def write_neighbors_toDB():
    print("begin")
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["movieDB"]
    mycol = mydb["movLinkSim"]
    counter = 1
    for i in movie_dict:
        print(counter)
        if mycol.find_one({"title":movie_dict[i][0]}):
            print("skip")
            continue
        else:
            print("writing")
            z = neighbors(movie_dict, movie_dict[i][0])
            link = movie_dict[i][5].split(", ")[0]
            movdict = {"movID":movie_dict[i][4],"title":movie_dict[i][0],"link":link,"sim":list(z["movID"])[1:]}
            mycol.insert_one(movdict)
        counter+=1
    print("finish")

full_table = pd.read_csv("data.csv", header = 0,encoding = 'gb18030') 
table = pd.DataFrame(full_table[['电影名', '评分', '计划观看人数', '分类','下载链接']]).drop_duplicates(['电影名']).dropna(subset=["分类"]).dropna(subset=["评分"]).dropna(subset=["计划观看人数"]).dropna(subset=["下载链接"])
#find_generos(table)
movie_dict = movie_dict(table) 
#rating_info(movie_dict)
#popularity_info(movie_dict)
#search_neighbors()
write_neighbors_toDB()

