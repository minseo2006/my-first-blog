'''
Created on 2018. 5. 26.

@author: main
'''
from django.urls import path
from .views import *
from django.contrib.auth import views
#from .views import sign
app_name = 'customuser'

urlpatterns=[
    path('sign/',sign,name='sign'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name="logout")
    #path('login/',login,name='login'),
    #path('logout/',logout,name='logout'),
    ]


