"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import include, path
from django.conf.urls import url
# from rest_framework import routers
from django.contrib.auth.models import User, Group
# from ebay.viewsets import ProductViewSet

admin.site.site_header = "eBay Admin"
admin.site.site_title = "eBay Admin Portal"
admin.site.index_title = "Welcome to eBay Researcher Portal"
# admin.site.unregister(User)
# admin.site.unregister(Group)

# router = routers.DefaultRouter()
# router.register(r'products', ProductViewSet)

urlpatterns = [
    # url('admin/', admin.site.urls),
    # url('ebay/', admin.site.urls),
    # path('ebay/', include('ebay.urls')),
    # url(r'^', include(router.urls)),
    url(r'^', admin.site.urls),
]