from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import RegisterForm
from .models import UserData
from MediaManager.models import UserMedia
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

def login_user(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username = username, password=password)
		
		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.success(request, ('There was an error while login, try again' ))
			return redirect('login')
	else:
		return render(request, 'accounts/login.html')

def register_user(request):
	if request.method == 'POST':
		username = request.POST['username']
		fullname = request.POST['fullname']
		email = request.POST['email']
		password = request.POST['password']
		password2 = request.POST['password_confirmation']

		if password and password2 and password!=password2:
			messages.error(request, "Password doesnt match")

		#user registration
		if User.objects.filter(username = username).exists():
			return HttpResponse(404)

		user = User.objects.create( username = username, email = email )
		user.set_password(password)
		user.save()

		#information_data
		data = UserData.objects.create(user = user, fullname = fullname )
		usermedia = UserMedia.objects.create(user = user )

		data.save()
		usermedia.save()

		login(request, user)
		return redirect('home')

	else:

		form = RegisterForm()

	return render(request, 'accounts/register.html')

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("home")

def home(request):
	return render(request, 'accounts/home.html')

def checkUsername(request):
	username = request.GET.get('username')
	print(username)
	# checks if a username aleady exist
	user = User.objects.filter(username = username)
	print(user.exists())
	return JsonResponse({'exists':user.exists()})