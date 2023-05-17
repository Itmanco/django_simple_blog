from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.context_processors import request
from django.urls import reverse_lazy
from django.views import generic
from . import models
from .forms import PostForm
from django.http import Http404
from braces.views import SelectRelatedMixin
from django.contrib.auth import get_user_model
# Create your views here.

User = get_user_model()


class ListPosts(SelectRelatedMixin, generic.ListView):
    model = models.Post
    select_related = ('user', 'group')
    template_name = 'post_list.html'


class UserPosts(generic.ListView):
    model = models.Post
    template_name = 'user_post_list.html'

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related('posts').get(username__iexact=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_user'] = self.post_user
        return context


class PostDetail(SelectRelatedMixin, generic.DetailView):
    model = models.Post
    select_related = ('user', 'group')
    template_name = 'post_detail.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))


class CreatePost(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):

    model = models.Post
    form_class = PostForm
    template_name = 'post_form.html'
    # fields = ('message', 'image', 'group')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class UpdatePost(generic.UpdateView):
    model = models.Post
    template_name = 'post_update.html'
    fields = ['message', 'image']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)


class DeletePost(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = models.Post
    select_related = ('user', 'group')
    template_name = 'post_confirm_delete.html'
    success_url = reverse_lazy('posts:all')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, 'Post Deleted')
        return super().delete(*args, **kwargs)