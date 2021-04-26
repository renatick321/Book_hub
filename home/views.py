from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Book, Tag, Genre, Chapter, Person
from .forms import BookCreateForm, ChapterForm
from django.utils import timezone
import datetime


def home(request):
	popular = Book.objects.all().order_by("-views")
	if len(popular) >= 20:
		popular = popular[:20]
	lasts = Book.objects.all().order_by("-pub_date")
	if len(lasts) >= 20:
		lasts = lasts[:20]
	return render(request, "home/home_page.html", {'user': request.user, 'populars': popular, "lasts": lasts})

def addbook(request, book_id):
	book = get_object_or_404(Book, id=book_id)
	user = get_object_or_404(Person, user_id=request.user.id) #Защита от незареганных 
	user.read.add(book)
	return redirect(f"/book/{book_id}")

def popular(request):
	now = datetime.datetime.now()
	year = [timezone.now() - timezone.timedelta(365), timezone.now()]
	month = [timezone.now() - timezone.timedelta(30), timezone.now()]
	week = [timezone.now() - timezone.timedelta(7), timezone.now()]
	books_y = Book.objects.filter(pub_date__range=year).order_by("-views")
	books_m = Book.objects.filter(pub_date__range=month).order_by("-views")
	books_w = Book.objects.filter(pub_date__range=week).order_by("-views")
	return render(request, "home/section.html", {'user': request.user, "title": "Популярные", "books_y": books_y, 
		"books_m": books_m, "books_w": books_w})

def book_create(request):
	if not request.user.is_authenticated:
		return redirect("/")
	if request.method == "POST":
		form = BookForm(request.POST)
		if form.is_valid():
			book = Book()
			data = form.cleaned_data
			book.title = data["title"] 
			book.image = data["image"] 
			book.description = data["description"] 
			book.price = data["price"] 
			book.tags = data["tags"] 
			book.genres = data["genres"] 
			book.author_name_id = request.user.id
			book.save()
			return redirect('/')
	return render(request, "home/book_create.html", {'user': request.user, "form": BookForm()})

def get_tag(request, slug):
	tag = get_object_or_404(Tag, slug=slug)
	books = tag.books.all
	return render(request, "home/for_column_view.html", {'user': request.user, "title": tag, "books": books})

def get_genre(request, slug):
	genre = get_object_or_404(Genre, slug=slug)
	books = genre.books.all
	return render(request, "home/for_column_view.html", {'user': request.user, "title": genre, "books": books})

def tag_list(request):
	tags = Tag.objects.all
	return render(request, "home/tag_list.html", {'user': request.user, "title": "Теги", "tags": tags})

def genre_list(request):
	genres = Genre.objects.all
	return render(request, "home/genre_list.html", {'user': request.user, "title": "Жанры", "genres": genres})

def rec_book(request):
	books = Book.objects.order_by('-pub_date')
	return render(request, "home/section.html", {'user': request.user, "title": "Недавние", "books": books})

def book(request, book_id):
	book = get_object_or_404(Book, id=book_id)
	book.views += 1
	book.save()
	chapters = Chapter.objects.filter(book_id=book_id).order_by("-num")
	chapters_ = chapters[::-1]
	try:
		in_libr = request.user.person.read.get(id=book_id)
	except Book.DoesNotExist:
		in_libr = False
	return render(request, "home/book.html", {'user': request.user, "book": book, 
											  "chapters": chapters, "chapters_": chapters_, 'in_libr': in_libr})

def chapter(request, book_id, number):
	chapters = Chapter.objects.filter(book_id=book_id)
	chapters = chapters.filter(num=number)
	if len(chapters) == 0:
		raise Http404
	chapter = chapters[0]
	book = get_object_or_404(Book, id=book_id)
	book.views += 1
	book.save()
	next_ = False
	back_ = False
	try:
		for i in range(1, 13):
			try: 
				a = Chapter.objects.filter(book_id=book_id).get(num=(number + i))
				next_ = a
				break
			except Exception as e:
				print(e)
	except Exception as e:
		print(e)
	try:
		for i in range(1, 13):
			try: 
				a = Chapter.objects.filter(book_id=book_id).get(num=(number - i))
				back_ = a
				break
			except Exception as e:
				print(e)
	except Exception as e:
		print(e)
	return render(request, "home/only_text.html", {'user': request.user, "chapter": chapter, "next_": next_, "back_": back_})


def first_best(request, book_id):
	if not request.user.is_authenticated:
		return redirect("/")
	user = get_object_or_404(Person, user_id=request.user.id)
	user.first_best_id = book_id
	user.save()
	return redirect(f"/cabinet/{request.user.id}")


def second_best(request, book_id):
	if not request.user.is_authenticated:
		return redirect("/")
	user = get_object_or_404(Person, user_id=request.user.id)
	user.second_best_id = book_id
	user.save()
	return redirect(f"/cabinet/{request.user.id}")


def third_best(request, book_id):
	if not request.user.is_authenticated:
		return redirect("/")
	user = get_object_or_404(Person, user_id=request.user.id)
	user.third_best_id = book_id
	user.save()
	return redirect(f"/cabinet/{request.user.id}")


def fourth_best(request, book_id):
	if not request.user.is_authenticated:
		return redirect("/")
	user = get_object_or_404(Person, user_id=request.user.id)
	user.fourth_best_id = book_id
	user.save()
	return redirect(f"/cabinet/{request.user.id}")


def fifth_best(request, book_id):
	if not request.user.is_authenticated:
		return redirect("/")
	user = get_object_or_404(Person, user_id=request.user.id)
	user.fifth_best_id = book_id
	user.save()
	return redirect(f"/cabinet/{request.user.id}")