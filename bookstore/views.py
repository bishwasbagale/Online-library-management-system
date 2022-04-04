from asyncio.windows_events import NULL
from base64 import urlsafe_b64decode, urlsafe_b64encode
import email
from bookapp import settings
from django.shortcuts import redirect, render,HttpResponse
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic
from bootstrap_modal_forms.mixins import PassRequestMixin
from .models import User, Book, Chat,Feedback
from django.contrib import messages
from django.db.models import Sum
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView
from .forms import ChatForm, BookForm, UserForm
from . import models
import operator
import itertools
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, logout
from django.contrib import auth, messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponseRedirect
from .forms import changepassword
from django.core.mail import send_mail,send_mass_mail
    

# Shared Views    
def logoutView(request):
    logout(request)
    return render(request,'bookstore/login.html')


def loginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            if user.is_admin or user.is_superuser:
                return redirect('dashboard')
            elif user.is_librarian:
                return redirect('librarian')
            else:
                
                return redirect('student')
        else:
            msg="Invalid username or password"
        return render(request,'bookstore/login.html',{'msg':msg})
       
    else:
        return render(request,'bookstore/login.html')
   
        





def registerView(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password = make_password(password)
        uname = User.objects.filter(username=username)
        emaillist = User.objects.filter(email = email)
    
        if(len(uname)>0):
            msg="Username is alredy exist"
            return render(request,'bookstore/register.html',{'msg':msg})
        elif(len(emaillist)>0):
            msg="email is alredy exist"
            return render(request,'bookstore/register.html',{'msg':msg})
        else:
            user = User(first_name=fname, last_name=lname, username=username, email=email, password=password, is_student=True)                         
            
            user.save()
            msg="Account was created successfully"
        
            return render(request,'bookstore/register.html',{'msg':msg})

    else:
        return render(request,'bookstore/register.html')
     
        
        
        
        
        
        

# student views
@login_required
def student(request):
    return render(request, 'student/home.html')


@login_required
def uabook_form(request):
    return render(request, 'student/add_book.html')


@login_required
def feedback_form(request):
    return render(request, 'student/send_feedback.html')

@login_required
def about(request):
    return render(request, 'student/about.html')

# This function takes unsorted array as an input 
# and returns sorted array.
def insertion_sort(arr):

    #loop over all the elements in the list 
    for i in range(1, len(arr)): 
  
        val = arr[i]
  
        # move elements of list [0..i-1], that are 
        # greater than val, to one position ahead 
        # of the current position 
        j = i-1
        while j >=0 and val < arr[j] : 
            arr[j+1] = arr[j] 
            j -= 1
        arr[j+1] = val
    
    return arr


# Python 3 program for recursive binary search.
# Modifications needed for the older Python 2 are found in comments.

# Returns index of x in arr if present, else -1
def binary_search(arr, low, high, x):

    # Check base case
    if high >= low:

        mid = (high + low) // 2

        # If element is present at the middle itself
        if arr[mid] == x:
            return mid

        # If element is smaller than mid, then it can only
        # be present in left subarray
        elif arr[mid] > x:
            return binary_search(arr, low, mid - 1, x)

        # Else the element can only be present in right subarray
        else:
            return binary_search(arr, mid + 1, high, x)

    else:
        # Element is not present in the array
        return -1


@login_required
def usearch(request):
   query = request.GET['query']
   Context ={}
   searchElem = Book.objects.all().filter(title = query)
   if(len(searchElem)==0):
       Context['message'] ="NO Such Element in Database"
       return render(request,"student/result.html",Context)
        
   else:
       for item in searchElem:
           searchId = item.id
       value = Book.objects.all()
       myVal = []
       for item in value:
           myVal.append(item.id)
        # print(myVal)
       myVal = insertion_sort(myVal)
       myIndex = binary_search(myVal,0,len(myVal),searchId)
        # print(myIndex)
       mytitle = myVal[myIndex]
       searchedValue = Book.objects.all().filter(id = mytitle)
       Context['files'] = searchedValue
       return render(request,'student/result.html',Context) 
 
        
@login_required
def send_feedback(request):
    if request.method == 'POST':
        feedback = request.POST['feedback']
        current_user = request.user
        user_id = current_user.id
        username = current_user.username
        feedback = username + " " + " says " + feedback

        a = Feedback(feedback=feedback)
        a.save()
        messages.success(request, 'Feedback was sent')
        return redirect('feedback_form')
    else:
        messages.error(request, 'Feedback was not sent')
        return redirect('feedback_form')



class UBookListView(LoginRequiredMixin,ListView):
    model = Book
    template_name = 'student/book_list.html'
    context_object_name = 'books'
    

    def get_queryset(self):
        return Book.objects.order_by('-id')


class UCreateChat(LoginRequiredMixin, CreateView):
    form_class = ChatForm
    model = Chat
    template_name = 'student/chat_form.html'
    success_url = reverse_lazy('ulchat')


    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class UListChat(LoginRequiredMixin, ListView):
    model = Chat
    template_name = 'student/chat_list.html'

    def get_queryset(self):
        return Chat.objects.filter(posted_at__lt=timezone.now()).order_by('posted_at')
    
def student_change_pass(request):
    if request.method == 'POST':
        fm = changepassword(user=request.user, data=request.POST)
        if fm.is_valid():
            fm.save()
            messages.add_message(request,messages.SUCCESS,'password change is successful')
            return HttpResponseRedirect('/')
    else:
        fm = changepassword(user=request.user)
    return render(request,'student/changepass.html',{'form':fm})












# Librarian views
@login_required    
def librarian_change_pass(request):
    if request.method == 'POST':
        fm = changepassword(user=request.user, data=request.POST)
        if fm.is_valid():
            fm.save()
            messages.add_message(request,messages.SUCCESS,'password change is successful')
            return HttpResponseRedirect('/')
    else:
        fm = changepassword(user=request.user)
    return render(request,'librarian/changepass.html',{'form':fm})

def librarian(request):
    book = Book.objects.all().count()
    user = User.objects.all().count()

    context = {'book':book, 'user':user}

    return render(request, 'librarian/home.html', context)


@login_required
def labook_form(request):
    return render(request, 'librarian/add_book.html')

@login_required
def labook(request):
    if request.method == 'POST':
        title = request.POST['title']
        author = request.POST['author']
        year = request.POST['year']
        publisher = request.POST['publisher']
        desc = request.POST['desc']
        cover = request.FILES['cover']
        pdf = request.FILES['pdf']
        current_user = request.user
        user_id = current_user.id
        username = current_user.username

        a = Book(title=title, author=author, year=year, publisher=publisher, 
            desc=desc, cover=cover, pdf=pdf, uploaded_by=username, user_id=user_id)
        a.save()
        messages.success(request, 'Book was uploaded successfully')
        return redirect('llbook')
    else:
        messages.error(request, 'Book was not uploaded successfully')
        return redirect('llbook')



class LBookListView(LoginRequiredMixin,ListView):
    model = Book
    template_name = 'librarian/book_list.html'
    context_object_name = 'books'
    paginate_by = 3

    def get_queryset(self):
        return Book.objects.order_by('-id')


class LManageBook(LoginRequiredMixin,ListView):
    model = Book
    template_name = 'librarian/manage_books.html'
    context_object_name = 'books'
    # paginate_by = 3

    def get_queryset(self):
        return Book.objects.order_by('-id')


class LViewBook(LoginRequiredMixin,DetailView):
    model = Book
    template_name = 'librarian/book_detail.html'

    
class LEditView(LoginRequiredMixin,UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'librarian/edit_book.html'
    success_url = reverse_lazy('lmbook')
    success_message = 'Data was updated successfully'


class LDeleteView(LoginRequiredMixin,DeleteView):
    model = Book
    template_name = 'librarian/confirm_delete.html'
    success_url = reverse_lazy('lmbook')
    success_message = 'Data was deleted successfully'


class LDeleteBook(LoginRequiredMixin,DeleteView):
    model = Book
    template_name = 'librarian/confirm_delete2.html'
    success_url = reverse_lazy('librarian')
    success_message = 'Data was dele successfully'



@login_required
def lsearch(request):
   query = request.GET['query']
   Context ={}
   searchElem = Book.objects.all().filter(title = query)
   if(len(searchElem)==0):
       Context['message'] ="NO Such Element in Database"
       return render(request,"librarian/result.html",Context)
        
   else:
       for item in searchElem:
           searchId = item.id
       value = Book.objects.all()
       myVal = []
       for item in value:
           myVal.append(item.id)
        # print(myVal)
       myVal = insertion_sort(myVal)
       myIndex = binary_search(myVal,0,len(myVal),searchId)
        # print(myIndex)
       mytitle = myVal[myIndex]
       searchedValue = Book.objects.all().filter(id = mytitle)
       Context['files'] = searchedValue
       return render(request,'librarian/result.html',Context) 
 
        

class LCreateChat(LoginRequiredMixin, CreateView):
    form_class = ChatForm
    model = Chat
    template_name = 'librarian/chat_form.html'
    success_url = reverse_lazy('llchat')


    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)




class LListChat(LoginRequiredMixin, ListView):
    model = Chat
    template_name = 'librarian/chat_list.html'

    def get_queryset(self):
        return Chat.objects.filter(posted_at__lt=timezone.now()).order_by('posted_at')




# Admin views

def dashboard(request):
    book = Book.objects.all().count()
    user = User.objects.all().count()
   
    context = {'book':book, 'user':user}

    return render(request, 'dashboard/home.html', context)

def create_user_form(request):
    choice = ['1', '0', 'student', 'Admin', 'Librarian']
    choice = {'choice': choice}

    return render(request, 'dashboard/add_user.html', choice)


class ADeleteUser(SuccessMessageMixin, DeleteView):
    model = User
    template_name='dashboard/confirm_delete3.html'
    success_url = reverse_lazy('aluser')
    success_message = "Data successfully deleted"



    
def update_data(request,id):
    if request.method == 'POST':
        pi = User.objects.get(pk=id)
        fm = UserForm(request.POST, instance=pi)
        if fm.is_valid:
            fm.save()
            return HttpResponseRedirect('/aluser/')
            
    else:
        pi = User.objects.get(pk=id)
        fm = UserForm(instance=pi)
    return render(request,'dashboard/edit_user.html',{'form':fm})

    


class ListUserView(generic.ListView):
    model = User
    template_name = 'dashboard/list_users.html'
    context_object_name = 'users'
    

    def get_queryset(self):
        return User.objects.order_by('-id')

def create_user(request):
    choice = ['1', '0', 'student', 'Admin', 'Librarian']
    choice = {'choice': choice}
    if request.method == 'POST':
            first_name=request.POST['first_name']
            last_name=request.POST['last_name']
            username=request.POST['username']
            userType=request.POST['userType']
            email=request.POST['email']
            password=request.POST['password']
            password = make_password(password)
            print("User Type")
            print(userType)
            if userType == "student":
                a = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password,is_student=True)
                a.save()
                print(a.is_student)
                messages.success(request, 'Member was created successfully!')
                return redirect('aluser')
            elif userType == "Admin":
                a = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password, is_admin=True,is_superuser=True)
                a.save()
                messages.success(request, 'Member was created successfully!')
                return redirect('aluser')
            elif userType == "Librarian":
                a = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password, is_librarian=True)
                a.save()
                messages.success(request, 'Member was created successfully!')
                return redirect('aluser')    
            else:
                messages.success(request, 'Member was not created')
                return redirect('create_user_form')
    else:
        return redirect('create_user_form')


class ALViewUser(DetailView):
    model = User
    template_name='dashboard/user_detail.html'



class ACreateChat(LoginRequiredMixin, CreateView):
    form_class = ChatForm
    model = Chat
    template_name = 'dashboard/chat_form.html'
    success_url = reverse_lazy('alchat')


    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)




class AListChat(LoginRequiredMixin, ListView):
    model = Chat
    template_name = 'dashboard/chat_list.html'

    def get_queryset(self):
        
        return Chat.objects.filter(posted_at__lt=timezone.localtime()).order_by('posted_at')


@login_required
def aabook_form(request):
    return render(request, 'dashboard/add_book.html')


@login_required
def aabook(request):
    if request.method == 'POST':
        title = request.POST['title']
        author = request.POST['author']
        year = request.POST['year']
        publisher = request.POST['publisher']
        desc = request.POST['desc']
        cover = request.FILES['cover']
        pdf = request.FILES['pdf']
        current_user = request.user
        user_id = current_user.id
        username = current_user.username

        a = Book(title=title, author=author, year=year, publisher=publisher, 
            desc=desc, cover=cover, pdf=pdf, uploaded_by=username, user_id=user_id) 
        
        
        message1 = ('Subject here', 'Here is the message', 'bishwas12345bagale@gmail.com', ['bagalebishwas888@gmail.com', 'other@example.com'])
        if send_mass_mail((message1), fail_silently=False):
            return HttpResponse('yes')
            a.save()
        else:
            return HttpResponse('no')
      
        
        #     # write email code
        # subject = 'online library management system login'
        # message = "Hello new book"+title+"is uploaded"
        # from_email = settings.EMAIL_HOST_USER
        # email_list = User.objects.all()
        # context = []
        # for em in email_list:
        #     context.append(em.email)
        # to_list = context
        # if send_mail(subject,message,from_email,to_list):
        #     return HttpResponse('yes')     
        #     a.save()
        # else:
        #     return HttpResponse("no")
        # messages.success(request, 'Book was uploaded successfully')
        # return redirect('ambook')
    else:
        messages.error(request, 'Book was not uploaded successfully')
        return redirect('aabook_form')


class ABookListView(LoginRequiredMixin,ListView):
    model = Book
    template_name = 'dashboard/book_list.html'
    context_object_name = 'books'
    paginate_by = 3

    def get_queryset(self):
        return Book.objects.order_by('-id')




class AManageBook(LoginRequiredMixin,ListView):
    model = Book
    template_name = 'dashboard/manage_books.html'
    context_object_name = 'books'
    # paginate_by = 3

    def get_queryset(self):
        return Book.objects.order_by('-id')




class ADeleteBook(LoginRequiredMixin,DeleteView):
    model = Book
    template_name = 'dashboard/confirm_delete2.html'
    success_url = reverse_lazy('ambook')
    success_message = 'Data was delete successfully'


class ADeleteBookk(LoginRequiredMixin,DeleteView):
    model = Book
    template_name = 'dashboard/confirm_delete.html'
    success_url = reverse_lazy('dashboard')
    success_message = 'Data was delete successfully'


class AViewBook(LoginRequiredMixin,DetailView):
    model = Book
    template_name = 'dashboard/book_detail.html'




class AEditView(LoginRequiredMixin,UpdateView):
    model = Book
    form_class = BookForm
    # fields="__all__"
    template_name = 'dashboard/edit_book.html'
    success_url = reverse_lazy('ambook')
    success_message = 'Data was updated successfully'




class AFeedback(LoginRequiredMixin,ListView):
    model = Feedback
    template_name = 'dashboard/feedback.html'
    context_object_name = 'feedbacks'
    paginate_by = 3

    def get_queryset(self):
        return Feedback.objects.order_by('-id')
                  

@login_required
def asearch(request):
    query = request.GET['query']
    # print(query)
    # print(type(query))
    
   
    # print(myVal)
    # print(myVal[2])
    
    Context = {}
    searchElem = Book.objects.all().filter(title = query)
    if(len(searchElem)==0):
        Context['message'] ="NO Such Element in Database"
        return render(request,"dashboard/result.html",Context)
        
    else:
        for item in searchElem:
            searchId = item.id
        value = Book.objects.all()
        myVal = []
        for item in value:
            myVal.append(item.id)
        myVal = insertion_sort(myVal)
        # print(myVal)
        myIndex = binary_search(myVal,0,len(myVal),searchId)
        # print(myIndex)
        mytitle = myVal[myIndex]
        searchedValue = Book.objects.all().filter(id = mytitle)
        Context['files'] = searchedValue
        return render(request,'dashboard/result.html',Context) 


@login_required    
def admin_change_pass(request):
    if request.method == 'POST':
        fm = changepassword(user=request.user, data=request.POST)
        if fm.is_valid():
            fm.save()
            messages.add_message(request,messages.SUCCESS,'password change is successful')
            return HttpResponseRedirect('/')
    else:
        fm = changepassword(user=request.user)
    return render(request,'dashboard/changepass.html',{'form':fm})
















