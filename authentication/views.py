from django.contrib import messages, auth
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import CreateView, FormView, RedirectView

from .forms import *
from .models import User


# REGISTER STUDENT VIEW
class StudentRegisterView(CreateView):
    model = User
    form_class = StudentRegistrationForm
    template_name = 'authentication/register.html'
    success_url = '/'

    extra_context = {
        'title': 'Student Registeration'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.success_url)
        return super().dispatch(self.request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            return redirect('authentication:login')
        else:
            return render(request, 'authentication/register.html', {'form': form})


# REGISTER TEACHER VIEW
class TeacherRegisterView(CreateView):
    model = User
    form_class = TeacherRegistrationForm
    template_name = 'authentication/register.html'
    success_url = '/'

    extra_context = {
        'title': 'Teacher Registeration'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.success_url)
        return super().dispatch(self.request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            return redirect('authentication:login')
        else:
            return render(request, 'authentication/register.html', {'form': form})


# LOGIN VIEW
class LoginView(FormView):
    success_url = '/dashboard'
    form_class = UserLoginForm
    template_name = 'authentication/login.html'

    extra_context = {
        'title': 'Login'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def get_success_url(self):
        if 'next' in self.request.GET and self.request.GET['next'] != '':
            return self.request.GET['next']
        else:
            return self.success_url

    def get_form_class(self):
        return self.form_class

    def form_valid(self, form):
        auth.login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))


# LOGOUT VIEW
class LogoutView(RedirectView):
    url = '/'

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return super(LogoutView, self).get(request, *args, **kwargs)
