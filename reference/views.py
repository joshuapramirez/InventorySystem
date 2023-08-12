from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from django.db.models import Count
from .models import User, Post, Follow, Like
from django.core.exceptions import ObjectDoesNotExist


def get_like_count(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
        like_count = post.likes_count()
        return JsonResponse({'count': like_count})
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'The object you are looking for does not exist.'}, status=404)

def remove_like(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
        user = User.objects.get(pk=request.user.id)
        like = Like.objects.filter(user=user, post=post)
        like.delete()
        return JsonResponse({"message": "Like removed!"})
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'The object you are looking for does not exist.'}, status=404)

def add_like(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
        user = User.objects.get(pk=request.user.id)
        like = Like(user=user, post=post)
        like.save()
        return JsonResponse({"message": "Like added!"})
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'The object you are looking for does not exist.'}, status=404)

def edit(request, post_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            edit_post = Post.objects.get(pk=post_id)
            edit_post.content = data["content"]
            edit_post.save()
            return JsonResponse({"message": "Change successful", "data": data["content"]})
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'The object you are looking for does not exist.'}, status=404)


def index(request):
    all_posts = Post.objects.all().order_by("id").reverse()

    # Pagination
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    posts_of_the_page = paginator.get_page(page_number)

    # Create an empty list to store the post IDs that the current user has liked
    posts_user_liked = []

    try:
        # Iterate through all the likes
        for like in Like.objects.filter(user=request.user):
            # Add the ID of the liked post to the list
            posts_user_liked.append(like.post.id)
    except:
        # If an error occurs during the iteration, set the list of liked post IDs to empty
        posts_user_liked = []

    return render(request, "network/index.html", {
        "posts_of_the_page": posts_of_the_page,
        "posts_user_liked": posts_user_liked,
    })

def new_post(request):
    if request.method == "POST":
        try:
            content = request.POST['content']
            user = User.objects.get(pk=request.user.id)
            post = Post(content=content, user=user)
            post.save()
            return HttpResponseRedirect(reverse(index))
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'The object you are looking for does not exist.'}, status=404)

def profile(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        all_posts = Post.objects.filter(user=user).order_by("id").reverse()

        following = Follow.objects.filter(user=user)
        followers = Follow.objects.filter(user_follower=user)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'The object you are looking for does not exist.'}, status=404)

    try:
        check_if_following = followers.filter(user=User.objects.get(pk=request.user.id))
        if len(check_if_following) != 0:
            is_following = True
        else:
            is_following = False
    except:
        is_following = False

    # Pagination
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    posts_of_the_page = paginator.get_page(page_number)


    # Retrieve the likes for all posts
    all_likes = Like.objects.all()

    # Create an empty list to store the post IDs that the current user has liked
    posts_user_liked = []

    try:
        # Iterate through all the likes
        for like in all_likes:
            # Check if the like is associated with the current user
            if like.user.id == request.user.id:
                # Add the ID of the liked post to the list
                posts_user_liked.append(like.post.id)
    except:
        # If an error occurs during the iteration, set the list of liked post IDs to empty
        posts_user_liked = []

    return render(request, "network/profile.html", {
        "posts_of_the_page": posts_of_the_page,
        "username" : user.username,
        "following": following,
        "followers": followers,
        "is_following": is_following,
        "user_profile": user,
        "posts_user_liked": posts_user_liked
    })

def following(request):
    current_user = User.objects.get(pk=request.user.id)
    users_following = Follow.objects.filter(user=current_user)
    all_posts = Post.objects.all().order_by('id').reverse()

    posts_of_following = []

    for post in all_posts:
        for each_user in users_following:
            if each_user.user_follower == post.user:
                posts_of_following.append(post)

    # Pagination
    paginator = Paginator(posts_of_following, 10)
    page_number = request.GET.get('page')
    posts_of_the_page = paginator.get_page(page_number)


    # Retrieve the likes for all posts
    all_likes = Like.objects.all()

    # Create an empty list to store the post IDs that the current user has liked
    posts_user_liked = []

    try:
        # Iterate through all the likes
        for like in all_likes:
            # Check if the like is associated with the current user
            if like.user.id == request.user.id:
                # Add the ID of the liked post to the list
                posts_user_liked.append(like.post.id)
    except:
        # If an error occurs during the iteration, set the list of liked post IDs to empty
        posts_user_liked = []

    return render(request, "network/following.html", {
        "posts_of_the_page": posts_of_the_page,
        "posts_user_liked": posts_user_liked
    })


def follow(request):
    userfollow = request.POST['userfollow']
    current_user = User.objects.get(pk=request.user.id)
    userfollow_data = User.objects.get(username=userfollow)
    f = Follow(user=current_user, user_follower=userfollow_data)
    f.save()
    user_id = userfollow_data.id
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id':user_id}))

def unfollow(request):
    userfollow = request.POST['userfollow']
    current_user = User.objects.get(pk=request.user.id)
    userfollow_data = User.objects.get(username=userfollow)
    f = Follow.objects.get(user=current_user, user_follower=userfollow_data)
    f.delete()
    user_id = userfollow_data.id
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id':user_id}))

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
