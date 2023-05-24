
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.context_processors import request
from django.urls import reverse_lazy
from django.views import generic
from . import models
from .forms import EventForm
from django.http import Http404
from braces.views import SelectRelatedMixin
from django.contrib.auth import get_user_model
# Create your views here.

User = get_user_model()


class ListEvents(SelectRelatedMixin, generic.ListView):
    model = models.UpcomingEvent
    select_related = ('user', 'group')
    template_name = 'event_list.html'


class UserEvents(generic.ListView):
    model = models.UpcomingEvent
    template_name = 'user_event_list.html'

    def get_queryset(self):
        try:
            self.event_user = User.objects.prefetch_related('events').get(username__iexact=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.event_user.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event_user'] = self.event_user
        return context


class EventDetail(SelectRelatedMixin, generic.DetailView):
    model = models.UpcomingEvent
    select_related = ('user', 'group')
    template_name = 'event_detail.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))


class CreateEvent(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):

    model = models.UpcomingEvent
    form_class = EventForm
    template_name = 'event_form.html'
    # fields = ('message', 'image', 'group')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class UpdateEvent(generic.UpdateView):
    model = models.UpcomingEvent
    template_name = 'event_update.html'
    fields = ['message', 'image']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)


class DeleteEvent(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = models.UpcomingEvent
    select_related = ('user', 'group')
    template_name = 'event_confirm_delete.html'
    success_url = reverse_lazy('events:all')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, 'Event Deleted')
        return super().delete(*args, **kwargs)