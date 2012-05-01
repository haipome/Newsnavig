from django.db import models
from django.contrib.auth.models import User
from comments.models import Comment

class Remind(models.Model):
	'''
	'''
	to_user = models.ForeignKey(User, related_name="remind_list")
	from_user = models.ForeignKey(User, related_name="remind_yield_list")
	way = models.CharField(max_length=1)
	time = models.DateTimeField(auto_now_add=True)
	comment = models.ForeignKey(Comment, related_name="remind_comment",
	                            blank=True, null=True)
	is_read = models.BooleanField(default=False)
	
	class Meta:
		ordering = ['-id']
