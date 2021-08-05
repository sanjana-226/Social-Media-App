from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, User
from .forms import NewUserForm, PostForm, CommentForm, UserUpdateForm, NewUserForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
User = get_user_model()


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by(
        "-published_date"
    )
    return render(request, "social/post_list.html", {"posts": posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    new_comment = None
    # Comment posted
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(
        request,
        "social/post_detail.html",
        {
            "post": post,
            "comments": comments,
            "new_comment": new_comment,
            "comment_form": comment_form,
        },
    )

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect("post_detail", pk=post.pk)
    else:
        form = PostForm()
    return render(request, "social/post_edit.html", {"form": form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect("post_detail", pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, "social/post_edit.html", {"form": form})

def about(request):
    return render(request, "social/about.html", {})

def my_profile(request):
    return render(request, "social/my_profile.html", {})

def register(request):
    if request.method == "POST":
        f = NewUserForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, "Account created successfully")
            return redirect("register")

    else:
        f = NewUserForm()

    return render(request, "registration/signup.html", {"form": f})

def signup_request(request):

    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("main:homepage")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(
        request=request,
        template_name="registration/signup.html",
        context={"register_form": form},
    )

def follow_list(request):
    p = request.user
    friends = p.friends.all()
    context = {"friends": friends}
    return render(request, "users/friend_list.html", context)

def profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    post = Post.objects.filter(author=user)

    following = True if user in request.user.follow.all() else False

    return render(
        request,
        "social/profile.html",
        {
            "user": user,
            "post": post,
            "following": following,
        },
    )

def edit_profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f"Your account has been updated!")
            return redirect("/my_profile")
    else:
        u_form = UserUpdateForm(instance=request.user)
    context = {
        "u_form": u_form,
    }
    return render(request, "social/edit_profile.html", context)

def follow(request, user):
    other_user= get_object_or_404(User, pk=user)
    me= request.user
    request.user.follow.add(other_user)
    return redirect(f"/profile/{user}")

def unfollow(request, user):
    other_user= get_object_or_404(User, pk=user)
    me= request.user
    request.user.follow.remove(other_user)
    return redirect(f"/profile/{user}")
    
def feed(request,user):
    pass