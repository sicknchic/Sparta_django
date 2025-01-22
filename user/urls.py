from django.urls import path
from . import views

app_name = "user"
urlpatterns = [
    path("", views.user_list, name="list"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("delete/", views.delete, name="delete"),
    path("update/", views.update, name="update"),
    path("password/", views.change_password, name="change_password"),
    path("<int:pk>", views.profile, name="profile"),
]
