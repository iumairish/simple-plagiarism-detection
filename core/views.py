from django.contrib.auth.models import User
from django.db import models
from django.http import request
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from authentication.decorators import is_teacher, is_student
from .forms import AssignmentCreateForm, AssignmentSubmitForm, AssignmentUpdateForm
from .models import Assignment, Submissions, User
from plagiarism.check import init_plagiarism
import os, logging
import datetime

 
# DASHBOARD
class HomeView(ListView):
    template_name = 'core/home.html'
    model = Assignment 
    context_object_name = 'assignment'

    @method_decorator(login_required(login_url=reverse_lazy('authentication:login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        myobj = self.model.objects.all().order_by('-id')
        current_datetime = datetime.date.today()
        for obj in myobj:
            obj.due_date = obj.due_date.date()
            obj.expired = (current_datetime > obj.due_date)
        return myobj


# ASSIGNMENT CREATE VIEW
class AssignmentCreateView(CreateView):
    template_name = 'core/assignment/create.html'
    form_class = AssignmentCreateForm
    extra_context = {
        'title': 'Create New Assignment'
    }
    success_url = reverse_lazy('core:home')

    @method_decorator(login_required(login_url=reverse_lazy('authentication:login')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('authentication:login')
        if self.request.user.is_authenticated and self.request.user.role != 'teacher':
            return reverse_lazy('authentication:login')
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AssignmentCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


# ASSIGNMENT DETAIL VIEW 
class AssignmentDetailView(ListView):
    model = Assignment
    template_name = 'core/assignment/view.html'
    context_object_name = 'assignment'

    @method_decorator(login_required(login_url=reverse_lazy('authentication:login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        if self.request.user.role == 'teacher':
            return self.model.objects.filter(user_id=self.request.user.id).order_by('-id')
        else:
            return self.model.objects.filter(id=self.kwargs['pk']).order_by('-id')


# ASSIGNMENT UPDATE VIEW
class AssignmentUpdateView(UpdateView):
    template_name = 'core/assignment/create.html'
    form_class = AssignmentUpdateForm
    model = Assignment
    success_url = reverse_lazy('core:home')
    extra_context = {
        'title': 'Update Assignment'
    }

    @method_decorator(login_required(login_url=reverse_lazy('authentication:login')))
    def dispatch(self, request, *args, **kwargs):
        if request.user.role == 'teacher':
            return super().dispatch(self.request, *args, **kwargs)
        return HttpResponseRedirect(reverse_lazy('core:home')) 


# ASSIGNMENT SUBMIT VIEW
class AssignmentSubmitView(CreateView):
    template_name = 'core/assignment/submit.html'
    form_class = AssignmentSubmitForm
    extra_context = {
        'title': 'Submit Assignment'
    }
    success_url = reverse_lazy('core:home')

    @method_decorator(login_required(login_url=reverse_lazy('authentication:login')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('authentication:login')
        if self.request.user.is_authenticated and self.request.user.role != 'student':
            return reverse_lazy('authentication:login')
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):    
        form.instance.user = self.request.user
        return super(AssignmentSubmitView, self).form_valid(form)
    
    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)      
        else:
            return self.form_invalid(form)


# SUBMISSIONS VIEW
class AssignmentSubmissionsView(ListView):
    model = Submissions
    template_name = 'core/assignment/submissions.html'
    context_object_name = 'submissions'

    @method_decorator(login_required(login_url=reverse_lazy('authentication:login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.all()


# SUBMISSION DETAIL VIEW 
class AssignmentSubmissionDetailView(TemplateView):
    model = Submissions
    template_name = 'core/teacher/assignment/view.html'
    context_object_name = 'assignment'

    @method_decorator(login_required(login_url=reverse_lazy('authentication:login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(user_id=self.request.user.id).order_by('-id')


# ASSIGNMENT SUBMIT RESULT VIEW
class AssignmentSubmitResultView(UpdateView):
    template_name = 'core/assignment/submit.html'
    model = Submissions
    fields = ['marks', 'comments']
    success_url = reverse_lazy('core:home')

    @method_decorator(login_required(login_url=reverse_lazy('authentication:login')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('authentication:login')
        if self.request.user.is_authenticated and self.request.user.role != 'teacher':
            return reverse_lazy('authentication:login')
        return super().dispatch(self.request, *args, **kwargs)


# ASSIGNMENT SUBMIT RESULT VIEW
@is_teacher
def AssignmentDeclareResult(request, id):

    assigment = Assignment.objects.get(id=id)
    assigment.result = True
    assigment.save()

    return HttpResponseRedirect(reverse_lazy('core:home'))


# ASSIGNMENT RESULT DETAIL VIEW
class AssignmentResultView(ListView):
    model = Submissions
    template_name = "core/assignment/result.html"
    context_object_name = 'result'

    @method_decorator(login_required(login_url=reverse_lazy('authentication:login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(user_id=self.request.user.id).order_by('-id')


def PlagcheckView(request, pk, *args, **kwargs):

    instance = Submissions.objects.filter(id=pk).values('user','assignment','file')
    instance2 = Assignment.objects.filter(id=instance[0]['assignment']).values('exclude_urls')
    user = User.objects.get(id=instance[0]['user'])

    name = user.first_name
    
    f = 'uploads/'+instance[0]['file']
    ex = instance2[0]['exclude_urls']
    
    filename = f"Result_{name}.txt"
    fileData = 'Links:\n\n'
    
    result = init_plagiarism(f, ex)

    for key in result:
        if 'href' in key:
            lines=result['href']
            for i in lines: 
                fileData += i+'\n'
        elif 'score' in key:
            score = result[key][0]
            scoreTxt = '{:.3f}%'.format(float(score))
            fileData += '\nScore: '+scoreTxt+'\n'

    report_path = os.path.join('uploads/reports', filename)


    if score:
        instance.update(score=score, report='reports/%s'%filename)

    file = open(report_path, "w+")
    file.write( fileData )
    file.close()
    
    # return HttpResponse(result, content_type='text/plain,charset=utf8')
    # response['Content-Disposition'] = 'attachment;filename=%s'%filename
    
    return redirect('core:assignment-submissions', id=pk)
