from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
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
	print(request.body.decode('utf-8'))
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		print(username)
		user = authenticate(username = username, password=password)
		
		if user is not None:
			print('Sesion iniciada')
			login(request, user)
			return redirect('home')
		else:
			print('Authentication failed')
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
		user = User.objects.create( username = username, email = email )
		user.set_password(password)
		user.save()

		#information_data
		data = UserData.objects.create(user = user, fullname =fullname )
		UserMedia.objects.create(user = user )

		return redirect('login')

	else:

		form = RegisterForm()

	return render(request, 'accounts/register.html')

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("home")

def home(request):
	return render(request, 'accounts/home.html')

class user_info(viewsets.ModelViewSet):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]

	def get_serializer_class(self):
		return UserInfoSerializer
	def get_queryset(self):

		username = self.request.query_params['username']
		user = User.objects.get(username=username)
		# print(UserData.objects.get(user=user).fullname) 
		info = UserData.objects.filter(user=user)
		return info
