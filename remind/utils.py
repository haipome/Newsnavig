from models import Remind
from data.models import UserData
from django.db.models import F

def creat_remind(to_user, from_user, way, comment=None):
	'''
	'''
	Remind.objects.create(to_user=to_user, 
	                      from_user=from_user,
	                      way=way,
	                      comment=comment)
	
	to_user.userdata.un_read_remind += 1
	to_user.userdata.n_reminds += 1
	to_user.userdata.save()
	
