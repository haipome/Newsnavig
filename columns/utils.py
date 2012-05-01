from models import Column
from nng.utils import generate_sha1

def create_column(obj):
	'''
	'''
	c = Column(content_object=obj)
	
	key = ''
	while True:
		key = generate_sha1()[:20]
		if not Column.objects.filter(secret_id=key).count():
			break
	
	c.secret_id = key
	
	c.save()
