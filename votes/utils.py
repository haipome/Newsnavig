from models import Vote
from links.models import Link
from discusses.models import Discuss
from comments.models import Comment
from topics.utils import topic_ship_update
from django.utils import timezone
from nng.settings import HOT_RATE, BOUTIQUE_RATE
from dynamic.models import Dynamic
from nng.settings import WAY_LINK_TOPIC_POST, WAY_DISCUSS_TOPIC_POST
from globalvars.utils import get_averages

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

def vote_obj(user, obj):
	'''
	'''
	v = Vote.objects.filter(user=user, object_id=obj.id)
	if v:
		return v[0]
	
	if not isinstance(obj, Link) and \
	   not isinstance(obj, Discuss) and \
	   not isinstance(obj, Comment):
		return False
	
	if user == obj.user:
		return True
	
	data = obj.user.userdata
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
			topic_ship_update(topic, obj.user, domain=obj.domain, is_vote=True)
	elif isinstance(obj, Discuss):
		for topic in obj.topics.all():
			topic_ship_update(topic, obj.user, is_vote=True)
	
	obj.n_supporter += 1
	
	if isinstance(obj, Link):
		
		average_sum = 0
		
		for topic in obj.topics.all():
			if obj.n_supporter >= int(HOT_RATE * \
			                          topic.link_average_votes) + 1:
				column = topic.get_column()
				if not Dynamic.objects.filter(
				       column=column).filter(
				       object_id=obj.id).count():
					Dynamic.objects.create(column=column,
					                       way=WAY_LINK_TOPIC_POST,
					                       content_object=obj)
			
			average_sum += topic.link_average_votes
		
		count = obj.topics.count()
		if count:
			average = average_sum * 1.0 / count
		else:
			average = get_averages().link_average_votes
		
		if obj.n_supporter >= int(BOUTIQUE_RATE * average) + 1:
			if average != 0:
				obj.is_boutique = True
	
	
	elif isinstance(obj, Discuss):
		
		average_sum = 0
		
		for topic in obj.topics.all():
			if obj.n_supporter >= int(HOT_RATE * \
			                          topic.discuss_average_votes) + 1:
				column = topic.get_column()
				if not Dynamic.objects.filter(
				       column=column).filter(
				       object_id=obj.id).count():
					Dynamic.objects.create(column=column,
					                       way=WAY_DISCUSS_TOPIC_POST,
					                       content_object=obj)
			
			average_sum += topic.discuss_average_votes
		
		count = obj.topics.count()
		if count:
			average = average_sum * 1.0 / count
		else:
			average = get_averages().discuss_average_votes
		
		if obj.n_supporter >= int(BOUTIQUE_RATE * average) + 1:
			if average != 0:
				obj.is_boutique = True
	
	
	else:
		
		average_sum = 0
		
		for topic in obj.content_object.topics.all():
			average_sum += topic.comment_average_votes
		
		count = obj.content_object.topics.count()
		if count:
			average = average_sum * 1.0 / count
		else:
			average = get_averages().comment_average_votes
		
		if obj.n_supporter >= int(BOUTIQUE_RATE * average) + 1:
			if average != 0:
				obj.is_boutique = True
	
	obj.save()
	vote = Vote.objects.create(user=user, content_object=obj)
	
	
	return vote
	
