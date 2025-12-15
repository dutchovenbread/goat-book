from django.http import HttpResponse
from django.shortcuts import render
from lists.models import Item

# Create your views here.
def home_page(request):
  if request.method == 'POST':
    item = Item()
    item.text = request.POST['item_text']
    item.save()

  return render (request,
    'home.html',
    {"new_item_text": request.POST.get('item_text','')}
  )