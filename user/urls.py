from django.urls import path
from . import views
urlpatterns = [
    path("test/", views.test),
    path('', views.index, name="users"),
    path('login/', views.login, name='login_url'),
    path('logout/', views.logout, name='logout_url'),
    path('register/', views.registeration, name="register_url"),
    path('otp/', views.otp, name="otp verification"),
    path("resend_otp/", views.resendOtp, name="resend otp")
]