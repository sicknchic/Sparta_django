from django.shortcuts import render, redirect
from .forms import PostForm, CommentForm
from .models import Post, Comment
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.urls import reverse


def post_list(request):
    posts = Post.objects.all().order_by("-pk")
    context = {"posts": posts}
    return render(request, "post/post_list.html", context)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comment_form = CommentForm()
    comments = post.comments.all()
    context = {"post": post, "comment_form": comment_form, "comments": comments}
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


@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        post_detail_url = reverse("post:post_detail", kwargs={"pk": pk})
        context = {"post_detail_url": post_detail_url}
        return render(request, "post/post_forbidden.html", context)

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
        post_detail_url = reverse("post:post_detail", kwargs={"pk": pk})
        context = {"post_detail_url": post_detail_url}
        return render(request, "post/post_forbidden.html", context)
    post.delete()
    return redirect("post:post_list")


@login_required
@require_POST
def comment_create(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect("post:post_detail", post.pk)


@login_required
@require_POST
def comment_delete(request, pk, comment_pk):
    post = get_object_or_404(Post, pk=pk)
    comment = Comment.objects.get(pk=comment_pk)

    if comment.author != request.user:
        post_detail_url = reverse("post:post_detail", kwargs={"pk": pk})
        context = {"post_detail_url": post_detail_url}
        return render(request, "post/post_forbidden.html", context)
    comment.delete()
    return redirect("post:post_detail", post.pk)


# @login_required
# def comment_update(request, pk, comment_pk):
#     post = get_object_or_404(Post, pk=pk)
#     comments = Comment.objects.all()
#     comment = Comment.objects.get(pk=comment_pk)

#     if comment.author != request.user:
#         post_detail_url = reverse("post:post_detail", kwargs={"pk": pk})
#         context = {"post_detail_url": post_detail_url}
#         return render(request, "post/post_forbidden.html", context)

#     if request.method == "POST":
#         form = CommentForm(request.POST, instance=comment)
#         if form.is_valid():
#             comment = form.save()
#             comment.save()
#             return redirect("post:post_detail", post.pk)
#     else:
#         form = CommentForm(instance=comment)
#     context = {"post": post, "comments": comments, "comment": comment, "form": form}
#     return render(request, "post/post_detail.html", context)
