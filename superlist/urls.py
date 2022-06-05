from django.urls import path

from lists import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('lists/new', views.new_list, name='new_list'),
    path('lists/the-only-list-in-the-world/', views.view_list, name='view_list'),
]
