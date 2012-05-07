from models import Discuss
from topics.models import Topic
from topics.utils import add_discuss_topic
from globalvars.utils import get_available_id
from dynamic.models import Dynamic
from models import DiscussIndex
from django.utils import timezone
from nng.settings import *
from django.utils.timezone import now

def post_discuss(user, title, detail, topic_names):
	'''
	'''
	discuss = Discuss(id=get_available_id(),
	                  user=user,
	                  title=title,
	                  detail=detail)
	
	for topic_name in topic_names:
		topic = add_discuss_topic(topic_name, user)
		discuss.topics.add(topic)
	
	discuss.last_active_time = now()
	discuss.last_active_user = user
	
	discuss.save()
	user.userdata.discusses.add(discuss)
	
	for topic in discuss.topics.all():
		
		DiscussIndex.objects.create(column=topic.get_column(),
		                            way=WAY_DISCUSS_TOPIC_POST,
		                            discuss=discuss,
		                            last_active_time=timezone.now())
	
	DiscussIndex.objects.create(column=user.userprofile.get_column(),
	                            way=WAY_DISCUSS_USER_POST,
	                            discuss=discuss,
	                            last_active_time=timezone.now())
	
	Dynamic.objects.create(column=user.userprofile.get_column(),
	                       way=WAY_DISCUSS_USER_POST,
	                       content_object=discuss)
	
	return discuss


def get_discusses(follows, s, e):
	
	discusses = DiscussIndex.objects.filter(
	            is_visible=True).filter(
	            column__in=follows).order_by(
	            '-last_active_time').all(
	            )[s:e].prefetch_related(
	            'discuss__user__userprofile__avatar',
	            'column__content_object',
	            'last_active_user__userprofile',)
	
	return discusses
	
