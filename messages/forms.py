from django import forms

class MessageSendForm(forms.Form):
	'''
	'''
	send_to = forms.CharField(max_length=30)
	message = forms.CharField()
	
