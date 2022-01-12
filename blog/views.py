from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import Post,Comment
from django import db
from .forms import PostForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from bs4 import BeautifulSoup
from django.http import JsonResponse
def register_user(request):
    page = "register"
    form = UserCreationForm()
    context = {
        "form":form,
        "page":page,
    }
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if User.objects.filter(username=username).exists():
            messages.error(request,"Username already exists!")
            return render(request,"blog/register-login.html",context)
        
        if password1 != password2:
            messages.error(request,"Passwords do not match.")
            return redirect("register-user")
        elif len(password1) < 8:
            messages.error(request,"Password must be atleast 8 characters.")
            return redirect("register-user")
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect("home")
        else:
            messages.error(request,"something went wrong")
            # return render(request,"blog/register_user.html",context)
    return render(request,"blog/register-login.html",context)

def login_view(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,"User does not exist.")
            return redirect("login")
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect("home")
        else:
            messages.error(request,"Password does not match.")

    context = {"page":page}
    return render(request,"blog/register-login.html",context)


def logout_view(request):
    logout(request)
    return redirect("home")
def home(request):
    page = "public"
    posts = Post.objects.filter(private=False).order_by("-pub_date")
    context = {
        "posts":posts,
        "page":page
    }
    return render(request,"blog/like_ajax.html",context)
def private_home(request):
    page="private"
    posts = Post.objects.filter(user=request.user,private=True)
    context = {
        "posts":posts,
        "page":page
    }
    return render(request,"blog/home.html",context)




@login_required(login_url="login")
def create_post(request):
    if request.method == "POST":
        title = request.POST.get("title").title()
        body = request.POST.get("body")
        private = request.POST.get("private")
        if str(private) == "on":
            private = True
        else:
            private = False
        soup = BeautifulSoup(body,"html.parser")
        p_text = ""
        for p in soup.find_all("p"):
            p_text += p.get_text()
        p_text = p_text[:80] + "..."
        print(p_text)
        # print(body)
        user = request.user
        if title == "" or body == "":
            messages.error(request,"You did not enter anything in title or body field!")
            return redirect("create-post")
        Post.objects.create(user=user,body=body,title=title,home_desc=p_text,private=private)
        return redirect("home")
    form  =PostForm()
    return render(request,"blog/create_post.html",{"form":form})

@login_required(login_url="login")
def delete_post(request,pk):
    post = Post.objects.get(id=pk)
    try:
        referer = request.META['HTTP_REFERER']
    except KeyError:
        referer = "http://127.0.0.1:8000/home"
    if request.user != post.user:
        return redirect("home")
    if request.method == "POST":
        post.delete()
        return redirect("home")
    return render(request,"blog/delete_post.html",{"obj":post,"referer":referer})


def view_post(request,pk):
    post = Post.objects.filter(id=pk).first()
    context = {'post':post}
    return render(request,"blog/view_post.html",context)


def show_comp(request):
    posts = Post.objects.all().order_by("-pub_date")
    context = {
        "posts":posts
    }
    return render(request,"blog/comp-test.html",context)
def create_ref(request):
    form = PostForm()
    if request.method == "POST":
        title = request.POST.get("title").title()
        body = request.POST.get("body")
        soup = BeautifulSoup(body,"html.parser")
        p_text = ""
        for p in soup.find_all("p"):
            p_text += p.get_text()
        p_text = p_text[:80] + "..."
        print(p_text)
        # print(body)
        user = request.user
        if title == "" or body == "":
            messages.error(request,"You did not enter anything in title or body field!")
            return redirect("create-post")
        Post.objects.create(user=user,body=body,title=title,home_desc=p_text)
        return redirect("home")
    return render(request,"blog/create-post-refugee.html",{"form":form})

@login_required(login_url="login")
def like_post(request,post_id):
    post = Post.objects.get(id=post_id)
    print("this runs")
    db.connections.close_all()
    
    post.likes.add(request.user)
    likes = post.total_likes()
    serial_likes = {"likes":likes}
    return JsonResponse(serial_likes)

@login_required(login_url="login")
def unlike_post(request,post_id):
    post = Post.objects.get(id=post_id)
    post.likes.remove(request.user)
    likes = post.total_likes()
    serial_likes = {"likes":likes}
    return JsonResponse(serial_likes)
def show_test(request):
    print("hello")
    
def show_test_home(request):
    print("hello")


def test_view(request,pk):
    post = Post.objects.filter(id=pk).first()
    context = {'post':post}
    return render(request,"blog/view_post.html",context)


@login_required(login_url="login")
def make_public(request,pk):
    post = Post.objects.get(id=pk)
    post.private = False
    post.save()
    return True


@login_required(login_url="login")
def make_private(request,pk):
    post = Post.objects.get(id=pk)
    post.private = True
    post.save()
    return True