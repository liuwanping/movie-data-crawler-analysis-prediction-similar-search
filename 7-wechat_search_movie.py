# -*- coding: utf-8 -*-

import werobot
import pymongo


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["movieDB"]
mycol = mydb["linkSim"]

robot = werobot.WeRoBot(token='mytoken')

@robot.handler

def hello(message):
	flag = 0
	res = mycol.find({"title":message.content})
	for x in res:
		flag = 1
		title = x["title"]
		link = x["link"]
		sim_list = x["sim"]
		sim_str = ""
		for each in sim_list:
			sim_mov = mycol.find({"movID":each})
			for each_sim_mov in sim_mov:
				sim_str = sim_str + "\n" + "《" + each_sim_mov["title"] + "》" + "\n" + each_sim_mov["link"] + "\n" + "******************************"
		result ="《"+ title + "》" + "\n" + link + "\n\n" + "我们相似推荐还有:" + "\n" + "*****************************" + sim_str 
		return result
	if flag == 0:
		return "抱歉没有找到这部电影"

robot.config['HOST'] = '0.0.0.0'

robot.config['PORT'] = 80

robot.run()

