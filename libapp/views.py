from django.shortcuts import render,redirect
from .forms import BookForm
from .models import Book
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .serializers import BookSerializer
from rest_framework import generics
from .models import Book

# Create your views here.

def home(request):
    return render(request,'home.html')

@login_required
def addbook(request):
    if request.method == 'POST':
        form=BookForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request,'addbook.html',{'form':BookForm(),'msg':'Book added Successfully'})
    else:
        form=BookForm()
    return render(request,'addbook.html',{'form':form})        

@login_required
def viewbooks(request):
    bookdata = Book.objects.all()
    return render(request,'viewbooks.html', {'bookdata':bookdata})

@login_required
def deletebook(request,id):
    book=Book.objects.get(id=id)
    book.delete()
    bookdata=Book.objects.all()
    return render(request,'viewbooks.html',{'bookdata':bookdata,'msg':'Bookdeleted'})

@login_required
def searchbook(request):
    if request.method == "POST":
        id=request.POST.get(id)
        book=Book.objects.get(id=id)
        return render(request,'searchbook.html',{'book':book})
    
    return render(request, 'searchbook.html')


def signup(request):
    if request.method=="POST":
        form = UserCreationForm(request.POST)#create an object of usercreationforms
        if form.is_valid():
            form.save()
            return render(request,'signup.html',{'form':UserCreationForm(),'msg':'User Created Successfully'})
    else:
        form=UserCreationForm()
    return render(request,'signup.html',{'form':form})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html',{'form':AuthenticationForm()})

def logout_view(request):
    logout(request)
    return redirect('home')

class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
class BookRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer    