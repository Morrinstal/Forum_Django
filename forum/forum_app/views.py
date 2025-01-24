from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Post, Like, Comment
from .forms import CategoryForm, PostForm

from django.contrib.auth import authenticate, login
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User
from forum_app.models import Profile
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm,UserEditForm,ProfileEditForm,PasswordChangeForm
from django.urls import reverse
from django.http import JsonResponse


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()  
            messages.success(request, "Registration successful!")
            return redirect('login')  
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()
    return render(request, 'forum_app/register.html', {'form': form})


def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login successful")
                return redirect('homepage') 
            else:
                messages.error(request, "Invalid username or password")
    else:
        form = LoginForm()

    return render(request, 'forum_app/login.html', {'form': form})


def homepage(request):
    return render(request,"forum_app/homepage.html")

def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        user = request.user
        like, created = Like.objects.get_or_create(user=user, post=post)

        if not created:
            like.delete()
            liked = False
        else:
            liked = True

        post.like_count = post.likes.count()
        post.save()

        return JsonResponse({'like_count': post.like_count, 'liked': liked}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required
def user_profile(request,username):
    profile, created = Profile.objects.get_or_create(user=request.user)
    user_form = UserEditForm(instance=request.user)
    profile_form = ProfileEditForm(instance=profile)
    password_form = PasswordChangeForm()

    if request.method == 'POST':
        if 'updated_profile' in request.POST:
            user_form = UserEditForm(request.POST, instance=request.user)
            profile_form = ProfileEditForm(request.POST, request.FILES, instance=profile)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                print(f"Updated profile: {profile_form.instance}")
                messages.success(request, 'Your profile has been updated')
                return redirect(reverse('profile', kwargs={'username': request.user.username}))
        elif 'change_password' in request.POST:
            password_form = PasswordChangeForm(request.POST)
            if password_form.is_valid():
                old_password = password_form.cleaned_data['old_password']
                if request.user.check_password(old_password):
                    request.user.set_password(password_form.cleaned_data['new_password'])
                    request.user.save()
                    update_session_auth_hash(request, request.user)
                    messages.success(request, 'Your password has been updated')
                    return redirect(reverse('profile', kwargs={'username': request.user.username}))
                else:
                    messages.error(request, 'Old password is incorrect')
    return render(request, 'forum_app/user_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'password_form': password_form
    })





def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

@login_required
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    posts = Post.objects.filter(category=category)

    is_admin = False
    if request.user.username == 'admin' and authenticate(username=request.user.username, password='qwerty'):
        is_admin = True

    return render(request, 'category_detail.html', {
        'category': category,
        'posts': posts,
        'is_admin': is_admin,
    })


def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'create_category.html', {'form': form})

def delete_category(request, id):
    category = get_object_or_404(Category, id=id)
    category.delete()
    return redirect('category_list')


def create_post(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.category = category 
            post.save()
            return redirect('category_detail', pk=category.pk)  
        else:
            print(form.errors) 
    else:
        form = PostForm()

    return render(request, 'create_post.html', {'form': form, 'category': category})




def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    return render(request, 'post_detail.html', {'post': post, 'comments': comments})

def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('category_detail', pk=post.category.pk)
    
@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Comment.objects.create(post=post, author=request.user, text=text)
            return redirect('post_detail', pk=pk) 
    return redirect('post_detail', pk=pk)

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user == comment.author:
        comment.delete()
        return redirect('post_detail', pk=comment.post.pk)
    return redirect('post_detail', pk=comment.post.pk) 