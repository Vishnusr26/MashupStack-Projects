from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .models import WeightModel
from .forms import SignUpForm, WeightForm
#from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.utils import timezone


def signUp(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})
     

def logIn(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required(login_url='/log-in/')
def logOut(request):
    logout(request)
    return redirect('home')

def home1(request):
    return render(request, 'home.html')

@login_required(login_url='/log-in/')
def add_weight(request):
    if request.method == 'POST':
        form = WeightForm(request.POST)
        if form.is_valid():
            weight_entry = form.save(commit=False)
            weight_entry.user = request.user
            
            today = timezone.now().date()
            if WeightModel.objects.filter(user=request.user, date_added=today).exists():
                return render(request, 'add_weight.html', {
                    'form': form, 
                    'error': 'You have already added a weight today.'
                    })
            weight_entry.save()
            return redirect('weightlist')
    else:
        form = WeightForm()
    return render(request, 'add_weight.html', {'form': form})

@login_required(login_url='/log-in/')
def weight_list(request):
    weights = WeightModel.objects.filter(user=request.user).order_by('-date_added')
    paginator = Paginator(weights, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'weight_list.html', {'page_obj': page_obj})

@login_required(login_url='/log-in/')
def edit_weight(request, pk):
    weight_entry = get_object_or_404(WeightModel, pk=pk, user=request.user)
    if request.method == 'POST':
        form = WeightForm(request.POST, instance=weight_entry)
        if form.is_valid():
            form.save()
            return redirect('weightlist')
    else:
        form = WeightForm(instance=weight_entry)
    return render(request, 'add_weight.html', {'form': form})

@login_required(login_url='/log-in/')
def delete_weight(request, pk):
    weight_entry = get_object_or_404(WeightModel, pk=pk, user=request.user)
    if request.method == 'POST':
        weight_entry.delete()
        return redirect('weightlist')
    return render(request, 'delete_weight.html', {'weight_entry': weight_entry})

@login_required(login_url='/log-in/')
def weight_loss(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        weights = WeightModel.objects.filter(user=request.user, date_added__range=[start_date, end_date]).order_by('-date_added')
        if weights.exists():
            initial_weight = weights.first().weight
            final_weight = weights.last().weight
            weight_loss = initial_weight - final_weight
            return JsonResponse({'weight_loss': weight_loss})
    return JsonResponse({'error': 'Invalid date range'})