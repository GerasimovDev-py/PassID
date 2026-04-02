from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get-pass/', views.visitor_form, name='visitor_form'),
    path('success/', views.request_success, name='request_success'),
    path('login/', views.staff_login, name='staff_login'),
    path('logout/', views.staff_logout, name='staff_logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/partial/', views.dashboard_partial, name='dashboard_partial'),
    path('approve/<int:pk>/', views.approve_visitor, name='approve_visitor'),
    path('departed/<int:pk>/', views.mark_departed, name='mark_departed'),
    path('check-status/', views.check_status, name='check_status'),
]
