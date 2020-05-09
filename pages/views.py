from django.shortcuts import render

# home page

def home_view(request):
    """
    sets home view for muspolic
    """
    return render(request, 'pages/index.html')

