"""
URL configuration for justdial project.

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
from justdial import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    # main page
    path('', views.home),

    # login signup logout page
    path('login', views.login),
    path('signup', views.signup),
    path('logout', views.logout),

    # login signup page data
    path('actionsignup', views.actionsignup),
    path('actionlogin', views.actionlogin),

    # Bussinesses in Main Category Page
    path('category/<int:id>',views.category),

    # Main Bussiness
    path('bussiness/<int:id>',views.bussiness),

    # Edit Profile
    path('edit',views.edit), 
    path('editprofile',views.editprofile),

    # Change Password 
    path('changepassword',views.changepassword),
    path('passwordchange',views.passwordchange),
    
    # Search Bussiness
    path('search',views.search),

    # Comment and rating url 
    path('sharereply',views.sharereply),

    # Add District 
    path("adddistrict",views.adddistrict),

    # Dashboard Page 
    path("dashboard",views.dashboard),
    path("views",views.views),
    path("EditProfile",views.EditProfile),
    path("ChangePassword",views.ChangePassword),
    path("DashChangePassword",views.DashChangePassword),

    # Add Bussiness 
    
    path('addbussinessdata', views.addbussinessdata),
    path('UpdateBusiness', views.UpdateBusiness),
    
    # Views 
    path("loadmore",views.loadmore),

    # Advertisement
    path("advertisement",views.advertisement),
    path("advdata",views.advdata),

    # Gallery
    path("Gallery",views.gallery),
    path("galleryimg",views.galleryimg),

    # Bussiness Lead
    path("leadbussiness",views.leadbussiness),

    # Appointment
    path("appointment/<int:id>",views.appointments),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
