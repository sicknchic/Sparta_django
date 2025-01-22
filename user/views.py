from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from .forms import UserCreationForm, UserChangeForm
from .models import CustomUser


def user_list(request):
    users = CustomUser.objects.all()
    context = {"users": users}
    return render(request, "user/user_list.html", context)


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("user:list")
    else:
        form = UserCreationForm()
    context = {"form": form}
    return render(request, "user/signup.html", context)


@require_http_methods(["GET", "POST"])
def login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            next_path = request.GET.get("next") or "user:list"
            return redirect(next_path)
    else:
        form = AuthenticationForm()
    context = {"form": form}
    return render(request, "user/login.html", context)


@login_required
@require_POST
def logout(request):
    if request.method == "POST":
        auth_logout(request)
    return redirect("user:list")


@login_required
def delete(request):
    if request.user.is_authenticated:
        request.user.delete()
        auth_logout(request)
    return redirect("user:list")


@login_required
@require_http_methods(["GET", "POST"])
def update(request):
    if request.method == "POST":
        form = UserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("user:list")
    else:
        form = UserChangeForm(instance=request.user)
    context = {"form": form}
    return render(request, "user/update.html", context)


@login_required
@require_http_methods(["GET", "POST"])
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request=request, user=form.user)
            return redirect("user:list")
    else:
        form = PasswordChangeForm(request.user)
        context = {"form": form}
    return render(request, "user/change_password.html", context)


def profile(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    context = {"user": user}
    return render(request, "user/profile.html", context)
