from django.urls import path
from home import views

urlpatterns = [
    path("", views.homepage, name="home"),
    path("store/", views.store, name="store"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
]
