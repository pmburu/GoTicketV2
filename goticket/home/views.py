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

def product(request, event_id):
	return render(request, "product.html", {"event_id": event_id})

def product_empty(request):
	return render(request, "product.html", {})
