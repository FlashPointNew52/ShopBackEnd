"""HelloDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include
from HelloDjango import views

urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('admin/', include('HelloDjango.admin_urls')),
    path('catalog/<str:sec>/<str:subs>/<str:slug>', views.CategoryApi.as_view()),
    path('catalog/<str:sec>/<str:subs>', views.CategoryApi.as_view()),
    path('catalog/<str:sec>', views.CategoryApi.as_view()),
    path('filters/<str:sec>', views.FilterApi.as_view()),
    path('filters/<str:sec>/<str:subs>', views.FilterApi.as_view()),
]
