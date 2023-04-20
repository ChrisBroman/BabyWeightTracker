from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .forms import LoginForm

app_name = 'core'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html', authentication_form=LoginForm), name='login'),
    path('signup/', views.Signup.as_view(), name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('new_baby/', views.NewBaby.as_view(), name='new_baby'),
    path('<int:baby_pk>/delete_baby/', views.delete_baby, name='delete_baby'),
    path('<int:baby_pk>/', views.BabyDetails.as_view(), name='baby_details'),
    path('<int:baby_pk>/new_record/', views.NewRecord.as_view(), name='new_record'),
    path('<int:baby_pk>/records/', views.ViewRecords.as_view(), name='records'),
    path('<int:baby_pk>/records/<int:record_pk>/', views.ViewRecord.as_view(), name='record'),
    path('<int:baby_pk>/records/<int:record_pk>/delete_record/', views.delete_record, name='delete_record'),
]
