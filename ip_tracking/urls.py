from django.urls import path
from . import views

urlpatterns = [
    path('login/anonymous/', views.anonymous_limited_login, name='anonymous_login'),
    path('login/authenticated/', views.authenticated_limited_login, name='authenticated_login'),
]