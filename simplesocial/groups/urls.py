
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'groups'

urlpatterns = [
    path('', views.ListGroups.as_view(), name='all'),
    path('new/', views.CreateGroup.as_view(), name='create'),
    path('posts/in/<slug>/', views.SingleGroup.as_view(), name='single'),
    path('join/<slug>/', views.JoinGroup.as_view(), name='join'),
    path('leave/<slug>/', views.LeaveGroup.as_view(), name='leave'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)