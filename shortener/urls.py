from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('link/<slug:slug>/', views.detail, name='detail'),
    path('qr/<slug:slug>/', views.qr_code_view, name='qr'),
    path('<slug:slug>/', views.redirect_view, name='redirect'),
]
