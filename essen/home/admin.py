# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

from home.models import Member
from menu.models import AutoLatePlate

admin.site.register(Member)
admin.site.register(AutoLatePlate)
