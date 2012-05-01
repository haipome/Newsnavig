from models import Vote
from links.models import Link
from discusses.models import Discuss
from comments.models import Comment
from topics.utils import topic_ship_update
from django.utils import timezone
from nng.settings import HOT_RATE, BOUTIQUE_RATE
from dynamic.models import Dynamic

def is_this_month(now, time):
	if not time:
		return False
	if now.year  == time.year and now.month == time.month:
		return True
	else:
		return False

def is_last_month(now, time):
	if not time:
		return False
	if now.year == time.year and (now.month - time.month) == 1:
		return True
	if (now.year - time.year) == 1 and (time.month - now.month) == 11:
		return True
	return False

def is_last2_month(now, time):
	if not time:
		return False
	if now.year == time.year and (now.month - time.month) == 2:
		return True
	if (now.year - time.year) == 1 and (time.month - now.month) == 10:
		return True
	return False

def vote(user, obj):
	'''
	'''
	if isinstance(obj, Link):
		to_user = obj.post_user
	elif isinstance(obj, Discuss):
		to_user = obj.start_user
	elif isinstance(obj, Comment):
		to_user = obj.user
	else:
		return False
	
	data = to_user.userdata
	data.honor += 1
	
	now = timezone.now()
	if is_this_month(now, data.this_month_start_time):
		data.this_month_vote += 1
	elif is_last_month(now, data.this_month_start_time):
		if not is_last2_month(now, data.last_month_start_time):
			data.last_month_half_votes = 0
		data.this_month_vote = (data.this_month_vote - last_month_half_votes) / 2
		data.last_month_half_votes = data.this_month_vote
		data.last_month_start_time = data.this_month_start_time
		data.this_month_start_time = now
		
		data.this_month_vote += 1
	else:
		data.this_month_vote = 1
		data.this_month_start_time = now
	data.save()
	
	if isinstance(obj, Link):
		for topic in obj.topics.all():
			topic_ship_update(topic, to_user, domain=obj.domain, is_vote=True)
	elif isinstance(obj, Discuss):
		for topic in obj.topics.all():
			topic_ship_update(topic, to_user, is_vote=True)
	
	obj.n_supporter += 1
	
	if isinstance(obj, Link):
		for topic in obj.topics:
			column = topic.get_column()
			if obj.n_supporter >= int(HOT_RATE * \
			                          topic.link_average_votes) + 1:
				if not Dynamic.objects.filter(
				       column=column).filter(
				       object_id=obj.id).count():
					Dynamic.objects.create(column=column,
					                       way=WAY_LINK_TOPIC_POST,
					                       content_object=discuss)
			if obj.n_supporter >= int(BOUTIQUE_RATE * \
			                          topic.link_average_votes) + 1:
				obj.is_boutique = True
	
	elif isinstance(obj, discuss):
		for topic in obj.topics:
			column = topic.get_column()
			if obj.n_supporter >= int(HOT_RATE * \
			                          topic.discuss_average_votes) + 1:
				if not Dynamic.objects.filter(
				       column=column).filter(
				       object_id=obj.id).count():
					Dynamic.objects.create(column=column,
					                       way=WAY_LINK_TOPIC_POST,
					                       content_object=discuss)
			if obj.n_supporter >= int(BOUTIQUE_RATE * \
			                          topic.discuss_average_votes) + 1:
				obj.is_boutique = True
	
	
	else:
		if obj.n_supporter >= int(BOUTIQUE_RATE * \
		                          topic.discuss_average_votes) + 1:
			obj.is_boutique = True
	
	
	obj.save()
	vote = Vote.objects.create(user=user, content_object=obj)
	
	
	return vote
	
