from django.urls import path
from polls import views

app_name = 'polls' #해당하는 urls파일의 별칭을 설정
urlpatterns = [ 
    path('', views.index , name ='index'), #"polls:index"
    path('<int:question_id>/', views.detail ,name ='detail'), #"polls:detail"
    path('<int:question_id>/vote/', views.vote ,name ='vote'), #"polls:vote"
    path('<int:question_id>/results/', views.results ,name ='results'), #"polls:results"
    path('registerQ/', views.registerQ, name ='registerQ'),
    path('registerC/<int:question_id>/', views.registerC, name ='registerC'),
    path('deleteQ/<int:question_id>/',views.deleteQ , name = "deleteQ" ),
    path('deleteC/<int:choice_id>/', views.deleteC, name='deleteC'),
    path('search/',views.search,name='search'),
]








