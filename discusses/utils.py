from models import Discuss
from topics.models import Topic
from topics.utils import add_discuss_topic
from globalvars.utils import get_available_id
from dynamic.models import Dynamic
from models import DiscussIndex
from django.utils import timezone
from nng.settings import *
from django.utils.timezone import now
from data.models import UserData
from django.db.models import F
from django.core.cache import cache
from nng.settings import MESSAGES_PER_PAGE, PREFETCH_RATE, D_CACHE_AGE
from dynamic.utils import process_cache
from topics.utils import del_discuss_topic

def post_discuss(user, title, detail, topic_names):
	'''
	'''
	discuss = Discuss(id=get_available_id(),
	                  user=user,
	                  title=title,
	                  detail=detail)
	discuss.last_active_time = now()
	discuss.last_active_user = user
	discuss.save()
	
	for topic_name in topic_names:
		topic = add_discuss_topic(topic_name, user)
		discuss.topics.add(topic)
		
		column = topic.get_column()
		
		DiscussIndex.objects.create(column=column,
		                            way=WAY_DISCUSS_TOPIC_POST,
		                            discuss=discuss,
		                            last_active_time=timezone.now())
		
		if not FILTER:
			Dynamic.objects.create(column=column,
			                       way=WAY_DISCUSS_TOPIC_POST,
			                       content_object=discuss)
	
	user.userdata.discusses.add(discuss)
	
	DiscussIndex.objects.create(column=user.userprofile.get_column(),
	                            way=WAY_DISCUSS_USER_POST,
	                            discuss=discuss,
	                            last_active_time=timezone.now())
	
	Dynamic.objects.create(column=user.userprofile.get_column(),
	                       way=WAY_DISCUSS_USER_POST,
	                       content_object=discuss)
	
	UserData.objects.filter(user=user).update(n_discusses=F('n_discusses') + 1)
	
	return discuss


def del_discuss(d):
	if not isinstance(d, Discuss):
		return False
	
	if d.is_visible:
		d.is_visible = False
		d.save()
	
	data = d.user.userdata
	data.n_discusses -= 1
	data.save()
	
	for topic in d.topics.all():
		del_discuss_topic(d, topic)
	
	return True


def get_objs(follows, offset, n, s=None, e=None):
	
	if offset and n:
		discusses = DiscussIndex.objects.filter(
		            is_visible=True).filter(
		            id__lt=offset).filter(
		            column__in=follows).order_by(
		            '-last_active_time').all(
		            )[:n].prefetch_related(
		            'discuss__user__userprofile__avatar',
		            'column__content_object',
		            'last_active_user__userprofile',)
	else:
		discusses = DiscussIndex.objects.filter(
		            is_visible=True).filter(
		            column__in=follows).order_by(
		            '-last_active_time').all(
		            )[s:e].prefetch_related(
		            'discuss__user__userprofile__avatar',
		            'column__content_object',
		            'last_active_user__userprofile',)
	
	return discusses

def get_discusses(user, follows, page):
	
	key = str(user.id) + 'd'
	offset, logs, user_log = process_cache(key, page)
	
	n = int(MESSAGES_PER_PAGE * PREFETCH_RATE)
	if offset:
		objs = get_objs(follows, offset, n)
	else:
		s = n * (page - 1)
		e = s + n
		objs = get_objs(follows, offset=0, n=0, s=s, e=e)
	
	if not objs:
		return ([], False)
	
	discusses = []
	page_log = []
	counter = 0
	for obj in objs:
		counter += 1
		obj_id = obj.id
		i = obj.discuss_id
		if i not in logs:
			logs.append(i)
			page_log.append(i)
			discusses.append(obj)
	
	offset = obj_id
	user_log['offset'] = offset
	user_log['pre_page'] = page
	user_log[page] = page_log
	cache.set(key, user_log, D_CACHE_AGE)
	
	
	
	if counter == n:
		next_page = True
	else:
		next_page = False
	
	return (discusses, next_page)
	
