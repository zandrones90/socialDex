from django.urls import path
from . import views

#('nomedametterenellabarra/',views.funzione, nome=nome da assegnare nella pagina html)
urlpatterns = [
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('', views.home, name='home')
]