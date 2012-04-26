from models import Message, Contact

def send_message(sender, receiver, words):
	'''
	'''
	m = Message.objects.create(sender=sender, receiver=receiver, message=words)
	try:
		sender_contact = sender.contact_list.filter(to_user=receiver)[0]
		sender_contact.n_messages += 1
		sender_contact.last_contact = m.send_time
		sender_contact.last_message = m
		sender_contact.save()
	except:
		sender_contact = Contact.objects.create(to_user=receiver,
		                                        user=sender,
		                                        last_contact=m.send_time,
		                                        last_message=m,
		                                        n_messages=1)
	try:
		receiver_contact = receiver.contact_list.filter(to_user=sender)[0]
		receiver_contact.n_messages += 1
		receiver_contact.last_contact = m.send_time
		receiver_contact.last_message = m
		receiver_contact.un_read += 1
		receiver_contact.save()
	except:
		receiver_contact = Contact.objects.create(to_user=sender,
		                                          user=receiver,
		                                          last_contact=m.send_time,
		                                          last_message=m,
		                                          n_messages=1,
		                                          un_read=1)
	try:
		receiver.userdata.un_read_messages += 1
		receiver.userdata.save()
	except:
		pass
	return m

def _get_next_message(users):
	'''
	'''
	return Message.objects.filter(sender__in=users).filter(receiver__in=users)[1]

def _get_contact_messages(users):
	'''
	'''
	return Message.objects.filter(sender__in=users).filter(receiver__in=users).all().values('sender', 'receiver', 'send_time', 'message')
	# .prefetch_related('sender__userprofile__avatar', 'receiver__userprofile__avatar')

def delete_message(user, m):
	'''
	'''
	if user == m.sender:
		if not m.sender_delete:
			m.sender_delete = True
			contact = user.contact_list.get(to_user=m.receiver)
			contact.n_messages -= 1
			if contact.n_messages == 0:
				contact.delete()
			else:
				m = _get_next_message([m.sender, m.receiver])
				contact.last_message = m
				contact.last_contact = m.send_time
				contact.save()
		else:
			return True
	elif user == m.receiver:
		if not m.receiver_delete:
			m.receiver_delete = True
			contact = user.contact_list.get(to_user=m.sender)
			contact.n_messages -= 1
			if contact.n_messages == 0:
				contact.delete()
			else:
				m = _get_next_message([m.sender, m.receiver])
				contact.last_message = m
				contact.last_contact = m.send_time
				contact.save()
	else:
		return False
	if m.sender_delete and m.receiver_delete:
		m.delete()
	else:
		m.save()
	return True
	
def delete_contact(user, to_user):
	'''
	'''
	try:
		c = user.contact_list.filter(to_user=to_user)[0]
	except:
		return False
	c.delete()
	
	messages = _get_contact_messages([user, to_user])
	n = messages.count()
	for m in messages:
		if user == m.sender:
			m.sender_delete = True
		elif user == m.receiver:
			m.receiver_delete = True
		else:
			pass
		if m.sender_delete and m.receiver_delete:
			m.delete()
		else:
			m.save()
	return n

def get_conversation(user, to_user):
	'''
	'''
	try:
		c = user.contact_list.filter(to_user=to_user)[0]
	except:
		return False
	if c.un_read:
		if user.userdata.un_read_messages != 0:
			user.userdata.un_read_messages = 0
			user.userdata.save()
		c.un_read = 0
		c.save()
	
	return _get_contact_messages([user, to_user])


