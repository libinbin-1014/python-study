import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import requests
import json
import math
import time
import re

class BraSpider(object):
	
	base_url = "https://sclub.jd.com/comment/productPageComments.action?productId=17209509645&score=0&sortType=5&pageSize=10&page=%d"

	def parse_comment(self, response, ret):
		content = json.loads(response.text)
		comments = content['comments']
		i = len(ret) + 1
		for comment in comments:
			item = {}
			item['content'] = comment['content']
			item['guid'] = comment['guid']
			item['id'] = comment['id']
			item['time'] = comment['referenceTime']
			item['color'] = comment['productColor']
			item['size'] = comment['productSize']
			item['userClientShow'] = comment['userClientShow']
			ret.insert(i, item)
			i = i + 1

	def parse_hot_tag(self, response, ret):
		content = json.loads(response.text)
		tags = content['hotCommentTagStatistics']
		for tag in tags:
			ret[tag['name']] = tag['count']


	def start_requests(self):
		comments_ret = []
		hot_tag_ret = {}
		ret = {}
		for page in range(1,100):
			url = self.base_url % page
			response = requests.get(url)
			if response.status_code == 200:
				self.parse_comment(response, comments_ret)
				if page == 1:
					self.parse_hot_tag(response, hot_tag_ret)
		ret['comments'] = comments_ret
		ret['tag'] = hot_tag_ret
		return ret

class data_parse(object):
	def dict2list(self, dic):
		keys = dic.keys()
		vals = dic.values()
		lst = [(key, val) for key, val in zip(keys, vals)]
		return sorted(lst, key=lambda x:x[1], reverse=True)  

	def phone_and_num(self, data):
		iphone_mobile_num = 0
		android_mobile_num = 0
		qq_mobile_num = 0
		weixin_num = 0
		others_num = 0
		ret = {}
		for item in data:
			if item['userClientShow'] == '来自京东iPhone客户端':
				iphone_mobile_num = iphone_mobile_num + 1
			elif item['userClientShow'] == '来自京东Android客户端':
				android_mobile_num = android_mobile_num + 1
			elif item['userClientShow'] == '来自微信购物':
				weixin_num = weixin_num + 1
			elif item['userClientShow'] == '来自手机QQ购物':
				qq_mobile_num = qq_mobile_num + 1
			else:
				print(item['userClientShow'])
				others_num = others_num + 1
		ret["iphone_mobile"]  =iphone_mobile_num
		ret["android_mobile"]  =android_mobile_num
		ret["qq_mobile"]  =qq_mobile_num
		ret["weixin"]  =weixin_num
		ret["others"]  =others_num
		return ret

	def product_color(self, data):
		black_color_num = 0
		red_color_num = 0
		coffer_color_num = 0
		white_color_num = 0
		violet_color_num = 0
		yellow_color_num = 0
		others_num = 0
		ret = {}
		for item in data:
			if item['color'] == '西瓜红色':
				red_color_num = red_color_num + 1
			elif item['color'] == '黑色':
				black_color_num = black_color_num + 1
			elif item['color'] == '咖啡色':
				coffer_color_num = coffer_color_num + 1
			elif item['color'] == '白色':
				white_color_num = white_color_num + 1
			elif item['color'] == '紫色':
				violet_color_num = violet_color_num + 1
			elif item['color'] == '米黄色':
				yellow_color_num = yellow_color_num + 1
			else:
				print(item['color'])
				others_num = others_num + 1
		ret['紫色'] = violet_color_num
		ret['白色'] = white_color_num
		ret['咖啡色'] = coffer_color_num
		ret['黑色'] = black_color_num
		ret['红色'] = red_color_num
		ret['黄色'] = yellow_color_num
		ret['others'] = others_num
		return ret

	def bar_size_list(self, data):
		size_70_A_num = 0
		size_70_B_num = 0
		size_75_A_num = 0
		size_75_B_num = 0
		size_75_C_num = 0
		size_80_A_num = 0
		size_80_B_num = 0
		size_80_C_num = 0
		size_80_D_num = 0
		size_85_B_num = 0
		size_85_C_num = 0
		size_90_D_num = 0
		size_90_C_num = 0
		size_95_C_num = 0
		size_95_D_num = 0
		ret = {}
		for item in data:
			if item['size'] == '75B':
				size_75_B_num = size_75_B_num + 1
			elif item['size'] == '75A':
				size_75_A_num = size_75_A_num + 1
			elif item['size'] == '75C':
				size_75_C_num = size_75_C_num + 1
			elif item['size'] == '70A':
				size_70_A_num = size_70_A_num + 1
			elif item['size'] == '70B':
				size_70_B_num = size_70_B_num + 1
			elif item['size'] == '80A':
				size_80_A_num = size_80_A_num + 1
			elif item['size'] == '80B':
				size_80_B_num = size_80_B_num + 1
			elif item['size'] == '80C':
				size_80_C_num = size_80_C_num + 1
			elif item['size'] == '90C':
				size_90_C_num = size_90_C_num + 1
			elif item['size'] == '85C':
				size_85_C_num = size_85_C_num + 1
			elif item['size'] == '90D':
				size_90_D_num = size_90_D_num + 1
			elif item['size'] == '80D':
				size_80_D_num = size_80_D_num + 1
			elif item['size'] == '85B':
				size_85_B_num = size_85_B_num + 1
			elif item['size'] == '95C':
				size_95_C_num = size_95_C_num + 1
			elif item['size'] == '95D':
				size_95_D_num = size_95_D_num + 1
			else:
				print(item['size'])
		ret['70A'] = size_70_A_num
		ret['70B'] = size_70_B_num
		ret['75A'] = size_75_A_num
		ret['75B'] = size_75_B_num
		ret['75C'] = size_75_C_num
		ret['80A'] = size_80_A_num
		ret['80B'] = size_80_B_num
		ret['80C'] = size_80_C_num
		ret['80D'] = size_80_D_num
		ret['85B'] = size_85_B_num
		ret['85C'] = size_85_C_num
		ret['90D'] = size_90_D_num
		ret['90C'] = size_90_C_num
		ret['95C'] = size_95_C_num
		ret['95D'] = size_95_D_num
		#return self.dict2list(ret)
		return ret

class jpg_create(object):
	def create_pie(self, name, title, labels, quants):
	    # make a square figure
	    plt.figure(1, figsize=(6,6))
	    # For China, make the piece explode a bit
	    expl = []
	    for i in labels:
	    	expl.append(0)
	    # Colors used. Recycle if not enough.
	    colors  = ["blue","red","coral","green","yellow","orange"]  #设置颜色（循环显示）
	    # Pie Plot
	    # autopct: format of "percent" string;百分数格式
	    plt.pie(quants, explode=expl, colors=colors, labels=labels, autopct='%1.1f%%',pctdistance=0.8, shadow=True)
	    plt.title(title, bbox={'facecolor':'0.8', 'pad':5})
	    plt.show()
	    plt.close()

	def create_branch(self, title, ylabel, scale, labels, quants):
	    zhfont = mpl.font_manager.FontProperties(fname='/usr/share/fonts/opentype/noto/ukai.ttc')
	    # 绘图
	    plt.bar(range(len(quants)), quants, align = 'center',color='red', alpha = 1)
	    # 添加轴标签
	    plt.ylabel(ylabel)
	    # 添加标题
	    plt.title(title,fontproperties=zhfont)
	    # 添加刻度标签s
	    plt.xticks(range(len(labels)),labels,fontproperties=zhfont)
	    # 设置Y轴的刻度范围
	    plt.ylim(scale)

	    # 为每个条形图添加数值标签
	    #for x,y in enumerate(quants):
	    #    plt.text(x,y+100,'%s' %round(y,1),ha='center')# 显示图形plt.show()
	    plt.show()
	    plt.close()
if __name__ == '__main__': 	
	s = BraSpider()
	data = s.start_requests()

	comments = data['comments']
	tags = data['tag']
	print(tags)
	parse = data_parse()

	phone_and_num = parse.phone_and_num(comments)
	print(phone_and_num)
	bar_size_list = parse.bar_size_list(comments)
	print(bar_size_list)
	color_num = parse.product_color(comments)
	print(color_num)

	jpg = jpg_create()
	jpg.create_branch("color", "num", [1,600], list(color_num.keys()), list(color_num.values()))
	#jpg.create_pie("phone_and_num", "which client use", list(phone_and_num.keys()), list(phone_and_num.values()))
	#jpg.create_branch("bar size", "num", [1,600],list(bar_size_list.keys()), list(bar_size_list.values()))
	#jpg.create_branch("tag", "num", [1,100],list(tags.keys()), list(tags.values()))


