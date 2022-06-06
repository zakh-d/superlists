from django.urls import path, include

from lists import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('lists/', include('lists.urls')),
]
