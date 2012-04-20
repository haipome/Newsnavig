#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.dispatch import Signal

create_user_done = Signal(providing_args=["user"])
