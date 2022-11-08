from django.urls import path
from .views import *


app_name = "authentication"

urlpatterns = [
    path('student/register', StudentRegisterView.as_view(), name='student-register'),
    path('teacher/register', TeacherRegisterView.as_view(), name='teacher-register'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
]
