from django.urls import path

from lists import views

urlpatterns = [
    path('', views.homepage, name='homepage')
]
