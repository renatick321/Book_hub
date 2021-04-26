from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'api'

urlpatterns = [
	path('', views.info, name='info'),
	path('get_popular/', views.get_popular_, name='get_popular'),
	path('get_lasts/', views.get_lasts, name='get_lasts'),
	path('get_book/<int:book_id>', views.get_book, name='get_book'),
	#path('get_friends/<int:user_id>', views.get_friends, name='get_friends'),
	path('get_chapter/<int:book_id>/<int:chapter_id>', views.get_chapter, name='get_chapter')
]