import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import requests
import json
import math
import time
import re

class BraSpider(object):
	
	base_url = "https://sclub.jd.com/comment/productPageComments.action?productId=11565382115&score=%d&sortType=5&page=%d&pageSize=10"
	def parse_comment(self, response, ret):
		content = json.loads(response.text)
		comments = content['comments']
		i = len(ret) + 1
		for comment in comments:
			item = {}
			#item['content'] = comment['content']
			#item['guid'] = comment['guid']
			#item['id'] = comment['id']
			#item['time'] = comment['referenceTime']
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
		for page in range(1,150):
			for i in range(0,6):
				url = self.base_url % (i, page)
				response = requests.get(url)
				if response.status_code == 200:
					self.parse_comment(response, comments_ret)

		ret['comments'] = comments_ret
		ret['tag'] = hot_tag_ret
		return ret

class data_parse(object):
	def dict2list(self, dic):
		keys = dic.keys()
		vals = dic.values()
		lst = [(key, val) for key, val in zip(keys, vals)]
		return sorted(lst, key=lambda x:x[1], reverse=True)  

	def size_num(self, size, ret):
		if size == '70B/32':
			ret['70B'] = ret['70B'] + 1
		elif size == '75B/34':
			ret['75B'] = ret['75B'] + 1
		elif size == '75C/34':
			ret['75C'] = ret['75C'] + 1
		elif size == '80B/36':
			ret['80B'] = ret['80B'] + 1
		elif size == '80C/36':
			ret['80C'] = ret['80C'] + 1
		elif size == '85B/38':
			ret['85B'] == ret['85B'] + 1
		elif size == '85C/38':
			ret['85C'] = ret['85C'] + 1
		elif size == '80D/36':
			ret['80D'] = ret['80D'] + 1
		elif size == '85D/38':
			ret['85D'] = ret['85D'] + 1
		elif size == '90D/40':
			ret['90D'] = ret['90D'] + 1
		else:
			print(size)

	def phone_and_num(self, data):
		iphone_mobile_num = 0
		android_mobile_num = 0
		ret = {}
		android_ret = {}
		android_ret['70B'] = 0
		android_ret['75B'] = 0
		android_ret['75C'] = 0
		android_ret['80B'] = 0
		android_ret['85B'] = 0
		android_ret['80C'] = 0
		android_ret['80D'] = 0
		android_ret['85C'] = 0
		android_ret['85D'] = 0
		android_ret['90D'] = 0
		
		iphone_ret = {}
		iphone_ret['70B'] = 0
		iphone_ret['75B'] = 0
		iphone_ret['75C'] = 0
		iphone_ret['80B'] = 0
		iphone_ret['85B'] = 0
		iphone_ret['80C'] = 0
		iphone_ret['80D'] = 0
		iphone_ret['85C'] = 0
		iphone_ret['85D'] = 0
		iphone_ret['90D'] = 0
		
		for item in data:
			if item['userClientShow'] == '来自京东iPhone客户端' and iphone_mobile_num < 1000:
				iphone_mobile_num = iphone_mobile_num + 1
				self.size_num(item['size'], iphone_ret)
			elif item['userClientShow'] == '来自京东Android客户端' and android_mobile_num < 1000:
				android_mobile_num = android_mobile_num + 1
				self.size_num(item['size'], android_ret)
			if android_mobile_num >= 1000 and iphone_mobile_num >= 1000:
				break
		android_ret['all'] = android_mobile_num
		iphone_ret['all'] = iphone_mobile_num
		ret["iphone"]  = iphone_ret
		ret["android"]  = android_ret
		return ret

	def product_color(self, data):
		ret = {}
		ret[u'紫色'] = 0
		ret[u'白色'] = 0
		ret[u'银灰'] = 0
		ret[u'黑色'] = 0
		ret[u'红色'] = 0
		ret[u'黄色'] = 0
		ret[u'肤色'] = 0
		ret[u'蓝色'] = 0
		ret[u'粉色'] = 0
		for item in data:
			if item['color'] == '肤色' or item['color'] == '肤色（薄模杯）':
				ret['肤色'] = ret['肤色'] + 1
			elif item['color'] == '宝蓝':
				ret['蓝色'] = ret['蓝色'] + 1
			elif item['color'] == '黑色':
				ret['黑色'] = ret['黑色'] + 1
			elif item['color'] == '黑色（薄模杯）':
				ret['黑色'] = ret['黑色'] + 1
			elif item['color'] == '大红':
				ret['红色'] = ret['红色'] + 1
			elif item['color'] == '紫灰' or item['color'] == '紫灰（薄模杯）':
				ret[u'紫色'] = ret[u'紫色'] + 1
			elif item['color'] == '银灰':
				ret['银灰'] =  ret['银灰'] + 1
			elif item['color'] == '豆沙粉（厚模杯）':
				ret['粉色'] = ret['粉色'] + 1
			else:
				print(item['color'])

		return ret


class jpg_create(object):
	def create_double_branch(self, title, ylabels, xlabels, iphone, android):
		index = np.arange(len(android))
		width = 0.3
 
		plt.bar(left=index, height=iphone, width=width, color='yellow', label=u'iphone')
		plt.bar(left=index+width, height=android, width=width, color='red', label=u'android')
		plt.ylabel(ylabels)
		plt.xticks(range(len(xlabels)),xlabels)
		plt.title(title)
		plt.legend(loc='best')
		plt.show()


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
	    plt.bar(range(len(quants)), quants, align = 'center', width=0.3, color='red', alpha = 1)
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
	
	parse = data_parse()
	color_num = parse.product_color(comments)
	print(color_num)

	phone_and_num = parse.phone_and_num(comments)
	#phone_size = {'iphone': {'85D': 45, '70B': 83, '80C': 77, '80D': 29, '85C': 121, 'all': 1000, '85B': 0, '75C': 52, '90D': 69, '75B': 286, '80B': 238}, 'android': {'85D': 43, '70B': 49, '80C': 95, '80D': 19, '85C': 158, 'all': 1000, '85B': 0, '75C': 45, '90D': 52, '75B': 263, '80B': 275}}
	print(phone_size)

	iphone_size = phone_and_num['iphone']
	android_size = phone_and_num['android']

	xlabels = ['70B', '75B', '75C', '80B', '80C', '80D', '85B', '85C', '85D', '90D']
	iphone = []
	android = []
	bars_number = []
	for item in xlabels:
		iphone.append(iphone_size[item])
		android.append(android_size[item])
		bars_number.append(iphone_size[item] + android_size[item])

	jpg = jpg_create()
	jpg.create_double_branch('phone and size','counts', xlabels, iphone, android)



	#jpg.create_branch("color", "num", [1,600], list(color_num.keys()), list(color_num.values()))
	#jpg.create_pie("phone_and_num", "which client use", list(phone_and_num.keys()), list(phone_and_num.values()))
	#jpg.create_branch("bar size", "num", [1,600], xlabels, bars_number)
	jpg.create_branch("color", "num", [1,1500],list(color_num.keys()), list(color_num.values()))
	

