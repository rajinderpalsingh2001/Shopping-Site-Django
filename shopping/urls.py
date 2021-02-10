"""shopping URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from myfunctions import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path("addcategory",addcategory),
    path("newcategory",newcategory),
    path("viewcategory",viewcategory),
    path("viewadmin",viewadmin),
    path("addadmin",addadmin),
    path("newadmin",newadmin),
    path("login",login),
    path("checklogin",checklogin),
    path("dashboard",dashboard),
    path("logout",logout),
    path("addproduct",addproduct),
    path("newproduct",newproduct),
    path("viewproduct",viewproducts),
    path("",shopperhomepage),
    path("shopperhomepage",shopperhomepage),
    path("categorypage",categorypage),
    path("selectcategory",selectcategory),
    path("getcategory",getcategory),
    path("cart",cart),
    path("resetsession",resetsession),
    path("cart_total",cart_total),
    path("checkout",checkout),
    path("getcart",getcart),
    path("makepayment",makepayment),
    path("ordersuccess",ordersuccess),
    path("orderfailure",orderfailure),
    path("vieworders",vieworders),
    path("getorders",getorders),
    path("showcategory",getcategory)
]
