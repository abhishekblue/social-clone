from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Profile, Meep
from .forms import MeepForm, SignupForm, ProfilePicForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


# Create your views here.

def home(request):
    if request.user.is_authenticated:
        form = MeepForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                meep = form.save(commit=False)
                meep.user = request.user
                meep.save()
                return redirect('home')
        meeps = Meep.objects.all().order_by('-created_at')
        return render(request, 'home.html', {'meeps': meeps, 'form': form})
    else:
        meeps = Meep.objects.all().order_by('-created_at')
        return render(request, 'home.html', {'meeps': meeps})


def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', {'profiles': profiles})
    else:
        messages.success(request, "You must be logged in to view this page.")
        return redirect('home')


def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        meeps = Meep.objects.filter(user_id=pk).order_by('-created_at')
        if request.method == 'POST':
            #get current user
            current_user_profile = request.user.profile
            #get form data
            action = request.POST['follow']
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            elif action == "follow":
                current_user_profile.follows.add(profile)
            current_user_profile.save()
            
        return render(request, 'profile.html', {'profile': profile, 'meeps':meeps})
    else:
        messages.success(request, "You must be logged in to view this page.")
        return redirect('home')
    

def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, "Invalid username or password.")
            return redirect('login')
    else:
        return render(request, 'login.html', {})
    

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect('login')

def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'register.html', {'form':form})


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        profile_user = Profile.objects.get(user__id=request.user.id)
        form = SignupForm(request.POST or None, request.FILES or None, instance=current_user)
        profileform = ProfilePicForm(request.POST or None, request.FILES or None, instance=profile_user)
        print(request.FILES)
        print(form.is_valid()) 
        print(profileform.is_valid())
        print(form.errors)

        if form.is_valid() and profileform.is_valid():
            form.save()
            profileform.save()
            login(request, current_user)
            messages.success(request, "Your profile has been updated")
            return redirect('home')
        return render(request, 'update_user.html', {'form':form, 'profileform':profileform})
        
    else: 
        messages.success(request, "You must be logged in to continue.")
        return redirect('login')
    

def meep_like(request, pk):
    meep = get_object_or_404(Meep, id=pk)
    if meep.likes.filter(id=request.user.id):
        meep.likes.remove(request.user)
    else:
        meep.likes.add(request.user)
    return redirect(request.META.get('HTTP_REFERER')) 


def share(request, pk):
    meep = get_object_or_404(Meep, id=pk)
    if meep:
        return render(request, 'share.html', {'meep': meep})
    else:
        messages.success(request, "Does not exist")
        return redirect('home')