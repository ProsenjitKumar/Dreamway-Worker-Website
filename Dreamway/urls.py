"""Dreamway URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from accounts.views import (
profile,
home,
#sub_profile,
register_page,
login_page,
user_logout,
lead_number,
contact_us,
about,
#balance,
info,
charts,
#base_template,
coming_soon,
coming_soon_profile,
all_tasks,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # ****************** Accounts ********************
    path('', home, name='home'),
    path('profile/', profile, name='profile'),
    #path('sub-profile/', sub_profile, name='sub_profile'),
    path('register/', register_page, name='register'),
    path('login/', login_page, name='login'),
    path('profile/', profile, name='profile'),
    path('logout/', user_logout, name='logout'),
    #path(r'', home, name='home'),
    path('lead-number/', lead_number, name='lead_number'),
    path('contact-us/', contact_us, name='contact'),
    path('about/', about, name='about'),
    #path('balance/', balance, name='balance'),
    path('dashboard-charts/', charts, name='charts'),
    path('account-info/', info, name='info'),
    #path('base/', base_template, name='base_template'),
    path('coming-soon/', coming_soon, name='coming_soon'),
    path('coming-soon-profile/', coming_soon_profile, name='coming_soon_profile'),
    path('all-tasks/', all_tasks, name='all_tasks'),
]
