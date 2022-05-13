from django.shortcuts import render


def homepage(request):
    return render(request, 'home.html', {'new_item_text': request.POST.get('item_text', '')})
