from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('courses/', views.courses, name='courses'),
    path('courses/<int:id>/', views.courseId, name='courseId'), # DO I NEED UNIQUE NAME? NAME + STR(ID)?

    path('applications/<int:id>/', views.appId, name='appId'),

    path('user/', views.createUser, name='createUser'),
    path('user/login/', views.login, name='login'),
    path('user/logout/', views.logout, name='logout'),
    path('user/<int:id>/application/', views.createApp, name='createApp'),
]