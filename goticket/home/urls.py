from django.urls import path
from home import views

urlpatterns = [
    path("", views.homepage, name="home"),
    path("store/", views.store, name="store"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("profile/", views.profile, name="profile"),
	path("product/<uuid:event_id>/", views.product, name="product"),
	path("product/", views.product_empty, name="product"),
]
