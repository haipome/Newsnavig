from comments.models import Comment
from globalvars.utils import get_available_id
from topics.utils import topic_ship_update
from links.models import Link
from discusses.models import Discuss
from dynamic.models import Dynamic
from nng.settings import *

def post_comment(user, content, link_or_discuss, reply_to=None):
	'''
	'''
	comment = Comment(id=get_available_id(),
	                  user=user,
	                  content=content,
	                  content_object=link_or_discuss)
	
	if reply_to and isinstance(reply_to, Comment):
		comment.parent_comment = reply_to
		reply_to.n_reply += 1
		reply_to.save()
	
	topics = link_or_discuss.topics.all()
	if isinstance(link_or_discuss, Link):
		for topic in topics:
			topic_ship_update(topic=topic, user=user,
			                  domain=link_or_discuss.domain, is_comment=True)
	elif isinstance(link_or_discuss, Discuss):
		for topic in topics:
			topic_ship_update(topic=topic, user=user,
			                  is_comment=True)
	
	
	comment.save()
	
	if isinstance(link_or_discuss, Link):
		Dynamic.objects.create(column=user.userprofile.get_column(),
		                       way=WAY_LINK_COMMENT,
		                       content_object=comment)
	
	if isinstance(link_or_discuss, Discuss):
		Dynamic.objects.create(column=user.userprofile.get_column(),
		                       way=WAY_DISCUSS_COMMENT,
		                       content_object=comment)
	
	link_or_discuss.n_comments += 1
	link_or_discuss.save()
	
	return comment

