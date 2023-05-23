
from django.urls import path
from . import views


app_name = 'upcomingevents'

urlpatterns = [
    path('', views.ListEvents.as_view(), name='all'),
    path('new/', views.CreateEvent.as_view(), name='create'),
    path('by/<username>)', views.UserEvents.as_view(), name='for_user'),
    path('by/<username>/<int:pk>/', views.EventDetail.as_view(), name='single'),
    path('delete/<int:pk>/', views.DeleteEvent.as_view(), name='delete'),
    path('posted/edit/<int:pk>', views.UpdateEvent.as_view(), name='edit'),
]
