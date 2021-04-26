from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'cabinet'

urlpatterns = [
	path('<int:user_id>/', views.cabinet, name='cabinet'),
	path('registration/', views.reg, name='reg'),
	path('login/', views.log, name='login'),
	path('logout/', views.user_logout, name='logout'),
	path('add/<int:friend_id>/', views.add_friend, name='add_friend'),
	path('create/book/', views.bookcreate, name='bookcreate'),
	path('edit_me/', views.edit_user, name='edit_user'),
	path('unsubscribe/<int:friend_id>/', views.unsubscribe, name='unsubscribe'),
]