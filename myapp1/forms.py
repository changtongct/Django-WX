#coding:utf-8

from django import forms

class AddForm(forms.Form):
	a = forms.IntegerField()
	b = forms.IntegerField()

class QAForm(forms.Form):
	question = forms.CharField(label=u'问题')
	answer	 = forms.CharField(label=u'回答')

class QADelete(forms.Form):
	delete = forms.IntegerField(label=u'id号')

