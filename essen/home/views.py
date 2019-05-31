# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from home.models import Member
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import os
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

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
            # member.save()
        else:
            member = member_list.first()
        d = {context_object_name: member, "edit_access":check_if_profile_edit_access(user)}

    return render(request, template_name, d)

def submit_profile(request):
    if request.user.is_authenticated and check_if_profile_edit_access(request.user):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        p = dict(request.FILES.iterlists())
        d = dict(request.POST.iterlists())
        img = p["pic"][0]

        class_year = d["class_year"][0]
        bio = d["bio"][0]
        major = d["major"][0]

        # get the member entry
        member_list = Member.objects.filter(user=request.user)
        member = None
        if len(member_list) == 0:
            member = Member(user=request.user)
            # member.save()
        else:
            member = member_list.first()

        member.bio = bio
        member.class_year = class_year
        member.image = img

        # resize the image so loading time is not ridiculously long
        output = BytesIO()
        im = Image.open(member.image)
        basewidth = 200
        width, height = im.size
        wpercent = (basewidth / float(width))
        hsize = int((float(height) * float(wpercent)))
        im = im.resize((basewidth, hsize), Image.ANTIALIAS)
        im.save(output, format='JPEG', quality=100)
        output.seek(0)
        member.image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % member.image.name.split('.')[0], 'image/jpeg',
                                        sys.getsizeof(output), None)

        member.major = major
        member.save()

    return HttpResponseRedirect(reverse('home:home') + "#" + request.user.username)

def check_if_profile_edit_access(user):
    # users under profile ban will not be allowed to edit their profiles (for trolling prevention)
    return user.groups.all().filter(name="profile_ban").count() == 0





