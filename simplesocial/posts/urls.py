
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'posts'

urlpatterns = [
    path('', views.ListPosts.as_view(), name='all'),
    path('new/', views.CreatePost.as_view(), name='create'),
    path('by/<username>)', views.UserPosts.as_view(), name='for_user'),
    path('by/<username>/<pk>/', views.PostDetail.as_view(), name='single'),
    path('delete/<pk>/', views.DeletePost.as_view(), name='delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
