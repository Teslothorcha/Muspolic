from django.shortcuts import render

# Create your views here.
def index(request):
    return HttpResponseRedirect(reverse('pages:home_view'))
def error_404(request, exception):
    print("404-404-404-404-404")
    return render(request,'handler/404.html')

def error_500(request):
    print("500-500-500-500-500")
    return render(request,'handler/500.html')