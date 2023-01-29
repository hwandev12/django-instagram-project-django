from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.db import transaction
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth import authenticate, login


from .models import Profile
from .forms import EditProfileForm, UserRegisterForm
from django.urls import resolve

# create user profile
def UserProfile(request, username):
    player, created = Profile.objects.get_or_create(user=request.user)
    user = get_object_or_404(User, username=username)
    profile_form = Profile.objects.get(user=user)
    url_name = resolve(request.path).url_name
    
    # if url_name == 'profile':
    #     posts = Post.objects.filter(user=user).order_by('-posted')
    # else:
    #     posts = profile.favourite.all()
    
    # pagination
    # paginator = Paginator(posts, 8)
    # page_number = request.GET.get('page')
    # posts_paginator = paginator.get_page(page_number)
    
    context = {
        "profile": profile_form
    }
    return render(request, 'profile.html', context)

def edit_profile(request):
    user = request.user.id
    profile = Profile.objects.get(user__id=user)
    
    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            profile.image = form.cleaned_data.get('image')
            profile.first_name = form.cleaned_data.get('first_name')
            profile.last_name = form.cleaned_data.get('last_name')
            profile.location = form.cleaned_data.get('location')
            profile.url = form.cleaned_data.get('url')
            profile.bio = form.cleaned_data.get('bio')
            profile.save()
            return redirect('profile', profile.user.username)
    else:
        form = EditProfileForm(instance=request.user.profile)
        
    context = {
        "form": form
    }
    return render(request, 'editprofile.html', context)

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            # Profile.get_or_create(user=request.user)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hurray your account was created!!')

            # Automatically Log In The User
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],)
            login(request, new_user)
            # return redirect('editprofile')
            return redirect('index')
            


    elif request.user.is_authenticated:
        return redirect('index')
    else:
        form = UserRegisterForm()
    context = {
        'form': form,
    }
    return render(request, 'sign-up.html', context)

