from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('creator_studio_login', views.creator_studio_login, name='creator_studio_login'),
    path('creator_studio_login/register', views.register, name='register'),
    path('view_admin', views.view_admin, name='view_admin'),
    path('add_admin', views.add_admin, name='add_admin'),
    path('add_admin/add_user', views.add_user, name='add_user'),
    path('view_admin/all_users', views.all_users, name='all_users'),
    path('view_admin/delete_user', views.delete_user, name='delete_user'),
    path('edit_admin', views.edit_admin, name='edit_admin')
]