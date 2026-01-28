from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

from accounts.models import User
from lists.forms import ExistingListItemForm, ItemForm
from lists.models import Item, List

# Create your views here.
def home_page(request):
  return render (
    request,
    'home.html',
    {'form': ItemForm()}
  )
def view_list(request, list_id):
  our_list = List.objects.get(id=list_id)
  form = ExistingListItemForm(for_list=our_list)

  if request.method == 'POST':
    form = ExistingListItemForm(for_list=our_list, data=request.POST)
    if form.is_valid():
      form.save()
      return redirect(our_list)
  return render (
    request,
    'list.html',
    {"list": our_list, 'form': form}
  )

def new_list(request):
  form = ItemForm(data=request.POST)
  if form.is_valid():
    nulist = List.objects.create()
    if request.user.is_authenticated:
      nulist.owner = request.user
      nulist.save()
    form.save(for_list=nulist)
    return redirect(nulist)
  else:
    return render(request, "home.html", {"form": form})

def my_lists(request, email):
  owner = User.objects.get(email=email)
  shared_lists = List.objects.filter(shared_with=owner)
  return render(request, "my_lists.html", {"owner": owner, "shared_lists": shared_lists})

def share_list(request, list_id):
  our_list = List.objects.get(id=list_id)
  email = request.POST['sharee']
  user = User.objects.get(email=email)
  our_list.shared_with.add(user)
  return redirect(f'/lists/{list_id}/')
