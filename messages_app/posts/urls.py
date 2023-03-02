from django.urls import path
from . import views


urlpatterns = [
    path('', views.userregister, name="user-register"),
    path('login/', views.userlogin, name="user-login"),
    path('logout/', views.userlogout, name="user-logout"),
    path('postList/',views.postsList,name='posts'),
    path('postList/<str:pk>/', views.myposts, name="myposts"),
    path('postList/<str:pk>/like/', views.postlike, name="postlike"),
    path('postList/<str:pk>/postcreate/', views.postCreate, name='postCreate'),
    path('post-api/',views.apiOverview,name='Messages-overview'),
    path('post-api/post-create/', views.postcreateandview, name='post-create'),
    path('post-api/post-list/', views.postList, name="post-lists"),
    path('post-api/post-list/<str:pk>/', views.postDetail, name="post-Details"),
    path('post-api/post-list/<str:pk>/like/', views.postLike, name="post-like"),
]