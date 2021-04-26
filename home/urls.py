from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'home'

urlpatterns = [
	path('', views.home, name='home'),
	path("popular/", views.popular, name="popular"),
	path("book_create/", views.book_create, name="book_create"),
	path("tag/<str:slug>/", views.get_tag, name="get_tag"),
	path("tags/", views.tag_list, name="tag_list"),
	path("genre/<str:slug>/", views.get_genre, name="get_genre"),
	path("genre/", views.genre_list, name="genre_list"),
	path("book/<int:book_id>/", views.book, name="book"),
	path("book/<int:book_id>/<int:number>/", views.chapter, name="chapter"),
	path('add/<int:book_id>/', views.addbook, name='addbook'),
	path('first_best/<int:book_id>/', views.first_best, name='first_best'),
	path('second_best/<int:book_id>/', views.second_best, name='second_best'),
	path('third_best/<int:book_id>/', views.third_best, name='third_best'),
	path('fourth_best/<int:book_id>/', views.fourth_best, name='fourth_best'),
	path('fifth_best/<int:book_id>/', views.fifth_best, name='fifth_best'),
]