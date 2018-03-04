# -*- coding: utf-8   -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from .models import User, Quote
from django.contrib import messages
from time import gmtime, strptime
def index(request):
    return render(request, "index.html")

def register(request):
    response = User.objects.register(
        request.POST["fname"],
        request.POST["lname"],
        request.POST["email"],
        request.POST["password"],
        request.POST["conpassword"],
        request.POST["dob"],
    )
    if response["valid"]:
        request.session["user_id"] = response["user"].id
        return redirect("/valhalla")
    else:
        for error in response["errors"]:
            messages.add_message(request, messages.ERROR, error)
    return redirect("/")

def login(request):
    response = User.objects.login(
        email = request.POST["email"],
        password = request.POST["password"],
    )
    if response["valid"]:
        request.session["user_id"] = response["user"].id
        return redirect("/valhalla")
    else:
        for error in response["errors"]:
            messages.add_message(request, messages.ERROR, error)
    return redirect("/")

def logout(request):
    request.session.clear()
    return redirect("/")

def valhalla(request):
    if "user_id" not in request.session:
        return redirect("/")
    data = {
        'quotes': Quote.objects.all(),
        'yourquotes': Quote.objects.filter(creator=request.session["user_id"]),
        'user': User.objects.get(id=request.session['user_id']),
        'othersquotes': Quote.objects.all().filter(quoters=request.session["user_id"]),
        'unclaimed': Quote.objects.all().exclude(quoters=request.session["user_id"]),
    }
    return render(request, "valhalla.html", data)
def add(request):
    if "user_id" not in request.session:
        return redirect("/")
    return render(request, "create.html")
def join(request, id):
    if "user_id" not in request.session:
        return redirect("/")
    response = Quote.objects.join(
        itemid = request.POST['hidden'],
        quoter = request.session["user_id"]
    )
    return redirect('/valhalla')

def create(request):
    if "user_id" not in request.session:
        return redirect("/")
    response = Quote.objects.createquote(
        request.POST['quote'],
        request.POST['message'],
        User.objects.get(id=request.session['user_id'])
    )
    if response['valid']:
        return redirect("/valhalla")
    else:
        for error in response["errors"]:
            messages.add_message(request, messages.ERROR, error)
            return redirect("/valhalla/create")
def item(request, id):
    if "user_id" not in request.session:
        return redirect("/")
    creator = [1]
    data = {
        'quote':Quote.objects.all().filter(creator=id),
        'total':len(Quote.objects.all().filter(creator=id)),
    }
    return render(request, "items.html", data)
def delete(request):
    if "user_id" not in request.session:
        return redirect("/")
    itemid = request.POST['hidden']
    Quote.objects.filter(id=itemid).delete()
    return redirect('/valhalla')
def unwant(request, id):
    if "user_id" not in request.session:
        return redirect("/")
    response = Quote.objects.unwant(
        request.POST['hidden'],
        request.session['user_id']
    )
    return redirect("/valhalla")
