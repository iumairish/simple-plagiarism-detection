from django.http.response import HttpResponseRedirect
from django.views.generic import TemplateView
from django.shortcuts import render
 
 
class HomeView(TemplateView):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect( '/dashboard' )
        return render(request, self.template_name)
        