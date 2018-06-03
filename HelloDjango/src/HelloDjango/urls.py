"""HelloDjango URL Configuration

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
from django.urls import path, include
#미디어 파일 경로를 설정하기 위해 추가한 모듈
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('social_django.urls', namespace='social')),
    path('polls/', include('polls.urls')),
    path('customuser/', include('customuser.urls')),
    path('blog/',include('Blog.urls')),
]
#Pillow 라이브러리 : 이미지와 관련된 기능이 있는 모듈
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)














