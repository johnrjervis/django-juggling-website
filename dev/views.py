from django.shortcuts import render

# Create your views here.

def programming(request):
    return render(request, 'dev/programming.html', {'selected': 'Programming'})

def web_development(request):
    return render(request, 'dev/web_development.html', {'selected': 'Web development'})
