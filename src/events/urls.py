from django.urls import include, path

from . import views

urlpatterns = [
    path('events/', include(([
        path('', views.events_list, name='events-list'),
        path('<int:pk>/', views.user_events, name='user-events'),
        path('<int:pk>/', views.event_details, name='event-view'),
        path('create/', views.event_create, name='event-new'),
    ], 'events'), namespace='events')),
]