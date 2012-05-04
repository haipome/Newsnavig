from models import Collect


def collect(user, obj):
	'''
	'''
	v = Collect.objects.filter(user=user, object_id=obj.id)
	if v:
		return v[0]
	
	try:
		obj.n_collecter += 1
		obj.save()
	except:
		return False
	
	collect = Collect.objects.create(user=user, content_object=obj)
	
	return collect
