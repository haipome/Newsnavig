from models import Collect
from data.models import UserData
from django.db.models import F
from links.models import Link
from discusses.models import Discuss
from comments.models import Comment


def collect(user, obj):
	'''
	'''
	v = Collect.objects.filter(user=user, object_id=obj.id)
	if v:
		return v[0]
	
	try:
		obj.n_collecter += 1
		obj.save()
	except:
		return False
	
	UserData.objects.filter(user=user).update(n_collections=F('n_collections') + 1)
	
	collect = Collect(user=user, content_object=obj)
	
	comment_obj = None
	if isinstance(obj, Link):
		collect.way = 'l'
	elif isinstance(obj,  Discuss):
		collect.way = 'd'
	elif isinstance(obj, Comment):
		collect.way = 'c'
		collect.comment_object =obj.content_object
	else:
		return False
	
	collect.save()
	
	return collect
