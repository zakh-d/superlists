from django.shortcuts import render, redirect
from django.urls import reverse
from lists.models import Item


def homepage(request):

    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/lists/the-only-list-in-the-world/')
    return render(request, 'home.html')


def  view_list(request):
    
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})
