from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth



# Create your views here.

def accountshome(request): #Change this to home page in product later
	return render(request, 'accounts/home.html')
	


def register(request):
	if request.method == 'POST':

		if request.POST['password1'] == request.POST['password2']:
			try:
				user = User.objects.get(username=request.POST['username'])
				return render(request, 'accounts/register.html', {'error':'Username has already been taken'})
			except User.DoesNotExist:
				user = User.objects.create_user(username=request.POST['username'], password=request.POST['password2'], first_name=request.POST['firstName'], last_name=request.POST['lastName'] ,email=request.POST['eMail'])
				auth.login(request,user)
				return redirect('home_page')
		else:
			return render(request, 'accounts/register.html', {'error':'Password must match'})

	else:
		return render(request, 'accounts/register.html')

def login(request):
	if request.method == 'POST':
		user = auth.authenticate(username= request.POST['username'], password=request.POST['password'])
		if user is not None:
			auth.login(request, user)
			return redirect('home_page')
		else:
			return render(request, 'accounts/login.html',{'error':'username or password is incorrect'})

	else:
		return render(request, 'accounts/login.html')




def logout(request):
	if request.method == 'POST':
		auth.logout(request)
		return redirect('home_page')
	

# Create your views here.
