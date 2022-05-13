from django.shortcuts import render, redirect
from django.urls import reverse
from lists.models import Item


def homepage(request):

    if request.method == 'POST':
        new_item_text = request.POST['item_text']
        Item.objects.create(text=new_item_text)
        return redirect(reverse('homepage'))
    
    items = Item.objects.all()
    return render(request, 'home.html', {'items': items})
