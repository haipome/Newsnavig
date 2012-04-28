from globalvars.models import GlobalVar

def get_available_id():
	'''
	'''
	try:
		g = GlobalVar.objects.select_for_update().get(pk=1)
	except:
		g = GlobalVar.objects.create()
	
	g.content_id += 1
	g.save()
	
	return g.content_id
