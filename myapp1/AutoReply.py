#coding:utf-8

import datetime
import re
from models import QA
from ThirdPartyAPI import Weather

def autoReply(content):
	if re.search(u"问：",content) and re.search(u"；答：",content):
		reply_content = teach(content)
	elif re.search(u"天气",content):
		reply_content = weather(content)
	else:
		reply_content = reply(content)
	return reply_content

def reply(content):
	temps = QA.objects.all()
	search_result = []
	temp_result = None
        for temp in temps:
		temp_result = re.search(temp.questions,content)
		if temp_result != None:
			search_result.append(temp)
			temp_result = None
	
	if len(search_result) == 1:
		reply_content = search_result[0].answers
		quest_times = search_result[0].questTimes
		quest_times += 1
		a = QA.objects.filter(questions=search_result[0].questions)
		a.update(questTimes = quest_times)
	elif len(search_result) == 0:
		reply_content = u"不知道怎么回答呢^_^"
		f = open("questions.txt","a+")
		f.write(content.encode('utf-8')+'\n')
		f.close()
	else:
		reply_content = u"回答哪个呢..."
	
	return  reply_content

def teach(content):
	p = re.compile(u'问：|；答：')
	p = p.split(content)
	QA.objects.create(questions=p[1],answers=p[2],datetime=datetime.datetime.now(),questTimes=0)
	reply_content = u"多谢指教，我记住啦"
	return reply_content

def weather(content):
	cityname = re.sub(u"天气","",content)
	a = Weather(cityname)
	reply_content = a.getWeather()
	return reply_content


def questTimesReset():
	QA.objects.all().update(questTimes=0)

#import re  
#source = "s2f程序员杂志一2d3程序员杂志二2d3程序员杂志三2d3程序员杂志四2d3"  
#temp = source.decode('utf8')  
#xx=u"([\u4e00-\u9fa5]+)"  
#pattern = re.compile(xx)  
#results =  pattern.findall(temp)  
#for result in results :  
#  print result













def aautoReply(content):
        values = {
                u"几点"		:datetime.datetime.now().strftime("%H点%M分%S秒"),
                u"时间"		:datetime.datetime.now().strftime("%H点%M分%S秒"),
		u"日期"		:datetime.datetime.now().strftime("%Y年%m月%d日，星期%w"),
		u"星期"		:datetime.datetime.now().strftime("星期%w"),
		u"天气"		:u"不错呦",
#		u"":u"",
#		u"":u"",
#		u"":u"",
#		u"":u"",
        }

#       content = content.decode('utf-8')
#       pattern = re.compile(content)
        search_result = None
        for key in values.keys():
                search_result = re.search(key,content)
                if search_result!=None:
                        reply_content = values[search_result.group()]
                        break
	if search_result==None:
		reply_content =  u"不知道怎么回答呢^_^"
		f = open("questions.txt","a+")
		f.write(content.encode('utf-8')+'\n')
		f.close()
	return reply_content
