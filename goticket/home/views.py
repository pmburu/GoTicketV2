from django.shortcuts import render


def homepage(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html", {})


def store(request):
    return render(request, "store.html", {})


def login(request):
    return render(request, "login.html", {})


def signup(request):
    return render(request, "sign_up.html", {})


def profile(request):
    return render(request, "profile.html", {})
