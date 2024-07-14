from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_register_page),
    path('register/user', views.register),
    path('login/user', views.login),
    path('logout', views.logout),
    path('shows', views.index),
    path('shows/new', views.new_show),
    path('create/show', views.create_new_show),
    path('shows/<int:id>', views.view_one_show),
    path('shows/<int:id>/edit', views.edit_show), 
    path('update/show/<int:id>', views.update_show),
    path('shows/<int:id>/destroy', views.delete_show)
    
]
