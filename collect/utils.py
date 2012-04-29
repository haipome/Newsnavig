from models import Collect


def collect(user, obj):
	'''
	'''
	try:
		obj.n_collecter += 1
		obj.save()
	except:
		return False
	
	collect = Collect.objects.create(user=user, content_object=obj)
	
	return collect
