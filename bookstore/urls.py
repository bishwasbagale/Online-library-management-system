from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [

# Shared URL's


 path('', views.loginView, name='login'),
 path('logout/', views.logoutView, name='logout'),
 path('register/', views.registerView, name='register'),



 # Librarian URL's
 path('librarian/', views.librarian, name='librarian'),
 path('labook_form/', views.labook_form, name='labook_form'),
 path('labook/', views.labook, name='labook'),
 path('llbook/', views.LBookListView.as_view(), name='llbook'),
 path('lsearch/', views.lsearch, name='lsearch'),
 path('ldbook/<int:pk>', views.LDeleteBook.as_view(), name='ldbook'),
 path('lmbook/', views.LManageBook.as_view(), name='lmbook'),
 path('ldbookk/<int:pk>', views.LDeleteView.as_view(), name='ldbookk'),
 path('lvbook/<int:pk>', views.LViewBook.as_view(), name='lvbook'),
 path('lebook/<int:pk>', views.LEditView.as_view(), name='lebook'),
 path('lcchat/', views.LCreateChat.as_view(), name='lcchat'),
 path('llchat/', views.LListChat.as_view(), name='llchat'),
 path('lchangepass/',views.librarian_change_pass, name='lchangepass'),




 # student URL's
 path('student/', views.UBookListView.as_view(), name='student'),
 path('ucchat/', views.UCreateChat.as_view(), name='ucchat'),
 path('ulchat/', views.UListChat.as_view(), name='ulchat'),
 path('feedback_form/', views.feedback_form, name='feedback_form'),
 path('send_feedback/', views.send_feedback, name='send_feedback'),
 path('about/', views.about, name='about'),
 path('usearch/', views.usearch, name='usearch'),
 path('changepass/',views.student_change_pass, name='changepass'),



 # Admin URL's
 path('dashboard/', views.dashboard, name='dashboard'),
 path('acchat/', views.ACreateChat.as_view(), name='acchat'),
 path('alchat/', views.AListChat.as_view(), name='alchat'),
 path('aabook_form/', views.aabook_form, name='aabook_form'),
 path('aabook/', views.aabook, name='aabook'),
 path('arabook/', views.ABookListView.as_view(), name='arabook'),
 path('ambook/', views.AManageBook.as_view(), name='ambook'),
 path('adbook/<int:pk>', views.ADeleteBook.as_view(), name='adbook'),
 path('avbook/<int:pk>', views.AViewBook.as_view(), name='avbook'),
 path('aebook/<int:pk>', views.AEditView.as_view(), name='aebook'),
 path('afeedback/', views.AFeedback.as_view(), name='afeedback'),
 path('asearch/', views.asearch, name='asearch'),
 path('adbookk/<int:pk>', views.ADeleteBookk.as_view(), name='adbookk'),
 path('create_user_form/', views.create_user_form, name='create_user_form'),
 path('aluser/', views.ListUserView.as_view(), name='aluser'),
 path('create_use/', views.create_user, name='create_user'),
 path('alvuser/<int:pk>', views.ALViewUser.as_view(), name='alvuser'),
 path('<int:id>/', views.update_data, name='aeuser'),
 path('aduser/<int:pk>', views.ADeleteUser.as_view(), name='aduser'),
 path('achangepass/',views.admin_change_pass, name='achangepass'),




















]
