"""
URL configuration for weight_loss_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from weightapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home1, name='home'),
    path('sign-up/', views.signUp, name='signup'),
    path('log-in/', views.logIn, name='login'),
    path('log-out/', views.logOut, name='logout'),
    path('add-weight/', views.add_weight, name='addweight'),
    path('weight-list/', views.weight_list, name='weightlist'),
    path('edit-weight/<int:pk>/', views.edit_weight, name='editweight'),
    path('delete-weight/<int:pk>/', views.delete_weight, name='deleteweight'),
    path('weight-loss/', views.weight_loss, name='weightloss'),
]
