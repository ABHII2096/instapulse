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
from .models import Profile,Report
from .forms import ReportForm
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
   
    if username == request.user.username:
        return redirect('my_profile') 

   
    user_profile = get_object_or_404(User, username=username)
    
   
    context = {
        'user_profile': user_profile, 
    }
    return render(request, 'Myapp/other.html', context)




@login_required
def report_post(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post14, id=post_id)
        form = ReportForm(request.POST)

        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user
            report.post = post
            report.save()
            return JsonResponse({'success': True})

    return JsonResponse({'success': False}, status=400)


@login_required
def notifications(request):
    reports = Report.objects.filter(
        reporter=request.user,
        is_replied=True
    ).order_by('-created_at')

    return render(request, 'Myapp/notifications.html', {'reports': reports})



@login_required
def profile_view(request, username):
    user_profile = get_object_or_404(User, username=username)
    posts = Post14.objects.filter(user=user_profile)

    followers_count = Follow.objects.filter(following=user_profile).count()
    following_count = Follow.objects.filter(follower=user_profile).count()

    is_following = False
    if request.user != user_profile:
        is_following = Follow.objects.filter(
            follower=request.user,
            following=user_profile
        ).exists()

    context = {
        'user_profile': user_profile,
        'posts': posts,
        'followers_count': followers_count,
        'following_count': following_count,
        'is_following': is_following,
    }
    return render(request, 'Myapp/profile.html', context)





# views.py
@login_required
def follow_toggle(request, username):
    user_to_follow = get_object_or_404(User, username=username)

    if request.user != user_to_follow:
        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            following=user_to_follow
        )
        if not created:
            follow.delete()

    return redirect('profile', username=username)
