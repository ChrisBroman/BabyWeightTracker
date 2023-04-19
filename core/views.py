from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import logout
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

import pandas as pd
import openpyxl
import scipy.stats as stats
from datetime import datetime

from .forms import SignupForm
from .models import Baby, Record


def get_percentile(weight, month):
    df = pd.read_excel('../percentile.xlsx')
    L = df.iloc[month]['L']
    M = df.iloc[month]['M']
    S = df.iloc[month]['S']
    z_score = ((weight / M) ** L - 1) / (L * S)
    percentile = stats.norm.cdf(z_score) * 100
    return percentile

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
        user = request.user
        baby = Baby.objects.get(parent=user)
        records = Record.objects.filter(baby=baby)
        context = {
            'user': user,
            'baby': baby,
            'records': records,
        }
        return render(request, 'core/index.html', context)