# Create your views here.

from django.shortcuts import render_to_response
from django.template import RequestContext

def profile(request):
	return render_to_response('accounts/profile.html', context_instance=RequestContext(request))
