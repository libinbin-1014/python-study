import requests
import json

class Computer(object):
	baseUrl = "https://sclub.jd.com/comment/productPageComments.action?productId=6949959&score=%d&sortType=5&page=%d&pageSize=30"
	def CommentParse(self, data, ret):
		content = json.loads(str(data.text))
		comments = content['comments']
		for comment in comments:
			item = {}
			item['id'] =  comment['id']
			item['time'] = comment['referenceTime']
			item['color'] = comment['productColor']
			item['userlevel'] = comment['userLevelName']
			item['client'] = comment['userClientShow']
			
			ret[item['id']] = item


	def Start(self):
		comments_ret = []
		hot_tag_ret = {}
		ret = {}
		for page in range(1,120):
			for i in range(0, 6):
				url = self.baseUrl %  (i, page)
				response = requests.get(url)
				if response.status_code == 200:
					self.CommentParse(response, ret)
		return ret


class Parse(object):
	def LevelNum(self, level, ret):
		if level == '金牌会员':
			ret['gold'] = ret['gold'] + 1
		elif level == 'PLUS会员':
			ret['Plus'] = ret['Plus'] + 1
		elif level == '银牌会员':
			ret['silver'] = ret['silver'] + 1
		elif level == '钻石会员':
			ret['diamond'] = ret['diamond'] + 1
		elif level == '注册会员':
			ret['register'] = ret['register'] + 1
		elif level == '铜牌会员':
			ret['copper'] = ret['copper'] + 1

	def PhoneAndLevel(self, data):
		AndroidNum = 0
		IphoneNum = 0
		ret = {}
		AndroidLevel = {}
		IphoneLevel = {}
		AndroidLevel['Plus'] = 0
		AndroidLevel['gold'] = 0
		AndroidLevel['silver'] = 0
		AndroidLevel['diamond'] = 0
		AndroidLevel['copper'] = 0
		AndroidLevel['register'] = 0
		IphoneLevel['Plus'] = 0
		IphoneLevel['gold'] = 0
		IphoneLevel['silver'] = 0
		IphoneLevel['diamond'] = 0
		IphoneLevel['copper'] = 0
		IphoneLevel['register'] = 0
		for item in data:
			if data[item]['client'] == '来自京东Android客户端' and AndroidNum < 500:
				AndroidNum = AndroidNum + 1
				self.LevelNum(data[item]['userlevel'], AndroidLevel)
			elif data[item]['client'] == '来自京东iPhone客户端' and IphoneNum < 500:
				IphoneNum = IphoneNum + 1
				self.LevelNum(data[item]['userlevel'], IphoneLevel)
			if AndroidNum >= 500 and IphoneNum >= 500:
				break

		AndroidLevel['all'] = AndroidNum
		IphoneLevel['all'] = IphoneNum
		ret['Android'] = AndroidLevel
		ret['Iphone'] = IphoneLevel
		print(ret)

if __name__ == '__main__':
	Com = Computer()
	data = Com.Start()

	Parse = Parse()
	Parse.PhoneAndLevel(data)

