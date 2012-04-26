from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
	'''
	'''
	sender = models.ForeignKey(User, related_name="send_messages")
	sender_delete = models.BooleanField(default=False)
	receiver = models.ForeignKey(User, related_name="receive_messages")
	receiver_delete = models.BooleanField(default=False)
	send_time = models.DateTimeField(auto_now_add=True)
	
	message = models.TextField()
	
	# objects = MessageManager()
	
	class Meta:
		ordering = ["-id"]
	
	def __unicode__(self):
		return self.sender.username + " -> " + self.receiver.username +": " + \
		       self.message

class Contact(models.Model):
	'''
	'''
	user = models.ForeignKey(User, related_name="contact_list")
	to_user = models.ForeignKey(User, related_name="be_contact_list")
	last_contact = models.DateTimeField()
	last_message = models.ForeignKey(Message)
	n_messages = models.IntegerField(default=0)
	un_read = models.IntegerField(default=0)
	
	class Meta:
		ordering = ["-last_contact"]
	
	def __unicode__(self):
		return self.to_user.username + " with " + str(self.n_messages) + \
		       " messages: " + self.last_message.message
	
	def get_absolute_url(self):
		return '/message/conversation/' + str(self.id) + '/'
