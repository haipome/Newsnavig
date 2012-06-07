#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.urlresolvers import reverse
from nng.settings import *
from links.models import Link
from discusses.models import Discuss
from models import Comment
from utils import post_comment
from forms import CommentPostForm
from string import atoi
from comments.utils import comment_sort_common

@login_required
def post(request):
	'''
	'''
	user = request.user
	if request.method == 'POST':
		form = CommentPostForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			items = data['reply'].split('-')
			obj_type = items[0]
			obj_id = atoi(items[1])
			content = data['content']
			
			if obj_type == 'l':
				try:
					obj = Link.objects.get(id=obj_id)
				except:
					raise Http404
			elif obj_type == 'd':
				try:
					obj = Discuss.objects.get(id=obj_id)
				except:
					raise Http404
			else:
				raise Http404
			
			if data['parent']:
				parent_id = atoi(data['parent'])
				try:
					parent = Comment.objects.get(id=parent_id)
				except:
					parent = None
			else:
				parent = None
			
			
			c = post_comment(user, content, obj, parent)
			if c:
				return HttpResponseRedirect(reverse(show_comment, args=[c.id]))
	
	try:
		from_url = request.META['HTTP_REFERER']
		return HttpResponseRedirect(from_url)
	except KeyError:
		raise Http404
	

def show_comment(request, comment_id):
	'''
	'''
	comment = get_object_or_404(Comment, id=atoi(comment_id))
	
	comments = comment.content_object.comments.all().select_related(
	           'user__userprofile__avatar')
	comments = comment_sort_common(comment, comments, COMMENT_DEEPS)
	
	return render_to_response('comment/show_comment.html',
	                         {'ct': comment,
	                          'comments': comments,},
	                         context_instance=RequestContext(request))
	


