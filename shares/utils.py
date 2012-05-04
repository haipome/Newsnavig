from links.models import Link
from discusses.models import Discuss
from comments.models import Comment
from dynamic.models import Dynamic
from models import Share
from nng.settings import *

def post_share(user, obj):
	'''
	'''
	v = Share.objects.filter(user=user, object_id=obj.id)
	if v:
		return v[0]
	
	d = Dynamic(column=user.userprofile.get_column(),
	            content_object=obj)
	
	if isinstance(obj, Link):
		d.way = WAY_LINK_SHARE
		if user == obj.post_user:
			return True
	elif isinstance(obj, Discuss):
		d.way = WAY_DISCUSS_SHARE
		if user == obj.start_user:
			return True
	elif isinstance(obj, Comment):
		if user == obj.user:
			return True
		if isinstance(obj.content_object, Link):
			d.way = WAY_LINK_COMMENT_SHARE
		elif isinstance(obj.content_object, Discuss):
			d.way = WAY_DISCUSS_COMMENT_SHARE
		else:
			return False
	else:
		return False
	
	d.save()
	
	obj.n_shares += 1
	obj.save()
	
	share = Share.objects.create(user=user, content_object=obj)
	
	return share
