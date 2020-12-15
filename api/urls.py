from django.urls import path, include
from . import views



urlpatterns=[
    path('', include('loguser.urls')),
    path('post/', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('admin_page/', views.admin_page, name='admin_page'),
    path('utente/<str:pk>/', views.post_utente, name='post_utente'),
    path('json/', views.postsjs, name='json'),
    path('get/', views.get_input, name='get'),

]