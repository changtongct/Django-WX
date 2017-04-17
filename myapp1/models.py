from django.db import models

class QA(models.Model):
	questions = models.CharField(max_length=60)
	answers   = models.CharField(max_length=60)
	datetime  = models.DateTimeField()
	questTimes= models.IntegerField()

#	def __unicode__(self):
#		return self.name
