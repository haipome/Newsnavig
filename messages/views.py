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
from utils import send_message, get_conversation, delete_message, delete_contact
from forms import MessageSendForm
from string import atoi
from models import Contact, Message
from nng.settings import *

@login_required
def send(request):
	'''
	'''
	form = MessageSendForm()
	from_user = request.user
	to_user = None
	if request.method == 'GET':
		if 'to' in request.GET and request.GET['to']:
			username = request.GET['to']
			try:
				to_user = User.objects.get(username__iexact=username)
			except:
				pass
			else:
				if to_user == from_user:
					return HttpResponseRedirect(reverse('message_inbox'))
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
			try:
				to_user = User.objects.get(username__iexact=data['send_to'])
			except:
				messages.error(request, u'用户不存在')
			else:
				if to_user == from_user:
					messages.error(request, u'不可以给自己发送私信')
					to_user = None
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
	page = 1
	n_contacts = user.contact_list.count()
	if request.method == 'GET':
		if 'p' in request.GET and request.GET['p']:
			page = atoi(request.GET['p'])
	if (((page - 1) * MESSAGES_PER_PAGE) >= n_contacts):
		page = 1
	if page != 1:
		pre_page = page - 1
	else:
		pre_page = False
	if page * MESSAGES_PER_PAGE < n_contacts:
		next_page = page + 1
	else:
		next_page = False
	s = (page - 1) * MESSAGES_PER_PAGE
	e = s + MESSAGES_PER_PAGE
	if n_contacts:
		contacts = user.contact_list.all(
		           )[s:e].prefetch_related(
		           'to_user__userprofile__avatar',
		           'last_message__sender__userprofile',
		           'last_message__receiver__userprofile')
	else:
		contacts = None
	if user.userdata.un_read_messages != 0:
		user.userdata.un_read_messages = 0
		user.userdata.save()
	return render_to_response('messages/inbox.html',
	                         {'contacts': contacts,
	                          'n_contacts': n_contacts,
	                          'pre': pre_page,
	                          'next': next_page,},
	                           context_instance=RequestContext(request))


@login_required
def conversation(request, contact_id):
	'''
	'''
	contact_id = atoi(contact_id)
	try:
		contact = Contact.objects.get(pk=contact_id)
	except:
		return HttpResponseRedirect(reverse('message_inbox'))
	if request.user != contact.user:
		raise Http404
	page = 1
	if request.method == 'GET':
		if 'p' in request.GET and request.GET['p']:
			page = atoi(request.GET['p'])
	if (page - 1) * MESSAGES_PER_PAGE >= contact.n_messages:
		raise Http404
	if page != 0:
		pre_page = page - 1
	else:
		pre_page = False
	if page * MESSAGES_PER_PAGE < contact.n_messages:
		next_page = page + 1
	else:
		next_page = False
	
	messages = get_conversation(contact.user, contact.to_user, page)
	return render_to_response('messages/conversation.html',
		                     {'contact': contact,
		                      'to_user': contact.to_user,
		                      'ms': messages,
		                      'pre': pre_page,
		                      'next': next_page,},
		                       context_instance=RequestContext(request))


@login_required
def delete(request):
	'''
	'''
	user = request.user
	t, i = None, None
	if request.method == 'GET':
		if 't' in request.GET and request.GET['t']:
			t = request.GET['t']
		if 'i' in request.GET and request.GET['i']:
			i = request.GET['i']
		if t == 'c' and i:
			try:
				to_user = User.objects.get(username__iexact=i)
			except:
				pass
			else:
				if delete_contact(user, to_user):
					return HttpResponseRedirect(reverse('message_inbox'))
		elif t == 'm' and i:
			i = atoi(i)
			try:
				m = Message.objects.get(pk=i)
			except:
				pass
			else:
				delete_message(user, m)
	
	try:
		from_url = request.META['HTTP_REFERER']
		return HttpResponseRedirect(from_url)
	except KeyError:
		raise Http404
