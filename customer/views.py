# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.context_processors import csrf
#from django.contrib.auth import *

from django import forms




# Create your views here.
def customer_login(request):
    #return HttpResponse("<p>客户登陆</p>")
    return render(request, 'customer/login.html')

def check_login(request):
    ctx = {}
    ctx.update(csrf(request))
    if request.POST:
        username = password = ''
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username is not None :
                ctx['success'] = "成功"
                return render(request, 'customer/login.html',ctx)


    return HttpResponse("<p>登陆失败</p>")












