from django.contrib import messages
from django.shortcuts import render


def index(request):
    data: dict = request.GET
    if ''.join(data.get('success', [])) == 'True':
        messages.success(request, 'Account is verify')
    return render(request, 'index.html', {})
