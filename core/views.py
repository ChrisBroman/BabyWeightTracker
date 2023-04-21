from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import logout
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

import pandas as pd
import openpyxl
import scipy.stats as stats
from datetime import datetime
from dateutil.relativedelta import relativedelta
from decimal import Decimal
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import urllib
import base64

from .forms import SignupForm, NewBabyForm, NewRecordForm, EditRecordForm, EditBabyForm
from .models import Baby, Record

def create_weight_graph(x, y):
    plt.figure()
    plt.plot(x, y, marker='*')
    plt.title('Date vs. Weight')
    plt.xticks(x, rotation='vertical')
    plt.xlabel('Dates')
    plt.ylabel('Weight (kg)')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    return image_base64

def create_percentile_graph(x, y):
    plt.figure()
    plt.plot(x, y, marker='*')
    plt.title('Date vs. Percentile')
    plt.xticks(x, rotation='vertical')
    plt.xlabel('Dates')
    plt.ylabel('Percentile')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    return image_base64

def months_difference(date1, date2):
    difference = relativedelta(date2, date1)
    months = difference.years * 12 + difference.months
    return months

def get_percentile(weight, month):
    df = pd.read_excel('core/percentiles.xlsx')
    df['L'] = df['L'].astype(float)
    df['M'] = df['M'].astype(float)
    df['S'] = df['S'].astype(float)
    L = Decimal(df.loc[month, 'L'])
    M = Decimal(df.loc[month, 'M'])
    S = Decimal(df.loc[month, 'S'])
    z_score = ((weight / M) ** L - 1) / (L * S)
    percentile = stats.norm.cdf(float(z_score)) * 100
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
        if user.is_authenticated:
            babies = Baby.objects.filter(parent=user)
            context = {
                'babies': babies,
            }
        else:
            context = {}
        return render(request, 'core/index.html', context)
    
class BabyDetails(View, LoginRequiredMixin):
    def get(self, request, baby_pk):
        user = request.user
        baby = Baby.objects.get(parent=user, pk=baby_pk)
        context = {
            'user': user,
            'baby': baby,
        }
        return render(request, 'core/baby_details.html', context)
    
class NewBaby(View, LoginRequiredMixin):
    def get(self, request):
        form = NewBabyForm()
        context = {
            'form': form,
        }
        return render(request, 'core/new_baby.html', context)
    
    def post(self, request):
        user = request.user
        form = NewBabyForm(request.POST)
        if not form.is_valid():
            context = {
                'form': form,
            }
            return render(request, 'core/new_baby.html', context)
        new_baby = form.save(commit=False)
        new_baby.parent = user
        new_baby.save()
        return redirect('core:index')
    
class EditBaby(View, LoginRequiredMixin):
    def get(self, request, baby_pk):
        user = request.user
        baby = Baby.objects.get(parent=user, pk=baby_pk)
        form = EditBabyForm()
        context = {
            'baby': baby,
            'form': form,
        }
        return render(request, 'core/edit_baby.html', context)
    
    def post(self, request, baby_pk):
        user = request.user
        baby = Baby.objects.get(parent=user, pk=baby_pk)
        form = EditBabyForm(request.POST, instance=baby)
        if not form.is_valid():
            context = {'form': form}
            return render(request, 'core/edit_baby.html', context)
        form.save()
        return render('core:baby_details', baby_pk=baby_pk)
    
def delete_baby(request, baby_pk):
    baby = Baby.objects.get(pk=baby_pk)
    baby.delete()
    return redirect('core:index')

class NewRecord(View, LoginRequiredMixin):
    def get(self, request, baby_pk):
        form = NewRecordForm()
        context = {'form': form}
        return render(request, 'core/new_record.html', context)
    
    def post(self, request, baby_pk):
        user = request.user
        baby = Baby.objects.get(parent=user, pk=baby_pk)
        form = NewRecordForm(request.POST)
        if not form.is_valid():
            context = {'form': form}
            return render(request, 'core_new_record.html', context)
        new_record = form.save(commit=False)
        new_record.baby = baby
        
        baby_birthdate = baby.birth_date
        record_date = form.cleaned_data['date']
        baby.age_in_months = months_difference(baby_birthdate, record_date)
        baby.current_weight = form.cleaned_data['weight']
        
        record_weight = form.cleaned_data['weight']
        new_record.percentile = get_percentile(record_weight, baby.age_in_months)
        baby.current_percentile = new_record.percentile
        baby.save()
        new_record.save()
        return redirect('core:baby_details', baby_pk=baby_pk)
    
class ViewRecords(View, LoginRequiredMixin):
    def get(self, request, baby_pk):
        user = request.user
        baby = Baby.objects.get(parent=user, pk=baby_pk)
        records = Record.objects.filter(baby=baby)
        x_weight_list = []
        y_weight_list = []
        for record in records:
            x_weight_list.append(record.date)
            y_weight_list.append(record.weight)
        weight_graph_image = create_weight_graph(x_weight_list, y_weight_list)
        x_percentile_list = []
        y_percentile_list = []
        for record in records:
            x_percentile_list.append(record.date)
            y_percentile_list.append(record.percentile)
        percentile_graph_image = create_percentile_graph(x_percentile_list, y_percentile_list)    
        context = {
            'baby': baby,
            'records': records,
            'weight_graph': weight_graph_image,
            'percentile_graph': percentile_graph_image,
        }
        return render(request, 'core/records.html', context)
    
class ViewRecord(View, LoginRequiredMixin):
    def get(self, request, baby_pk, record_pk):
        user = request.user
        baby = Baby.objects.get(parent=user, pk=baby_pk)
        record = Record.objects.get(baby=baby, pk=record_pk)
        context = {
            'baby': baby,
            'record': record,
        }
        return render(request, 'core/view_record.html', context)
    
@login_required
def delete_record(request, baby_pk, record_pk):
    user = request.user
    baby = Baby.objects.get(parent=user, pk=baby_pk)
    record = Record.objects.get(baby=baby, pk = record_pk)
    record.delete()
    return redirect('core:records', baby_pk=baby_pk)

class EditRecord(View, LoginRequiredMixin):
    def get(self, request, baby_pk, record_pk):
        user = request.user
        baby = Baby.objects.get(parent=user, pk=baby_pk)
        record = Record.objects.get(baby=baby, pk=record_pk)
        form = EditRecordForm()
        context = {
            'form': form,
            'record': record,
            }
        return render(request, 'core/edit_record.html', context)
    
    def post(self, request, baby_pk, record_pk):
        user = request.user
        baby = Baby.objects.get(parent=user)
        record = Record.objects.get(baby=baby, pk=record_pk)
        form = EditRecordForm(request.POST, instance=record)
        if not form.is_valid():
            context = {'form': form}
            return render(request, 'core/edit_record.html', context)
        edited_record = form.save(commit=False)
        baby_birthdate = baby.birth_date
        record_date = form.cleaned_data['date']
        record_weight = form.cleaned_data['weight']
        age_in_months = months_difference(baby_birthdate, record_date)
        edited_record.percentile = get_percentile(record_weight, age_in_months)
        edited_record.save()
        return redirect('core:record', baby_pk=baby_pk, record_pk=record_pk)
        
        
        