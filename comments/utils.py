from comments.models import Comment
from globalvars.utils import get_available_id
from topics.utils import topic_ship_update
from links.models import Link
from discusses.models import Discuss
from dynamic.models import Dynamic
from nng.settings import *
from remind.utils import creat_remind
from django.utils import timezone
from discusses.models import DiscussIndex
from data.models import UserData
from django.db.models import F

def post_comment(user, content, obj, parent=None):
	'''
	'''
	comment = Comment(id=get_available_id(),
	                  user=user,
	                  content=content,
	                  content_object=obj)
	
	if parent and isinstance(parent, Comment):
		comment.parent_comment = parent
		parent.n_comment += 1
		parent.save()
	
	topics = obj.topics.all()
	if isinstance(obj, Link):
		comment.way = 'l'
		for topic in topics:
			topic_ship_update(topic=topic, user=user,
			                  domain=obj.domain, is_comment=True)
	elif isinstance(obj, Discuss):
		comment.way = 'd'
		for topic in topics:
			topic_ship_update(topic=topic, user=user,
			                  is_comment=True)
	else:
		return False
	
	comment.save()
	
	if parent and isinstance(parent, Comment):
		if user != parent.user:
			creat_remind(parent.user, user, REMIND_NEW_COMMENT, comment)
	else:
		if user != obj.user:
			creat_remind(obj.user, user, REMIND_NEW_COMMENT, comment)
	
	if isinstance(obj, Link):
		Dynamic.objects.create(column=user.userprofile.get_column(),
		                       way=WAY_LINK_COMMENT,
		                       content_object=comment,
		                       comment_object=obj)
	
	elif isinstance(obj, Discuss):
		Dynamic.objects.create(column=user.userprofile.get_column(),
		                       way=WAY_DISCUSS_COMMENT,
		                       content_object=comment,
		                       comment_object=obj)
		
		DiscussIndex.objects.filter(discuss=obj).update(
		                            last_active_time=timezone.now(),
		                            last_active_user=user)
		
		obj.last_active_time = timezone.now()
		obj.last_active_user = user
		
		if not user.userdata.discusses.filter(id=obj.id).count():
			user.userdata.discusses.add(obj)
		
	else:
		pass
	
	obj.n_comment += 1
	obj.save()
	
	UserData.objects.filter(user=user).update(n_comments=F('n_comments') + 1)
	
	return comment

def del_comment(c):
	if not isinstance(c, Comment):
		return False
	
	if c.is_visible:
		c.is_visible = False
		c.save()
	
	obj = c.content_object
	obj.n_comment -= 1
	obj.save()
	topics = obj.topics.all()
	if isinstance(obj, Link):
		for t in topics:
			topic_ship_update(topic=t, user=c.user,
				              domain=obj.domain, is_comment=True, num=-1)
	elif isinstance(obj, Discuss):
		for t in topics:
			topic_ship_update(topic=t, user=c.user,
			                  is_comment=True, num=-1)
	
	data = c.user.userdata
	data.n_comments -= 1
	data.save()
	
	if c.parent_comment:
		c.parent_comment.n_comment -= 1
		c.parent_comment.save()
	
	return True

def obj_cmp(obj1, obj2):
	if obj1.n_supporter != obj2.n_supporter:
		return -cmp(obj1.n_supporter, obj2.n_supporter)
	else:
		return cmp(obj1.id, obj2.id)

def get_offset(deep, length):
	offset = deep % (2 * length)
	if offset >= length:
		offset = length - (offset - length)
	
	return offset

def process(deep, length, l, all_l, add_to):
	
	o = get_offset(deep, length)
	
	for i in l:
		if i.is_visible == True:
			add_to.append((o, length - o, i))
		if i.n_comment:
			temp_l = []
			for j in all_l:
				if j.parent_comment_id == i.id:
					temp_l.append(j)
			if temp_l:
				temp_l.sort(obj_cmp)
				process(deep + 1, length, temp_l, all_l, add_to)

def comment_sort(comments, length):
	'''
	'''
	c_sorted = []
	
	no_parent_c = []
	for c in comments:
		if not c.parent_comment_id:
			no_parent_c.append(c)
	no_parent_c.sort(obj_cmp)
	
	process(0, length, no_parent_c, comments, c_sorted)
	
	return c_sorted


def comment_sort_common(comment, comments, length):
	'''
	'''
	c_sorted = []
	
	temp_l = []
	for c in comments:
		if c.parent_comment_id == comment.id:
			temp_l.append(c)
	
	if temp_l:
		temp_l.sort(obj_cmp)
		process(0, length, temp_l, comments, c_sorted)
	
	return c_sorted



