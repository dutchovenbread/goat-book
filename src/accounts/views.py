from django.core.mail import send_mail
from django.shortcuts import redirect

def send_login_email(request):
  email = request.POST["email"]
  # expected future code:
  send_mail(
    "Your login link for Superlists",
    "Some kind of body",
    "noreply@superlists.com",
    [email],
  )
  return redirect("/")
