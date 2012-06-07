from models import Dynamic
from django.core.cache import cache
from nng.settings import MESSAGES_PER_PAGE, PREFETCH_RATE, D_CACHE_AGE


def get_objs(follows, offset, n, s=None, e=None):
	'''
	'''
	if offset and n:
		dynamics = Dynamic.objects.filter(
		           is_visible=True).filter(
		           id__lt=offset).filter(
		           column__in=follows).order_by(
		           '-id').all(
		           )[:n].prefetch_related(
		           'content_object__user__userprofile__avatar',
		           'content_object__domain',
		           'column__content_object',
		           'comment_object__domain',)
	
	else:
		dynamics = Dynamic.objects.filter(
		           is_visible=True).filter(
		           column__in=follows).order_by(
		           '-id').all(
		           )[s:e].prefetch_related(
		           'content_object__user__userprofile__avatar',
		           'content_object__domain',
		           'column__content_object',
		           'comment_object__domain',)
	
	
	return dynamics
	
def process_cache(key, page):
	
	if page == 1:
		return (None, [], {})
	
	user_log = cache.get(key)
	if not user_log:
		user_log = {}
		return (None, [], {})
	else:
		try:
			pre_page = user_log['pre_page']
			offset   = user_log['offset']
		except:
			return (None, [], {})
		
		if not pre_page + 1 == page:
			offset = 0
		
		history_logs = []
		for i in range(1, page):
			try:
				history_log = user_log[i]
			except:
				pass
			else:
				history_logs += history_log
		
		return (offset, history_logs, user_log)

def get_dynamics(user, follows, page):
	
	key = user.id
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
	
	dynamics = []
	page_log = []
	counter = 0
	for obj in objs:
		counter += 1
		obj_id = obj.id
		i = obj.object_id
		if i not in logs:
			logs.append(i)
			page_log.append(i)
			dynamics.append(obj)
	
	offset = obj_id
	user_log['offset'] = offset
	user_log['pre_page'] = page
	user_log[page] = page_log
	cache.set(key, user_log, D_CACHE_AGE)
	
	if counter == n:
		next_page = True
	else:
		next_page = False
	return (dynamics, next_page)
	
