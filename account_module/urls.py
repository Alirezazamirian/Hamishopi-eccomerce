from django.urls import path
from . import views

urlpatterns = [
    path('login-with-username/', views.UsernameLoginView.as_view(), name='login-username-page'),
    path('login-with-phone/', views.PhoneLoginView.as_view(), name='login-phone-page'),
    path('register/', views.RegisterView.as_view(), name='register-page'),
    path('forget_password/', views.ForgetPasswordView.as_view(), name='forget_password-page'),
    path('reset-pass/<activation_code>', views.ResetPasswordView.as_view(), name='reset_password_page'),
    path('logout', views.LogoutView.as_view(), name='logout_page'),
    path('verify', views.verify, name='verify-page'),

]
