# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from home.models import Member
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import os

# Create your views here.

def home(request):
    template_name = "home/home.html"
    context_object_name = "members"

    return render(request, template_name, {context_object_name: Member.objects.all()})

def edit_profile(request):
    template_name = "home/edit_profile.html"
    context_object_name = "member"

    d = {}
    if request.user.is_authenticated:
        user = request.user
        member_list = Member.objects.filter(user=user)
        member = None
        if len(member_list) == 0:
            member = Member(user=user)
            member.save()
        else:
            member = member_list.first()
        d = {context_object_name: member}

    return render(request, template_name, d)

def submit_profile(request):
    if request.user.is_authenticated:
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        p = dict(request.FILES.iterlists())
        d = dict(request.POST.iterlists())
        image = p["pic"][0]
        class_year = d["class_year"][0]
        bio = d["bio"][0]
        major = d["major"][0]

        # get the member entry
        member = Member.objects.filter(user=request.user).first()
        # delete old image
        # if str(member.image) != "":
            # os.remove(os.path.join(BASE_DIR, "media", str(member.image)))

        member.bio = bio
        member.class_year = class_year
        member.image = image
        member.major = major
        member.save()

    return HttpResponseRedirect(reverse('home:edit_profile'))







