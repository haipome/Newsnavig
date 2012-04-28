from models import Discuss
from topics.models import Topic
from topics.utils import add_discuss_topic
from globalvars.utils import get_available_id
from dynamic.models import Dynamic
from nng.settings import *

def post_discuss(user, title, detail, topic_names):
	'''
	'''
	discuss = Discuss(id=get_available_id(),
	                  start_user=user,
	                  title=title,
	                  detail=detail)
	
	for topic_name in topic_names:
		topic = add_discuss_topic(topic_name, user)
		discuss.topics.add(topic)
	
	discuss.save()
	
	for topic in discuss.topics.all():
		Dynamic.objects.create(column=topic.get_column(),
		                       way=WAY_DISCUSS_TOPIC_POST,
		                       content_object=discuss)
	
	Dynamic.objects.create(column=user.userprofile.get_column(),
	                       way=WAY_DISCUSS_USER_POST,
	                       content_object=discuss)
	
	return discuss
