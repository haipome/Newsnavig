from models import Topic
from links.models import Link
from discusses.models import Discuss
from comments.models import Comment
import datetime
from django.utils.timezone import now
from nng.settings import AVERAGE_TIME
from django.db.models import Avg, Count
from globalvars.utils import get_averages


def cal_comment_avg(topic, start_time):
	links = topic.topic_links.filter(
	        is_visible=True).filter(
	        time__gt=start_time).all(
	        ).values('comments__is_visible', 'comments__n_supporter')
	discusses = topic.topic_discusses.filter(
	            is_visible=True).filter(
	            time__gt=start_time).all(
	            ).values('comments__is_visible', 'comments__n_supporter')
	
	n_comments = 0
	n_comments_votes = 0
	
	for c in links:
		if c['comments__is_visible']:
			n_comments  += 1
			n_comments_votes += c['comments__n_supporter']
	
	for c in discusses:
		if c['comments__is_visible']:
			n_comments  += 1
			n_comments_votes += c['comments__n_supporter']
	
	if n_comments == 0:
		return 0
	return n_comments_votes * 1.0 / n_comments


def cal_average_vote():
	'''
	'''
	start_time = now() - datetime.timedelta(days=AVERAGE_TIME)
	
	for topic in Topic.objects.all():
		topic.link_average_votes = topic.topic_links.filter(
		                           is_visible=True).filter(
		                           time__gt=start_time).all(
		                           ).aggregate(Avg('n_supporter')
		                           )['n_supporter__avg']
		
		topic.discuss_average_votes = topic.topic_discusses.filter(
		                              is_visible=True).filter(
		                              time__gt=start_time).all(
		                              ).aggregate(Avg('n_supporter')
		                              )['n_supporter__avg']
		
		topic.comment_average_votes = cal_comment_avg(topic, start_time)
		
		if topic.link_average_votes == None:
			topic.link_average_votes = 0
		if topic.discuss_average_votes == None:
			topic.discuss_average_votes = 0
		
		topic.save()
	
	g = get_averages()
	
	g.link_average_votes = Link.objects.filter(
	                       is_visible=True).filter(
	                       time__gt=start_time).all(
	                       ).aggregate(Avg('n_supporter')
	                       )['n_supporter__avg']
	
	g.discuss_average_votes = Discuss.objects.filter(
	                           is_visible=True).filter(
	                           time__gt=start_time).all(
	                           ).aggregate(Avg('n_supporter')
	                           )['n_supporter__avg']
	
	g.comment_average_votes = Comment.objects.filter(
	                          is_visible=True).filter(
	                           time__gt=start_time).all(
	                           ).aggregate(Avg('n_supporter')
	                           )['n_supporter__avg']
	
	if g.link_average_votes == None:
		g.link_average_votes = 0
	if g.discuss_average_votes == None:
		g.discuss_average_votes = 0
	if g.comment_average_votes == None:
		g.comment_average_votes = 0
	
	g.save()
	


