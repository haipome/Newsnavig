from comments.models import Comment
from globalvars.utils import get_available_id
from topics.utils import topic_ship_update
from links.models import Link
from discusses.models import Discuss
from dynamic.models import Dynamic
from nng.settings import *
from remind.utils import creat_remind

def post_comment(user, content, obj, parent=None):
	'''
	'''
	comment = Comment(id=get_available_id(),
	                  user=user,
	                  content=content,
	                  content_object=obj)
	
	if parent and isinstance(parent, Comment):
		comment.parent_comment = parent
		parent.n_comments += 1
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
		if isinstance(obj, Link):
			if user != obj.post_user:	
				creat_remind(obj.post_user, user, REMIND_NEW_COMMENT, comment)
		else:
			if user != obj.start_user:
				creat_remind(obj.start_user, user, REMIND_NEW_COMMENT, comment)
	
	if isinstance(obj, Link):
		Dynamic.objects.create(column=user.userprofile.get_column(),
		                       way=WAY_LINK_COMMENT,
		                       content_object=comment)
	
	if isinstance(obj, Discuss):
		Dynamic.objects.create(column=user.userprofile.get_column(),
		                       way=WAY_DISCUSS_COMMENT,
		                       content_object=comment)
	
	obj.n_comments += 1
	obj.save()
	
	
	return comment


def obj_cmp(obj1, obj2):
	if obj1.n_supporter != obj2.n_supporter:
		return -cmp(obj1.n_supporter, obj2.n_supporter)
	else:
		return -cmp(obj1.id, obj2.id)


def process(offset, length, l, all_l, add_to):
	
	base = length - 4
	o = offset % (2 * base)
	if o >= base:
		o = base - (o - base)
		
	for i in l:
		add_to.append((o, length - o, i))
		if i.n_comments:
			temp_l = []
			for j in all_l:
				if j.parent_comment_id == i.id:
					temp_l.append(j)
			if temp_l:
				temp_l.sort(obj_cmp)
				process(offset + 1, length, temp_l, all_l, add_to)

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
