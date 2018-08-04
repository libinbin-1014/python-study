#import scrapy
import requests
import json
import math
import time
import re

class BraSpider(object):
	
	base_url = "https://sclub.jd.com/comment/productPageComments.action?productId=17209509645&score=0&sortType=5&pageSize=20&page=%d"

	def parse(self, response):
		content = json.loads(response.text)
		comments = content['comments']
		for comment in comments:
			item = {}
			item['content'] = comment['content']
			item['guid'] = comment['guid']
			item['id'] = comment['id']
			item['time'] = comment['referenceTime']
			item['color'] = comment['productColor']
			item['size'] = comment['productSize']
			item['userClientShow'] = comment['userClientShow']
			print(item)

	def start_requests(self):
		for page in range(1,3):
			url = self.base_url % page
			response = requests.get(url)
			if response.status_code == 200:
				self.parse(response)

if __name__ == '__main__':
	s = BraSpider()
	s.start_requests()
