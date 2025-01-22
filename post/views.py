from django.shortcuts import render, redirect
from .forms import PostForm
from .models import Post
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


def post_list(request):
    posts = Post.objects.all().order_by("-pk")
    context = {"posts": posts}
    return render(request, "post/post_list.html", context)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    context = {"post": post}
    return render(request, "post/post_detail.html", context)


@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("post:post_detail", post.pk)
    else:
        form = PostForm()
    context = {"form": form}
    return render(request, "post/post_form.html", context)


@require_POST
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return render(request, "post/post_forbidden.html")

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("post:post_detail", post.pk)
    else:
        form = PostForm(instance=post)
    context = {"post": post, "form": form}
    return render(request, "post/post_form.html", context)


@login_required
@require_POST
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return render(request, "post/post_forbidden.html")
    post.delete()
    return redirect("post:post_list")
