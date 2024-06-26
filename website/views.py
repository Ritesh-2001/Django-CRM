from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record

def home(request):
    records = Record.objects.all()


    # Check to see if loggin in
    if request.method == 'POST':
        username = request.POST['username'] # uername because of the'name' in the form in home.html
        password = request.POST['password']
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        # If user is not None
        if user is not None:
            login(request, user)
            messages.success(request, ('You have been logged in!'))
            return redirect('home')
        else:
            messages.success(request, ('Error logging in - Please try again...'))
            return redirect('home')
    else:
        return render(request, 'home.html', {'records': records})



def logout_user(request):
    logout(request)
    messages.success(request, ('You have been logged out!'))
    return redirect('home')
 
def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            #Authenticate and login user
            username = form.cleaned_data['username'] # username because of the'name' in the form in register.html
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password) 
            login(request, user)
            messages.success(request, ('You have been successfully registered!'))
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})
    return render(request, 'register.html', {'form':form})

def customer_record(request, pk):
    if request.user.is_authenticated:
        # Lookup records
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record': customer_record})
    else:
        messages.success(request, ('Please login to view customer records!'))
        return redirect('home')

def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, ('Customer Record has been deleted!'))
        return redirect('home')
    else:
        messages.success(request, ('Please login to delete customer records!'))
        return redirect('home')

def add_record(request):
	form = AddRecordForm(request.POST or None)
	if request.user.is_authenticated:
		if request.method == "POST":
			if form.is_valid():
				add_record = form.save()
				messages.success(request, "Record Added...")
				return redirect('home')
		return render(request, 'add_record.html', {'form':form})
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('home')

def update_record(request, pk):
	if request.user.is_authenticated:
		current_record = Record.objects.get(id=pk)
		form = AddRecordForm(request.POST or None, instance=current_record)
		if form.is_valid():
			form.save()
			messages.success(request, "Record Has Been Updated!")
			return redirect('home')
		return render(request, 'update_record.html', {'form':form})
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('home')