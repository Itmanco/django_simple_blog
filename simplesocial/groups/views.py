from sqlite3 import IntegrityError
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse
from django.views import generic
from .models import Group, GroupMember
# Create your views here.


class CreateGroup(LoginRequiredMixin, generic.CreateView):
    fields = ('name', 'description')
    model = Group
    template_name = 'group_form.html'


class SingleGroup(generic.DetailView):
    model = Group
    template_name = 'group_detail.html'


class ListGroups(generic.ListView):
    model = Group
    template_name = 'group_list.html'


class JoinGroup(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single', kwargs={"slug": self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group, slug=self.kwargs.get('slug'))

        try:
            GroupMember.objects.create(user=self.request.user, group=group)
        except IntegrityError:
            messages.warning(self.request, 'You are already a member of this group.')
        else:
            messages.success(self.request, 'You are now a member of this group.')
        return super().get(request, *args, **kwargs)


class LeaveGroup(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single', kwargs={"slug": self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):
        try:
            membership = GroupMember.objects.filter(
                user=self.request.user,
                group__slug=self.kwargs.get('slug')
            ).get()
        except GroupMember.DoesNotExist:
            messages.warning(self.request, 'You are not a member of this group.')
        else:
            membership.delete()
            messages.success(self.request, 'You are no longer a member of this group.')
        return super().get(request, *args, **kwargs)
