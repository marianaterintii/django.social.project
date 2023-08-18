# views module
from django.http import HttpResponse, HttpResponseForbidden
from django.template import loader
from datetime import datetime
from django.shortcuts import redirect, get_object_or_404, render
from random import randint
from django.contrib.auth.decorators import login_required
from .models import Post
from .models import Comment, User
from .forms import CommentForm
import re

from .models import CustomUser

from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib import messages
users = [
    {"username": "jonny", "created": "2000-01-01"},
    {"username": "marry", "created": "2000-01-02"},
    {"username": "pete", "created": "2000-01-03"},
    {"username": "pier", "created": "2000-01-04"},
    {"username": "vasilyi", "created": "2000-01-05"},
    {"username": "masha", "created": "2000-01-06"},
    {"username": "lily", "created": "2000-01-07"},
    
]
posts = [
    {"title": "First title", "created": "2001-01-01"},
    {"title": "Second title", "created": "2001-01-02"},
    {"title": "Third title", "created": "2001-01-03"},
    {"title": "Fourth title", "created": "2001-01-04"},
    {"title": "Fifth title", "created": "2001-01-05"},
]

def sort_users(user):
    return user["created"]

def sort_posts(post):
    return post["created"]

def homePage(request):
    template = loader.get_template("home.html") 
    

    # HW: sort users and posts by date descending
    
    users.sort(key=sort_users,reverse=True)
    posts.sort(key=sort_posts,reverse=True)
    show_notifications = request.session.get('show_notifications', None)
    return HttpResponse(template.render({
        "users": users[:5],
        "posts": posts[:3],
        "user": request.user,
        "show_notifications": show_notifications
        
        }, request))


def signupPage(request):
    template = loader.get_template("signup.html") 

    return HttpResponse(template.render({
        
        }, request))

def signinPage(request):
    template = loader.get_template("signin.html") 

    return HttpResponse(template.render({
        
        }, request))

def profilePage(request):
    return HttpResponse("User's page")


'''def postPage(request, id):
    template = loader.get_template("post/get.html") 

    post = Post.objects.get(pk=id)
  
    return HttpResponse(template.render({
        'post': post
        }, request))'''

# POST VIEWS
def addPost(request):
    template = loader.get_template("post/add-post.html") 

    return HttpResponse(template.render({
        
        }, request))

def savePost(request): # HttpRequest
    visitingUser = get_user (request) # User
    visitingUser = CustomUser.objects.get(pk=visitingUser.id)
    
    title = request.POST['title']
    body = request.POST['body']
        
    post = Post(title=title,body=body, author=visitingUser)
    post.save() 
        # HW : redirect to it's profile 
    return redirect (f"/user/profile/{visitingUser.id}")


  # HW: add comments to post

def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = Comment.objects.filter(post=post)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()        
    else:
        form = CommentForm()
    return render(request, "post/get.html", {'form': form, 
                                             'post': post, 
                                             'comments': comments})
    


'''def getPosts(request):
    template = loader.get_template("post/get.html") 

    posts = Post.objects.all() # afiseaza toate obiectele din post
    
    print(type(Post.objects)) # manager
    print(type(posts))        # QuerySet

    return HttpResponse(template.render({
        'posts': posts
        }, request))'''

def updatePost(request):
    template = loader.get_template("post/update.html") 
    
    id = request.GET["id"]

    # find the post by id
    post = Post.objects.get(pk=id)
  
    return HttpResponse(template.render({
        'post': post
        }, request))

def changePost(request):
    
    id = request.GET["id"]
    new_title = request.GET['title']
    new_body = request.GET['body']

    # find the post by id
    post = Post.objects.get(pk=id)
    post.title = new_title
    post.body = new_body

    post.save()
  
    return HttpResponse('Post updated succesufully')


def deletePost(request):
    id = request.GET["id"]

    #1. find the post by id
    post = Post.objects.get(pk=id)

    #2. delete
    post.delete()
    return HttpResponse("Post delete successufully")
#################

# User VIEWS
def registerUser(request):
    # req ---> FORM
    if request.method == "GET":
        template = loader.get_template("user/register.html") 
        return HttpResponse(template.render({}, request))
    elif request.method == "POST":

        username = request.POST ['username']
        if len(username) > 10 or not re.match(r'^(?=.*[a-zA-Z])(?=.*[0-9])[a-zA-Z0-9_]+$', username):                              
            messages.error(request, 'Invalid username. Usernames must be maximum 10 characters long and contain letters, numbers, and underscores.')
            return redirect("/user/register")
        
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose a different username.')
            return redirect("/user/register")
        
        email = request.POST ['email']
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            messages.error(request, 'Invalid email address. Please enter a valid email address.')
            return redirect("/user/register")
        
        password = request.POST['password']
        if len(password) < 6 or len(password) > 10:
            messages.error(request, 'Passwords must be between 6 and 10 characters long.')
            return redirect("/user/register")
        
        confirm_password = request.POST['confirm_password'] 
    # req ---> AUTH
        if password == confirm_password:
            CustomUser.objects.create_user(username, email, password)
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, 'successuful registration')
            return redirect("/")
        else:
            messages.error(request, 'password do not much')
            return redirect("/user/register")
        

def loginUser(request):
    if request.method == "GET":
        template = loader.get_template("user/login.html") 
        return HttpResponse(template.render({}, request))
    
    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
            
        if user is None: 
              messages.error(request, 'Wrong credentials')
              return redirect("/user/login")
        
        login(request, user)# save user

        messages.success(request, 'Login successufuly')
        return redirect("/")
    

def toggleUserNotification(request):
    visitingUser = get_user(request)
    toggle = request.GET.get('toggle', None) # method .get() pentru a scoate 
    # .POST.get() 

    if not toggle:
        request.session["show_notifications"] = False
    else:
        request.session["show_notifications"] = True
    return redirect(f"/user/profile/{visitingUser.id}")


def userProfile(request, id):
    # HW update user profile to show all posts

    if request.method == "GET":
        profileUser = CustomUser.objects.get(pk=id)
        visitingUser = get_user (request) # User
        visitingUser = CustomUser.objects.get(pk=visitingUser.id)
        template = loader.get_template("user/profile.html") 
        profileUserIsNotVisitingUserFriend = visitingUser.friends.all().contains(profileUser)
       
        userPosts = Post.objects.filter(author=profileUser) 
        
        return HttpResponse(template.render({
            'profileUser': profileUser, 
            'visitingUser': visitingUser,
            'userFriends': profileUser.friends.all(),
            'profileUserIsNotVisitingUserFriend': profileUserIsNotVisitingUserFriend,
            'userPosts': userPosts
            }, request))


def addUserFriend(request, id):
    if request.method == "GET":
        profileUser = CustomUser.objects.get(pk=id)
        visitingUser = get_user (request) # User
        visitingUser = CustomUser.objects.get(pk=visitingUser.id)
        visitingUser.friends.add(profileUser)
        visitingUser.save()
        return redirect (f"/user/profile/{visitingUser.id}")

# HW: remove friends
 
def removeUserFriend(request, id):
    if request.method == "GET":
        profileUser = CustomUser.objects.get(pk=id)
        visitingUser = get_user (request) # User
        visitingUser = CustomUser.objects.get(pk=visitingUser.id)
        if profileUser in visitingUser.friends.all():
            visitingUser.friends.remove(profileUser)
            visitingUser.save()
            messages.success(request, 'Friend deleted successufuly')
        return redirect (f"/user/profile/{visitingUser.id}")
        
def editUserProfile(request, id):
    if request.method == "GET":
        profileUser = CustomUser.objects.get(pk=id)
        visitingUser = get_user (request)
        if profileUser.id == visitingUser.id:
           template = loader.get_template("user/edit-profile.html") 
           return HttpResponse(template.render({
            'profileUser': profileUser, 
            'visitingUser': visitingUser
            }, request))
        else: 
            return HttpResponseForbidden('Access Denied!')
    elif request.method == 'POST':
        profileUser = CustomUser.objects.get(pk=id)
        visitingUser = get_user (request)
        if profileUser.id == visitingUser.id: # verifying id is a must,protects from hackers to find password or upload posts, edit profile
           avatar = request.FILES['avatar']
           avatar_file = open(f'public/uploads/{avatar}', 'wb+')
           for chunk in avatar.chunks():
               avatar_file.write(chunk)
        
           avatar_file.close()
           profileUser.avatar = f'/uploads/{avatar}'
           profileUser.save()
           return redirect(f'/user/profile/{profileUser.id}')
        else:
            return HttpResponseForbidden('Access Denied!')


def logoutUser(request):
     # save user info in a variable
     show_notifications = request.session.get('show_notifications', None)
     logout(request) # session.flush() deletes user info
     # recover data info while login back
     request.session['show_notifications'] = show_notifications
     return redirect("/")
        
    
    
       

