#coding:utf-8
from django.shortcuts import render

import hashlib
import xml.etree.ElementTree as ET
from django.http import HttpResponse
from django.views.generic.base import View
from django.views.decorators.csrf import csrf_exempt
import time
import datetime
from django.shortcuts import render_to_response,render
import urllib
import urllib2
import json
from django.core import serializers
from forms import *
from models import QA
from AutoReply import *

def index(request):
	if request.method == 'POST':
		form = AddForm(request.POST)
		if form.is_valid():
			a = form.cleaned_data['a']
			b = form.cleaned_data['b']
		return HttpResponse(str(int(a)+int(b)))
	else:
		form = AddForm()
		return render(request,'home.html',{'form':form})

def QAdisplay(request):
	if request.method == 'POST':
		if request.POST.has_key("questTimesRe"):
			QA.objects.all().update(questTimes=0)
		elif request.POST.has_key("addQA"):
			QAform = QAForm(request.POST)
			if QAform.is_valid():
				question = QAform.cleaned_data['question']
				answer   = QAform.cleaned_data['answer']
				QA.objects.create(questions=question,answers=answer,datetime=datetime.datetime.now(),questTimes=0)
		elif request.POST.has_key("deleteQA"):
			QAdelete = QADelete(request.POST)
			if QAdelete.is_valid():
				delete_id = QAdelete.cleaned_data['delete']
				QA.objects.filter(id=delete_id).delete()
		else:
			pass
		QAform = QAForm()
		QAdelete = QADelete()
		qas = serializers.serialize("json",QA.objects.all())
		return render(request,'QAdisplay.html',{'QAform':QAform,'QAdelete':QAdelete,'qas':qas})
	else:
		QAform = QAForm()
		QAdelete = QADelete()
		qas = serializers.serialize("json",QA.objects.all())
		return render(request,'QAdisplay.html',{'QAform':QAform,'QAdelete':QAdelete,'qas':qas})


class wx(View):

	def __init__(self):
		self.TOKEN = 'changtong'
		self.AppId = 'wxc0b235ffde29419c'
		self.AppSecret = '60459676ba3c1d3440617bb1f7d2aedb'
		self.token()
#自定义菜单，木有权限	self.createMenu()

	def get(self,request,*args,**kwargs):
		signature = request.GET.get("signature",None)
		timestamp = request.GET.get("timestamp",None)
		nonce 	  = request.GET.get("nonce"    ,None)
		echostr   = request.GET.get("echostr"  ,None)
		temp_list = [ self.TOKEN, timestamp, nonce]
		temp_list.sort()
		temp_str  = "%s%s%s" % tuple(temp_list)
		temp_str  = hashlib.sha1(temp_str).hexdigest()
		if temp_str == signature:
			return HttpResponse(echostr)
		else:
			return HttpResponse(self.access_token)
		
	def post(self,request,*args,**kwargs):
		str_xml = request.body
		xml = 	ET.fromstring(str_xml)
		toUserName   = xml.find("ToUserName").text
		fromUserName = xml.find("FromUserName").text
		createTime   = xml.find("CreateTime").text
		msgType      = xml.find("MsgType").text
		content      = xml.find("Content").text

		reply = '''
		<xml>
		<ToUserName>%s</ToUserName>
		<FromUserName>%s</FromUserName>
		<CreateTime>%s</CreateTime>
		<MsgType>%s</MsgType>
		<Content>%s</Content>
		</xml>
		''' % (fromUserName,toUserName,str(int(time.time())),msgType,autoReply(content))
		return HttpResponse(reply,content_type="application/xml")

#	@csrf_exempt
	def dispatch(self,*args,**kwargs):
		return super(wx,self).dispatch(*args,**kwargs)

	def token(self):
		url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (self.AppId, self.AppSecret)  
    		result = urllib2.urlopen(url).read()  
    		self.access_token = json.loads(result).get('access_token')  

	def createMenu(self):
		url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % self.access_token
		data = {
		"button":[
			{
			"name":"yy",
			"sub_button":[
				{
				"type":"click",
				"name":"图片",
				"key" :"image"
				},
				{
				"type":"view",
				"name":"search",
				"url":"http://www.baidu.com"
				}]
			}]
		}
		#data = json.loads(data)
		#data = urllib.urlencode(data)  
        	req = urllib2.Request(url)  
        	req.add_header('Content-Type', 'application/json')  
        	req.add_header('encoding', 'utf-8')  
        	response = urllib2.urlopen(req, json.dumps(data,ensure_ascii=False))  
        	self.result = response.read()  
