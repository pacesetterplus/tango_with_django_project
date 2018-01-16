from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    # Construct a dictionary to pass to the template engine as its context.
    # The key boldmessage is the declared in the template.
    context_dict = {'boldmessage':"Crunchy, creamy, cookie, candy, cupcake!"}

    #return a rendered response to send to the client
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    return render(request, 'rango/about.html')