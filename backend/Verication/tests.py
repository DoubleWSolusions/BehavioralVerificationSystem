from django.http import HttpResponse


def edit_lists(request):
    data = request.POST.getlist('myArray[]')
    return HttpResponse('Success')
