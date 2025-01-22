from django import forms
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
from django.contrib.auth.forms import UserChangeForm as DjangoUserChangeForm


class UserCreationForm(DjangoUserCreationForm):
    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "first_name",
            "last_name",
            "image",
            "introduction",
            "email",
        )


class UserChangeForm(DjangoUserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "email", "image", "introduction")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.fields.get("password")
        if self.fields.get("password"):
            password_help_text = (
                "You can change the password " '<a href="{}">here</a>.'
            ).format(f"{reverse('user:change_password')}")
            self.fields["password"].help_text = password_help_text
