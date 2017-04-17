#coding:utf-8

import requests
import json

class Weather():
	def __init__(self,cityname):
		self.url = 'http://apis.baidu.com/apistore/weatherservice/cityname'
		self.headers = {'apikey':'5d60366fcef8b0aa7a2f9f0eb9fc72e4'}
		self.parm = {'cityname':cityname}

	def getWeather(self):
		row_data = requests.get( self.url, headers=self.headers, params=self.parm)
		data = row_data.json()
		if data['errNum']==0:
			result = data['retData']
			reply_content = result['city'] + u"今天的天气如下：\n天气：" + result['weather'] + u"\n气温：" + result['temp'] + u"\n最低气温：" + result['l_tmp'] + u"\n最高气温：" +result['h_tmp']
		else:
			reply_content = u'没有这个城市啊/::L'
		return reply_content
