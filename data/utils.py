from django.contrib.contenttypes.models import ContentType
from models import FollowShip

def get_follows(user):
	'''
	'''
	user_type   = ContentType.objects.get(app_label='profiles', model='userprofile')
	topic_type  = ContentType.objects.get(app_label='topics',   model='topic')
	domain_type = ContentType.objects.get(app_label='domains',  model='domain')
	
	ships = FollowShip.objects.filter(
	          userdata=user.userdata).order_by(
	          '-time').all(
	          ).prefetch_related(
	          'column__content_object__avatar',
	          'column__content_object')
	
	follows = []
	follows_user = []
	follows_topic = []
	follows_domain = []
	
	for s in ships:
		c = s.column
		follows.append(c)
		if c.content_type_id == user_type.id:
			follows_user.append((c.content_object, c))
		elif c.content_type_id == topic_type.id:
			follows_topic.append((c.content_object, c))
		elif c.content_type_id == domain_type.id:
			follows_domain.append((c.content_object, c))
		else:
			pass
	
	user_self = user.userprofile.get_column()
	if user_self not in follows:
		follows.append(user.userprofile.get_column())
	
	return [follows, follows_user, follows_topic, follows_domain, user_self]


