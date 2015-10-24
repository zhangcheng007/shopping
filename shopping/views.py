# -*- coding: utf-8 -*-
from django.shortcuts import  get_object_or_404,render
from django.http import HttpResponse
from django.core.context_processors import csrf
from django import forms
# Create your views here.


from shopping.models import Character,Category,Product,ProductPic,ProductSpec

def staff(request):
    staff_list = Character.objects.all()
    staff_str  = map(str, staff_list)
    #return HttpResponse("<p>" + ' '.join(staff_str) + "</p>")
    #context   = {'label': ' '.join(staff_str)}
    #return render(request, 'testTemp.html', context)
    return render(request, 'testTemp.html', {'staffs': staff_list})

# 获取商品类型和商品
def index(request):


    latest_category_list = Category.objects.all()
    context = {'latest_category_list': latest_category_list}
    return render(request, 'shopping/shoppingIndex.html',context)


    #return HttpResponse("<p>购物</p>")


def detail(request, product_id):
   product = get_object_or_404(Product, pk=product_id)

   return render(request, 'shopping/productContent.html', {'product': product})



def categoryToProduct(request, category_id):
    categorys = get_object_or_404(Category, pk=category_id)
    latest_category_list = Category.objects.all()
    context = {'latest_category_list': latest_category_list,'categorys':categorys}

    return render(request, 'shopping/speciaProduct.html',context)







def testTemp(request):
    context          = {}
    context['label'] = 'Hello zhangcheng!'

    return render(request, 'testTemp.html', context)

def testBase(request):
    staff_list = Character.objects.all()
    return render(request, 'shopping/subbase.html', {'staffs': staff_list})
    #return render(request, 'shopping/base.html')


def form(request):
    return render(request, 'form.html')


class CharacterForm(forms.Form):
      name = forms.CharField(max_length =200)

def investigate(request):
    if request.POST:
            submitted  = request.POST['staff']
            #submitted  =form.cleaned_data['name']
            new_record = Character(name = submitted)
            new_record.save()
    ctx ={}
    ctx.update(csrf(request))
    all_records = Character.objects.all()
    ctx['staff'] = all_records
    return render(request, "form.html", ctx)













