from models import Dynamic


def get_dynamics(follows, s, e):
	
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
	
