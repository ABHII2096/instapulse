from django.shortcuts import render,redirect, get_object_or_404 
from .forms import PostForm
from .models import Post14 , Comment
from .forms import CommentForm
from django.contrib import messages 
from django.contrib.auth.models import User 
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import ContactForm
from Myapp.models import Post14 as Post, Follow
from .models import Profile

from django.contrib.auth import authenticate, login

 




def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not username or not email or not password:
            messages.error(request, "All fields are required.")
            return render(request, 'Myapp/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return render(request, 'Myapp/register.html')
        
        # Create user
        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Account created successfully! Please login.")
        return redirect('login')

    return render(request, 'Myapp/register.html')




def login_user(request):
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

       
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'Myapp/login.html', {'error': 'Invalid credentials'})

    return render(request, 'Myapp/login.html')



@login_required
def home(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()

 
    posts = Post14.objects.all().order_by('-created_at').prefetch_related('comments', 'likes')

    context = {
        'form': form,
        'posts': posts,
    }
    return render(request, 'Myapp/index.html', context)


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post14, id=post_id)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    # Return JSON instead of redirect
    return JsonResponse({
        "liked": liked,
        "likes": post.likes.count()
    })


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post14, id=post_id)

    if request.method == "POST":
        Comment.objects.create(
            post=post,
            user=request.user,
            text=request.POST.get('comment')
        )

    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def profile(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        bio = request.POST.get('bio')
        if bio:
            profile.bio = bio
        if 'profile_pic' in request.FILES:
            profile.profile_pic = request.FILES['profile_pic']
        profile.save()
        messages.success(request, "Profile updated!")
        return redirect('profile')

    posts = Post14.objects.filter(user=user)
    followers_count = Follow.objects.filter(following=user).count()
    following_count = Follow.objects.filter(follower=user).count()

    return render(request, 'Myapp/profile.html', {
        'user_profile': user,
        'posts': posts,
        'followers_count': followers_count,
        'following_count': following_count
    })




def delete_post(request, post_id):
    post = get_object_or_404(Post14, id=post_id)
    if post.user == request.user:
        post.delete()
    return redirect('home')

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Message sent successfully!")
            return redirect("contact")
    else:
        form = ContactForm()

    return render(request, "Myapp/contactus.html", {"form": form})

@login_required
def view_profile(request, username):
    # Prevent showing own profile in "other user view"
    if username == request.user.username:
        return redirect('my_profile')  # Redirect to your own profile page

    # Get the clicked user's profile
    user_profile = get_object_or_404(User, username=username)
    
    # Pass only the clicked user's info to template
    context = {
        'user_profile': user_profile,  # NOT request.user.profile
    }
    return render(request, 'Myapp/other.html', context)


@login_required
def follow_toggle(request, username):
    target_user = get_object_or_404(User, username=username)
    follow_obj, created = Follow.objects.get_or_create(follower=request.user, following=target_user)

    if not created:
        follow_obj.delete()  

    return redirect('profile_view', username=username)


def report_post(request, post_id):
    post = get_object_or_404(Post14, id=post_id)
    if post.user == request.user:
        return HttpResponseForbidden()
    # save report
    return redirect('home')
