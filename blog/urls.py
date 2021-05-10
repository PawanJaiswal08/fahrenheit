from django.urls import path 
from . import views


urlpatterns = [
    
    # category
    path('travelling', views.travelling , name="travelling"),
    path('dailylife', views.dailyLife , name="dailylife"),
    path('technology', views.technology , name="technology"),
    path('art&literature', views.artAndLiterature , name="artAndLiterature"),
    path('sports', views.sports , name="sports"),
    path('education', views.education , name="education"),
    path('entertainment', views.entertainment , name="entertainment"),
    path('food', views.food , name="food"),
    path('fitness', views.fitness , name="fitness"),
    
    
    
    path('new_blog', views.new_blog , name="new_blog"),
    path('allblogs', views.allblogs , name="allblogs"),
    path('myblogs', views.myblogs , name="myblogs"),
    path('<str:slug>/' , views.postview , name="postview"),
    path('<str:slug>/updatepost/', views.updatepost , name="updatepost"),
    path('delete/<str:slug>/', views.del_post, name='del_post'),
    # path('deletecomment/<int:pk>/', views.del_comment, name='del_comment'),
    path('deletecomment/<str:slug>/<int:pk>/', views.del_comment, name='del_comment'),
    path('blogComment/<str:slug>/', views.blogComment, name="blogComment"),
    path('reply/<str:slug>/', views.blogComment, name="blogComment"),
]