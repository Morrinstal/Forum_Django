from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views
from django.contrib.auth import views as auth_views 

urlpatterns = [
    path('homepage/',views.homepage,name='homepage'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'), 
    path('profile/<str:username>/', views.user_profile, name='profile'),
    path('logout/',auth_views.LogoutView.as_view(next_page='homepage'),name='logout'),

    path('post/<int:pk>/add_comment/', views.add_comment, name='add_comment'),
    path('comment/<int:pk>/delete/', views.delete_comment, name='delete_comment'),

    path('', views.category_list, name='category_list'),
    path('category/<int:pk>/', views.category_detail, name='category_detail'),
    path('category/<int:id>/delete/', views.delete_category, name='delete_category'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('category/create/', views.create_category, name='create_category'),
    path('category/<int:pk>/create_post/', views.create_post, name='create_post'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('like/<int:pk>/', views.like_post, name='like_post'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
