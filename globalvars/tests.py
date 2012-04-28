"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase


from django.contrib.auth.models import User
from utils import post_link


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
    def test_post_link(self):
        u = User.objects.get(id=2)
        url = 'https://docs.djangoproject.com/en/dev/ref/models/fields/'
        topic_names = ['django', 'python', 'program']
        title = 'QuerySet API reference'
        
        post(url, u, topic_names, title)
