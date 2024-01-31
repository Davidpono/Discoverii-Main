from django.shortcuts import render

# Create your views here.
def cell_view (request):
    return render(request,"cellhome.html")

def conf (request):
    return render(request,"conference.html")

def ldemo (request):
    return render(request,"demo.html")
def mpaper (request):
    return render(request,"mainpaper.html")
def lpre (request):
    return render(request,"livepresentation.html")