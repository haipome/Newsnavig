#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from utils import send_message, get_conversation
from forms import MessageSendForm
from string import atoi
from models import Contact

@login_required
def send(request):
	'''
	'''
	form = MessageSendForm()
	to_user = None
	if request.method == 'GET':
		if 'to' in request.GET and request.GET['to']:
			username = request.GET['to']
			try:
				to_user = User.objects.get(username__iexact=username)
			except:
				pass
			else:
				try:
					contact = from_user.contact_list.filter(to_user=to_user)[0]
					return HttpResponseRedirect(reverse(conversation, 
				               kwargs={'contact_id': contact.id}))
				except:
					pass
	elif request.method == "POST":
		form = MessageSendForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			from_user = request.user
			try:
				to_user = User.objects.get(username__iexact=data['send_to'])
			except:
				messages.error(request, u'用户不存在')
			else:
				message = data['message']
				send_message(from_user, to_user, message)
				contact = from_user.contact_list.filter(to_user=to_user)[0]
				return HttpResponseRedirect(reverse(conversation, 
				               kwargs={'contact_id': contact.id}))
		else:
			messages.error(request, u'发送失败')
			try:
				from_url = request.META['HTTP_REFERER']
				return HttpResponseRedirect(from_url)
			except KeyError:
				pass
	else:
		pass
	return render_to_response('messages/send.html',
	                         {'form': form,
	                          'to_user': to_user,},
	                          context_instance=RequestContext(request))

@login_required
def inbox(request):
	'''
	'''
	user = request.user
	contacts = user.contact_list.all().prefetch_related('to_user__userprofile__avatar','last_message__sender__userprofile', 'last_message__receiver__userprofile')
	if user.userdata.un_read_messages != 0:
		user.userdata.un_read_messages = 0
		user.userdata.save()
	return render_to_response('messages/inbox.html', {'contacts': contacts},
	                           context_instance=RequestContext(request))


@login_required
def conversation(request, contact_id):
	'''
	'''
	contact_id = atoi(contact_id)
	contact = get_object_or_404(Contact, pk=contact_id)
	if request.user != contact.user:
		return Http404()
	else:
		messages = get_conversation(contact.user, contact.to_user)
		return render_to_response('messages/conversation.html',
		                         {'contact': contact,
		                          'to_user': contact.to_user,
		                          'ms': messages,},
		                           context_instance=RequestContext(request))
	
