from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from models import Pages
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.template import Context


# Create your views here.
def is_logged(user):
    if user.is_authenticated():
        log = "<p>Logged in as " + user.username
        log += ". <a href='logout/'>Logout</a></p>"
        authenticated = True
    else:
        log = "<p>Not logged in. <a href='/login/'>Login</a></p>"
        authenticated = False
    return (log, authenticated)


def main_page(request):
    (log, authenticated) = is_logged(request.user)
    response = '<h1>Ejercicio 15.8: Django-cms_users_put</h1>'
    response += log
    pages_list = Pages.objects.all()
    if len(pages_list) != 0:
        response += '</br></br><p>Saved pages:</p>'
        response += '<ul>'
        for page in pages_list:
            response += '<p>' + str(page) + '</p>'
        response += '</ul>'
    return HttpResponse(response)


@csrf_exempt
def page_searching(request, resource):
    (log, authenticated) = is_logged(request.user)
    response = log
    if request.method == 'GET':
        try:
            pageSearched = Pages.objects.get(name=resource)
            response += pageSearched.page
            return HttpResponse(response)
        except Pages.DoesNotExist:
            response += '<h1>' + resource + ' not found.</h1>'
            return HttpResponseNotFound(response)

    elif request.method == 'PUT':
        if authenticated:
            try:
                page = request.body
                newPage = Pages(name=resource, page=page)
                newPage.save()
                response += '<h1>Page added successfully.</h1>'
                return HttpResponse(response)
            except:
                response += '<h1>Page not added '+ resource+'</h1>'
                return HttpResponseNotFound(response)
        else:
            response += "<h3>Necesitas registrate para crear paginas</h3>"
            return HttpResponse(response)
    else:
        response += '<h1>Invalid method.</h1>'
        return HttpResponse(response)


def annotated(request, resource):
    (log, authenticated) = is_logged(request.user)
    template = get_template('mytemplate.html')
    if request.method == 'GET':
        try:
            pageSearched = Pages.objects.get(name=resource)
            return HttpResponse(template.render(Context({'login': log, 'page': pageSearched.page})))
        except Pages.DoesNotExist:
            response = '<h1>' + resource + ' not found.</h1>'
            return HttpResponse(template.render(Context({'login': log, 'error': response})))
    else:
        return HttpResponse('<h1>Invalid method.</h1>')
