from django.shortcuts import render
from cabinet.models import User
from home.models import Book, Tag, Genre, Chapter, Person
import json
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.


def get_popular_(request):
	popular = Book.objects.all().order_by("-views")
	if len(popular) >= 20:
		popular = popular[:20]
	data = {"popular": []}
	for book in popular:
		d = {"title": book.title, "image": book.image.url, "author_name": str(book.author_name),
		     "second_author": str(book.second_author), 'third_author': str(book.third_author), 'description': book.description,
		     "pub_date": str(book.pub_date), 'status': book.status}
		data['popular'].append(d)
	print(json.dumps(data))
	return HttpResponse(json.dumps(data))


def info(request):
	return render(request, "info.html")


def get_lasts(request):
	lasts = Book.objects.all().order_by("-pub_date")
	if len(lasts) >= 20:
		lasts = lasts[:20]
	data = {"lasts": []}
	for book in lasts:
		d = {"title": book.title, "image": book.image.url, "author_name": str(book.author_name),
		     "second_author": str(book.second_author), 'third_author': str(book.third_author), 'description': book.description,
		     "pub_date": str(book.pub_date), 'status': book.status}
		data['lasts'].append(d)
	print(json.dumps(data))
	return HttpResponse(json.dumps(data))


def get_book(request, book_id):
	try:
		book = Book.objects.get(id=book_id)
	except Book.DoesNotExist:
		book = None
		return HttpResponse(json.dumps({"book": book}))
	chapters = Chapter.objects.filter(book_id=book_id).order_by("-num")
	chapters_ = chapters[::-1]
	lst = []
	for i in chapters_:
		lst.append(str(i.title))
	return HttpResponse(json.dumps({"book": str(book), "chapters": lst}))


def get_friends(request, user_id):
	pass


def get_chapter(request, book_id, chapter_id):
	try:
		book = Book.objects.get(id=book_id)
	except Book.DoesNotExist:
		book = None
		return HttpResponse(json.dumps({"book": book}))
	try:
		chapter = Chapter.objects.filter(book_id=book_id).get(num=chapter_id)
	except Chapter.DoesNotExist:
		chapter = None
		return HttpResponse(json.dumps({"chapter": chapter}))
	except Http404:
		chapter = None
		return HttpResponse(json.dumps({"chapter": chapter}))
	data = {"book": str(chapter.book), "num": chapter.num, "title": chapter.title, 
	        "text": chapter.txt, "pub_date": str(chapter.pub_date)}
	return HttpResponse(json.dumps(data))