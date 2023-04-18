from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import logout
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import SignupForm

import datetime

class Signup(View):
    def get(self, request):
        form = SignupForm()
        context = {'form': form}
        return render(request, 'core/signup.html', context)
    
    def post(self, request):
        form = SignupForm(request.POST)
        if not form.is_valid():
            context = {'form': form}
            return render(request, 'core/signup.html', context)
        form.save()
        return redirect('core:index')
    
def logout_view(request):
    logout(request)
    return redirect('core:index')

class Index(View):
    def get(self, request):
        context = {}
        return render(request, 'core/index.html', context)