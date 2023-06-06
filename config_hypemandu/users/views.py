from django.contrib import messages
from .forms import UserRegisterForm,EditUserForm,LoginForm
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from .models import sellerProduct
from django.contrib.auth.decorators import login_required
from django.views.defaults import page_not_found
from .models import UserProfile

def login_request(request):
	if request.user.is_authenticated:
		messages.error(request,"You are already logged in")
		return redirect('shop:product_list')
	else:
		if request.method == "POST":
			form = LoginForm(request, data=request.POST)
			if form.is_valid():
				username = form.cleaned_data.get('username')
				password = form.cleaned_data.get('password')
				latitude=form.cleaned_data.get('latitude')
				longitude=form.cleaned_data.get('longitude')
				print('latitude-longitude')
				print(latitude,longitude)
				user = authenticate(username=username, password=password)
				user_profile = UserProfile.objects.get(user_id=user.id)
				user_profile.latitude = latitude
				user_profile.longitude = longitude
				user_profile.save()
				# last_login=user.last_login
				# if last_login is None:
				# 	last_login=True
				# else:
				# 	last_login=False
				# request.session['last_login']=last_login
				is_owner=user.userprofile.is_owner
				if user is not None:
					if is_owner == True:
         
						login(request, user)
						messages.info(request, f"You are now logged in as Owner {username}.")
						return redirect('shop:product_list')
					else:
						login(request,user)
						messages.info(request,f'Logged in as Customer {username}')
						return redirect('shop:product_list')
				else:
					messages.error(request,"Invalid username or password.")
			else:
				messages.error(request,"Invalid username or password.")
	form = LoginForm()
	return render(request=request, template_name="users/login.html", context={
	 "form":form
	 })

def signup_request(request,isOwner):
	if request.method=='POST':
		form = UserRegisterForm(data=request.POST)
		if form.is_valid():
			form_f=form.save()
			user=User.objects.get(username=form_f.first_name)
			print(user.id)
			print(timezone.now())
			if isOwner == 'owner_signup':
				UserProfile.objects.create(user=user,is_owner=True)
			elif isOwner == 'customer_signup':
				print(isOwner)
				UserProfile.objects.create(user=user,is_owner=False)
			email=form.cleaned_data.get('email')
			messages.success(request,f'Account created for {email}.')
			return redirect('users:login')
		else:
			messages.error(request,f'Error occured while Signing up')				
			return redirect(reverse('users:signup', args=[isOwner]))
	else:			
		form_f = UserRegisterForm()
		if isOwner=='owner_signup':
			bool=True
		elif isOwner =='customer_signup':
			bool=False
		else:
			return page_not_found(request, exception=None, template_name='error/404.html')
		return render(request,'users/signup.html',context={
			'form':form_f,
			'bool':bool,
			})
	
@login_required
def logout_view(request):
	logout(request)
	return redirect('login')