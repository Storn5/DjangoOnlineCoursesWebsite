from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('courses/', views.courses, name='courses'),
    path('courses/<int:Cid>/', views.courseId, name='courseId'), # DO I NEED UNIQUE NAME? NAME + STR(ID)?

    path('applications/<int:Aid>/', views.appId, name='appId'),

    path('user/', views.createUser, name='createUser'),
    path('user/login/', views.my_login, name='login'),
    path('user/logout/', views.my_logout, name='logout'),
    path('user/application/', views.createApp, name='createApp'),
]