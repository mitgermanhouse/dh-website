# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.urls import reverse

from home.models import Member
from home.forms import MemberDataForm, MemberImageForm

class HomeView(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['members'] = Member.objects.exclude(user__groups__name__in=['alumni']).order_by('class_year', '-user')
        return context

# REFERENCE: https://python.plainenglish.io/adventures-in-django-how-to-implement-multiple-modelforms-in-a-view-5ec75058dff4
class EditProfileUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'home/edit_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get user and member
        user = self.request.user
        member = user.member or Member(user=user)

        # Modify context
        context['member'] = member
        context['edit_access'] = check_if_profile_edit_access(user)
        context['data_form'] = MemberDataForm(instance=member, label_suffix='')
        context['image_form'] = MemberImageForm(instance=member, label_suffix='')

        return context

    def post(self, request, *args, **kwargs):
        # Get user and member
        user = request.user
        member = uer.member or Member(user=user)

        # Check for edit access
        if not check_if_profile_edit_access(user):
            return HttpResponseForbidden("401 Forbidden: You don't have edit access.")

        # Member Data Form
        if 'form_type__MemberDataForm' in request.POST:
            form = MemberDataForm(instance=member, data=request.POST)
            
            if form.is_bound and form.is_valid():
                form.save()

        elif 'form_type__MemberImageForm' in request.POST:
            form = MemberImageForm(instance=member, data=request.POST, files=request.FILES)

            if form.is_bound and form.is_valid():
                form.save()

        return HttpResponseRedirect(reverse('home:edit_profile'))

def check_if_profile_edit_access(user):
    # users under profile ban will not be allowed to edit their profiles (for trolling prevention)
    return user.groups.all().filter(name="profile_ban").count() == 0
