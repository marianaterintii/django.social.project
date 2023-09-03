# ROUTER module

"""
URL configuration for mini_social project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from mini_social.views import *
from django.urls import include, path

from django.contrib import admin


urlpatterns = [
    # here routes - adresa sitelor si functiile
    path("", homePage),
    path("signup", signupPage),
    path("signin", signinPage),

    #post routes
    path("post/create", addPost),
    path("post/save", savePost),
    
   # path("post/get", getPosts),
    path("post/delete", deletePost),
    path("post/update", updatePost),
    path("post/change", changePost),
    path("post/get/<int:post_id>", post_detail),


    #user routes
    path("user/register", registerUser),
    path("user/login", loginUser),
    path("user/logout", logoutUser),
    path("user/preferences/notifications", toggleUserNotification),
    
    # url parameters
    path("user/profile/<int:id>", userProfile),
    path("user/profile/edit/<int:id>", editUserProfile),
    path("user/add/friend/<int:id>", addUserFriend),
    path("user/remove/friend/<int:id>", removeUserFriend),

  
    path("profile", profilePage),

    
    # development
    path("__debug__/", include("debug_toolbar.urls")),

    #admin
    path("admin/", admin.site.urls)  
    
]
