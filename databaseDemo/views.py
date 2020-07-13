from pprint import pprint

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Create your views here.
@login_required
def HomeV(request):
    return render(request, 'base.html')

@login_required
def TestV(request, id):
    if request.method == 'POST':
        field1 = request.POST.get('methycaptureinfo')
        print(">>>>> request.POST:")
        pprint(request.POST)
        print(">>>>> field1:")
        print(field1)
    else:
        return render(request, 'Test/test.{}.html'.format(id))
