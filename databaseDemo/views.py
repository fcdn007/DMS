from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Create your views here.
@login_required
def HomeV(request):
    return render(request, 'base.html')

@login_required
def TestV(request, id):
    return render(request, 'Test/test.{}.html'.format(id))
