from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg, Sum, Count, Case, When, CharField, Value, FloatField, Func
import random
from .forms import UserRegistrationForm, RosterUpdateForm, ProfileUpdateForm, UserUpdateForm
import numpy as np
import pandas as pd 
import os
from .modeling import focus_only_stats, deploy_model
from django.forms import formset_factory

import dash
import dash_core_components as dcc 
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import dash_daq as daq
from django_plotly_dash import DjangoDash

from django.contrib.auth.models import User
from vws_main.models import FS_Wrestler

import dash101 

class Round(Func):
    function = 'ROUND'
    arity = 2


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account created for ' + username + '.  You are now able to login.')
            return redirect('/')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST or None, instance=request.user)
        p_form = ProfileUpdateForm(request.POST or None, request.FILES, instance=request.user.profile)
        roster_form = RosterUpdateForm(request.POST or None, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            roster_form.save()
            messages.success(request, r'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        roster_form = RosterUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'roster_form': roster_form,
    }
    return render(request, 'users/profile.html', context)


@login_required
def profile_update(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST or None, instance=request.user)
        p_form = ProfileUpdateForm(request.POST or None, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, r'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'users/profile-update.html', context)


@login_required
def roster_update(request):
    if request.method == 'POST':
        roster_form = RosterUpdateForm(request.POST or None, instance=request.user.profile)
        if roster_form.is_valid():
            roster_form.save()
            messages.success(request, r'Your team has been updated!')
            return redirect('profile')
    else:
        roster_form = RosterUpdateForm(instance=request.user.profile)
    
    return render(request, 'users/roster-update.html', {'roster_form': roster_form})


@login_required
def athlete_comparison(request):
    if request.method == 'POST':
        search_name1 = request.POST.get('wrestler1')
        search_name2 = request.POST.get('wrestler2')
        cwd = os.getcwd()
        df = pd.read_csv(cwd + '/collection/stats/matchdata.csv', engine='python')
        w1_df = df[df['Focus']==search_name1]
        w2_df = df[df['Focus']==search_name2]
        w1_less = focus_only_stats(w1_df)
        w2_less = focus_only_stats(w2_df)
        w1_ewm = w1_less.ewm(alpha=0.5).mean().iloc[[-1]].values
        w2_ewm = w2_less.ewm(alpha=0.5).mean().iloc[[-1]].values
        loaded_model = deploy_model()
        model = loaded_model[0]
        support = loaded_model[1]
        subbed = np.subtract(w1_ewm, w2_ewm)
        pred = model.predict(subbed[:,support])

    else:
        messages.warning(request, r'Invalid form request, please try again.')
        return redirect('profile')

    context = {
        "w1_df": w1_df,
        "w2_df": w2_df,
        'prediction': pred,
    }
    return render(request, "users/athlete-comparison.html", context)
    

def dashboard(request):
    return render(request, template_name="users/dashboard.html")
