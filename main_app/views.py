from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import *

# ----------------------- Static routes
def home(request):
    cities = City.objects.all().order_by("?")
    return render(request, 'home.html', {'cities': cities})

def about(request):
    return render(request, 'about.html')

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            Profile.objects.create(user=user)
            return redirect('home')
        else:
            error_message = 'Invalid sign up = try again'
            form = UserCreationForm()
            context = {'form': form, 'error_message': error_message}
            return render(request, 'registration/signup.html', context)
    else:
        error_message = 'Invalid sign up = try again'
        form = UserCreationForm()
        context = {'form': form, 'error_message': error_message}
        return render(request, 'registration/signup.html', context)

# ----------------------- Profile routes
def profile_detail(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    comments = Comment.objects.filter(user=user)
    posts = Post.objects.filter(user=user).order_by('-id')
    context = {
        'profile': profile,
        'comments': comments,
        'posts': posts,
    }
    return render(request, 'profiles/detail.html', context)

@login_required
def my_profile(request):
    my_profile = User.objects.get(username=request.user.username)
    posts = Post.objects.filter(user=request.user).order_by('-id')
    cities = City.objects.all()
    comments = Comment.objects.filter(user=request.user)
    context = {
        'my_profile': my_profile,
        'posts': posts,
        'comments': comments,

    }
    return render(request,'profiles/my_profile.html', context)

@login_required
def edit_profile(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            updated_profile = profile_form.save()
            return redirect('my_profile')
    else:
        form = ProfileForm(instance=profile)
        context = {'form': form, 'profile': profile}
        return render(request, 'profiles/edit_profile.html', context)

# ----------------------- City Routes
def city_index(request):
    cities = City.objects.all()
    return render(request, 'cities/index.html', {'cities': cities})

@login_required
def city_detail(request, city_id):
    user = User.objects.get(id = request.user.id)
    city = City.objects.get(id = city_id)
    cities = City.objects.all()
    posts = Post.objects.filter(city=city).order_by('-id')

    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.user = request.user
            new_post.city = city
            new_post.save()
            messages.success(request, f'Successfully created post titled: {new_post.title}!')
            return redirect('city_detail', city_id)
    else:
        form = PostForm()
        return render(request, 'cities/detail.html', {'city': city, 'posts': posts, 'form': form, 'cities': cities})

# ----------------------- Post routes
def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    print(post.__dict__, '-------------------HERE')
    comments = Comment.objects.filter(post=post_id).order_by("-id")
    city = City.objects.get(post=post_id)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = post
            new_comment.save()
            return redirect('post_detail',post_id)
        else:
            
            return redirect('post_detail',post_id)
    else: 
        comment_form = CommentForm()
        context = {
        'post': post,
        'comments': comments,
        'form': comment_form,
        'city': city,
    }
        return render(request, 'posts/detail.html', context)  

@login_required
def edit_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.user == post.user:
        if request.method == 'POST':
            post_form = PostForm(request.POST,request.FILES, instance=post)
            if post_form.is_valid():
                updated_post = post_form.save()
                return redirect('post_detail', updated_post.id)

        else:
            form = PostForm(instance=post)
            context = {'form': form, 'post':post}
            return render(request, 'posts/edit_post.html', context)
    else:
        return redirect('city_index')

@login_required
def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.user == post.user:
        Post.objects.get(id=post_id).delete()
        
        return redirect('my_profile')
    else:
        # flash message error
        return redirect('my_profile')






def city_index(request):
    cities = City.objects.all()
    return render(request, 'cities/index.html', {'cities': cities})

@login_required
def city_detail(request, city_id):
    user = User.objects.get(id = request.user.id)
    city = City.objects.get(id = city_id)
    cities = City.objects.all()
    posts = Post.objects.filter(city=city).order_by('-id')

    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.user = request.user
            new_post.city = city
            new_post.save()
            messages.success(request, f'Successfully created post titled: {new_post.title}!')
            return redirect('city_detail', city_id)
    else:
        form = PostForm()
        context = {
            'city': city,
            'posts': posts,
            'form': form,
            'cities': cities
        }
        return render(request, 'cities/detail.html', context)

# ----------------------- Comment Routes
@login_required
def edit_comment(request, post_id, comment_id):
    post = Post.objects.get(id=post_id)
    comment = Comment.objects.get(id=comment_id)
    if(request.user == comment.user):
        if request.method == 'POST':
            comment_form = CommentForm(request.POST, instance=comment)
            updated_comment = comment_form.save()
            return redirect('post_detail', post_id)

@login_required    
def delete_comment(request, post_id, comment_id):
    post = Post.objects.get(id=post_id)
    comment = Comment.objects.get(id=comment_id)
    if(request.user == comment.user):
        comment.delete()
        return redirect('post_detail', post_id)

def handler404(request):
    return render(request, '404.html')