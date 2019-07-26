from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg, Sum, Count, Case, When, CharField, Value, FloatField, Func
import random
from .forms import *


class Round(Func):
    function = 'ROUND'
    arity = 2


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!  You are now able to login.')
            return redirect('/')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    # if request.method == 'POST':
    #     u_form = UserUpdateForm(request.POST, instance=request.user)
    #     p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
    #     roster_form = ProfileRosterUpdateForm(request.POST, instance=request.user.profile)
    #     if u_form.is_valid() and p_form.is_valid():
    #         u_form.save()
    #         p_form.save()
    #         roster_form.save()
    #         messages.success(request, f'Your account has been updated!')
    #         return redirect('profile')
    # else:
    #     u_form = UserUpdateForm(instance=request.user)
    #     p_form = ProfileUpdateForm(instance=request.user.profile)
    #     roster_form = ProfileRosterUpdateForm(request.POST, instance=request.user.profile)
    #
    # context = {
    #     'u_form': u_form,
    #     'p_form': p_form,
    #     'roster_form': roster_form,
    # }
    return render(request, 'users/profile.html')


def compare_view(request):
    length = [i for i in range(10)]
    search1 = ''
    search1_stats = ''
    search2 = ''
    search2_stats = ''
    prediction = ''
    if request.method == 'POST':
        prediction = str(random.randint(0, 100)) + '%'
        search_name1 = request.POST.get('wrestler1')
        search1 = FS_Wrestler.objects.get(name=search_name1)
        search1_stats = search1.focus_wrestler2.exclude(duration='00:00:00').aggregate(
            match_count=Count('result'),
            result=Round(Avg(Case(
                When(result='WinF', then=Value(1.75)),
                When(result='WinTF', then=Value(1.50)),
                When(result='WinMD', then=Value(1.25)),
                When(result='WinD', then=Value(1.10)),
                When(result='LossD', then=Value(0.90)),
                When(result='LossMD', then=Value(0.75)),
                When(result='LossTF', then=Value(0.50)),
                When(result='LossF', then=Value(0.25)),
                output_field=FloatField())), 2),
            hi_rate=Round(Avg('hi_rate'), 2),
            ho_rate=Round(Avg('ho_rate'), 2),
            d_rate=Round(Avg('d_rate'), 2),
            ls_rate=Round(Avg('ls_rate'), 2),
            gb_rate=Round(Avg('gb_rate'), 2),
            t_rate=Round(Avg('t_rate'), 2),
            npf=Round(Avg('npf'), 2),
            apm=Round(Avg('apm'), 2),
            points=Round(Avg('focus_score'), 2)
        )
        search_name2 = request.POST.get('wrestler2')
        search2 = FS_Wrestler.objects.get(name=search_name2)
        search2_stats = search2.focus_wrestler2.exclude(duration='00:00:00').aggregate(
            match_count=Count('result'),
            result=Round(Avg(Case(
                When(result='WinF', then=Value(1.75)),
                When(result='WinTF', then=Value(1.50)),
                When(result='WinMD', then=Value(1.25)),
                When(result='WinD', then=Value(1.10)),
                When(result='LossD', then=Value(0.90)),
                When(result='LossMD', then=Value(0.75)),
                When(result='LossTF', then=Value(0.50)),
                When(result='LossF', then=Value(0.25)),
                output_field=FloatField())), 2),
            hi_rate=Round(Avg('hi_rate'), 2),
            ho_rate=Round(Avg('ho_rate'), 2),
            d_rate=Round(Avg('d_rate'), 2),
            ls_rate=Round(Avg('ls_rate'), 2),
            gb_rate=Round(Avg('gb_rate'), 2),
            t_rate=Round(Avg('t_rate'), 2),
            npf=Round(Avg('npf'), 2),
            apm=Round(Avg('apm'), 2),
            points=Round(Avg('focus_score'), 2)
        )

    context = {
        "w1": search1,
        "w1_stats": search1_stats,
        "w2": search2,
        "w2_stats": search2_stats,
        'prediction': prediction,
        'length': length,
    }
    return render(request, "users/profile.html", context)
