from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.db import connection
from .model import Note, User


def index(request):
    if request.session.get("user_id") is None:
        return HttpResponseRedirect("/login")
    return HttpResponseRedirect("/notes")


def logout(request):
    request.session["user_id"] = None
    request.session["username"] = None
    return HttpResponseRedirect("/login")


def login(request):
    if request.GET.get('username') is not None \
            and request.GET.get('password') is not None:
        user = User.objects.filter(username=request.GET.get('username'), password=request.GET.get('password')).first()
        if user is not None:
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            return HttpResponseRedirect("/notes")
        return HttpResponse('Unauthorized', status=401)
    template = loader.get_template('login.html')
    return HttpResponse(template.render({}, request))


def notes(request):
    if request.session.get("user_id") is None:
        return HttpResponse('Unauthorized', status=401)
    user = User.objects.get(pk=request.session["user_id"])
    if request.GET.get('note_content') is not None and request.GET.get('user_id') is not None:
        new_note = Note(user_id=int(request.GET.get('user_id')), content=request.GET.get('note_content'))
        new_note.save()
        return HttpResponseRedirect("/notes")
    all_notes = get_user_notes(request.session["username"])
    template = loader.get_template('notes.html')
    return HttpResponse(template.render({'notes': all_notes, 'user': user}, request))


def register(request):
    if request.GET.get('username') is not None \
            and request.GET.get('password') is not None:
        u = User(username=request.GET.get('username'), password=request.GET.get('password'))
        u.save()
        u2 = User.objects.filter(username=request.GET.get('username')).first()
        request.session['user_id'] = u2.id
        request.session['username'] = u2.username
        return HttpResponseRedirect("/notes")
    template = loader.get_template('register.html')
    return HttpResponse(template.render({}, request))


def get_user_notes(username):
    with connection.cursor() as cursor:
        query_string = "SELECT * FROM cyber_security_base_project_2021_note n LEFT JOIN cyber_security_base_project_2021_user u ON n.user_id = u.id WHERE u.username = '%s'" % username
        cursor.execute(query_string)
        results = []
        for note in cursor.fetchall():
            results.append({'content': note[1]})
        return results
