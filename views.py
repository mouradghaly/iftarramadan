from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django import forms
from django.db import models
from django.urls import reverse
class reg(forms.Form):
    name = forms.CharField(label="Veuillez entrer votre prénom", widget=forms.TextInput(attrs={"class": "name"}))
    lastname = forms.CharField(label='Veuillez entrer votre nom', widget=forms.TextInput(attrs={"class": "lastname"}))
    email = forms.EmailField(label='Veuillez entrer votre addresse mail', widget=forms.EmailInput(attrs={"class": "email"}))
    classchoice = [
    ('3ème', '3ème',),
    ('2nde', '2nde',),
    ('1ère', '1ère',),
    ('Terminale', 'Terminale',),
    ('Professeur', 'Professeur')
]
    classe = forms.ChoiceField(choices= classchoice,widget=forms.Select(attrs={"class": "classe"}))
form = reg
class Person(models.Model):
    name = models.CharField(max_length=60)
    lastname = models.CharField(max_length=60)
    email = models.EmailField(max_length=60)
    classe = models.CharField(max_length=60)

# Create your views here.
def registration(request):
    if request.method == "POST":
        form = reg(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            lastname = form.cleaned_data['lastname']
            email = form.cleaned_data['email']
            classe = form.cleaned_data['classe']
            p = Person(name=name, lastname=lastname, email=email, classe=classe)
            p.save()
            return HttpResponse("OK")
    else:
        return render(request,"/Users/mouradghaly/python-stuff/iftarapp/registration/templates/registration.html", {
            "form": reg
        })

class superuserform(forms.Form):
    name =  forms.CharField(label="User : ")
    password = forms.CharField(label="Password : ", widget=forms.PasswordInput())
name = ""
password = ""
request_start_time_authn = None
def superuser(request):
    if request.method == "POST":
        form = superuserform(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            password = form.cleaned_data["password"]
            if (name == "Mourad" and password == "test") or (name == "Noria" and password == "test"):
                # Set session variable to indicate superuser status
                request.session['is_superuser'] = True
                return HttpResponseRedirect("/registration/admin")  # Redirect to admin page upon successful authentication
            else:
                  return HttpResponseRedirect("/registration/access_denied")

    else:
        form = superuserform()
    
    return render(request, "superuser.html", {"authn": form})

def admin(request):
    my_model = Person.objects.all()
    if request.session.get('is_superuser'):
        # Render admin page
        return render(request, "admin.html", {"my_model": my_model})
    else:
        return HttpResponseRedirect("/registration/authn")
    
def access_denied(request):
    return render(request, "403.html")


