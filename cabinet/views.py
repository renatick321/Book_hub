from django.shortcuts import render
from .models import User
from .forms import RegForm, LoginForm, EditForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.utils import timezone
from home.models import Book, Person
from django.db.models.signals import post_save, class_prepared
from django.dispatch import receiver
from requests.exceptions import HTTPError
from django.contrib.auth import logout, authenticate, login
	

def cabinet(request, user_id):
	person = get_object_or_404(Person, user_id=user_id)
	d = {}
	d['human'] = get_object_or_404(User, id=user_id)
	if user_id == request.user.id:
		d['edit'] = True
	else:
		d['edit'] = False
		try:
			d['in_friends'] = get_object_or_404(User, id=request.user.id).person.friends.get(id=user_id)
		except User.DoesNotExist:
			d['in_friends'] = False
	d['written'] = Book.objects.filter(author_name_id=user_id)
	d['read'] = person.read.all
	d["user"] = request.user
	a = d["human"].users.all()
	d['readers'] = a if len(a) < 7 else a[0:6]
	a = d["human"].person.friends.all()
	d['subscriptions'] = a if len(a) < 7 else a[0:6]
	d['first_best'] = person.first_best
	d['second_best'] = person.second_best
	d['third_best'] = person.third_best
	d['fourth_best'] = person.fourth_best
	d['fifth_best'] = person.fifth_best
	return render(request, "cabinet/cabinet.html", d)

def add_friend(request, friend_id):
	if friend_id == request.user.id:# Ограничение чтобы пользователь не добавлял сам себя в друзья
		return redirect("/")
	try:
		get_object_or_404(User, id=request.user.id).person.friends.get(id=friend_id)
	except User.DoesNotExist:
		to_me = get_object_or_404(User, id=friend_id)
		i_to = get_object_or_404(User, id=request.user.id).person
		print(1)
		i_to.friends.add(to_me)
		i_to.save()
		return redirect(f'/cabinet/{friend_id}')

def unsubscribe(request, friend_id):
	if friend_id == request.user.id:# Ограничение чтобы пользователь не добавлял сам себя в друзья
		return redirect("/")
	to_me = get_object_or_404(User, id=friend_id)
	i_to = get_object_or_404(User, id=request.user.id).person
	i_to.friends.remove(to_me)
	return redirect(f"/cabinet/{friend_id}")

def reg(request):
	message = ''
	form = RegForm(request.POST or None)
	if form.is_valid():
		form.save()
		cd = form.cleaned_data
		user = authenticate(username=cd['username'], password=cd['password1'])
		login(request, user)
		return redirect('/')
	else:
		try:
			errors = form.errors.as_data()
			messages = [i for i in errors]
			message = str(errors[messages[-1]])
			first = message.find("'") + 1
			second = message.rfind("'") - 1
			message = message[first:second]
		except:
			pass
	return render(request, 'cabinet/registration.html', {'user': request.user, 'message': message})

def log(request):
	form = LoginForm(request.POST or None)
	if form.is_valid():
		cd = form.cleaned_data
		user = authenticate(username=cd['username'], password=cd['password'])
		if user is not None:
			login(request, user)
			request.user = 'renat'
			print(request.user, 22)
			return redirect('/')
	return render(request, 'cabinet/login.html', {'user': request.user, })#

def user_logout(request):
	logout(request)
	return redirect('/')

def bookcreate(request):
	human = get_object_or_404(Person, user_id=request.user.id)
	form = LoginForm(request.POST or None)
	if form.is_valid():
		cd = form.cleaned_data
	return render(request, "cabinet/book_create.html", {"form": LoginForm()})


def edit_user(request):
	if not request.user.is_authenticated:
		return redirect("/")
	form = EditForm(request.POST, request.FILES)
	if form.is_valid():
		cd = form.cleaned_data
		user = get_object_or_404(User, id=request.user.id)
		user.image = cd['image']
		user.location = cd['location']
		user.username = cd['username']
		user.save()
		return redirect('/')
	else:
		try:
			errors = form.errors.as_data()
			messages = [i for i in errors]
			message = str(errors[messages[-1]])
			first = message.find("'") + 1
			second = message.rfind("'") - 1
			message = message[first:second]
		except:
			pass
	return render(request, 'cabinet/user_edition.html', {'form': form})



@receiver(post_save, sender = User)
def add_person(instance, **kwargs):
	try:
		person = get_object_or_404(Person, user_id=instance.id) # Если не найдено намерено вызывается ошибка 404
	except:
		person = Person()
		person.user_id = instance.id
		person.save()


#@receiver(post_save, sender=Book)
#def add_book_1(instance, **kwargs):
#	try:
#		book = get_object_or_404(Book, id=instance.id)
#		user = get_object_or_404(Person, user_id=1) #Защита от незареганных 
#		user.read.add(book)
#	except:
#		pass