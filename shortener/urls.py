from django.urls import path
from . import views

urlpatterns = [
    # auth
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # app
    path('', views.home, name='home'),
    path('my-links/', views.my_links, name='my_links'),
    path('link/<slug:slug>/', views.detail, name='detail'),
    path('qr/<slug:slug>/', views.qr_code_view, name='qr'),
    path('check-slug/', views.check_slug, name='check_slug'),

    # public redirect (must be last)
    path('<slug:slug>/', views.redirect_view, name='redirect'),
]
