from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get-pass/', views.visitor_form, name='visitor_form'),
    path('success/', views.request_success, name='request_success'),
    path('login/', views.staff_login, name='staff_login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('approve/<int:pk>/', views.approve_visitor, name='approve'),
]
