from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .model import Note, User


def index(request):
    if request.session.get("user_id") is None:
        return HttpResponseRedirect("/login")
    return HttpResponseRedirect("/notes")


def logout(request):
    request.session["user_id"] = None
    return HttpResponseRedirect("/login")


def login(request):
    if request.GET.get('username') is not None \
            and request.GET.get('password') is not None:
        user = User.objects.filter(username=request.GET.get('username')).first()
        if user is not None and user.password == request.GET.get('password'):
            request.session['user_id'] = user.id
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
    all_notes = Note.objects.filter(user_id=request.session.get("user_id")).all()
    template = loader.get_template('notes.html')
    return HttpResponse(template.render({'notes': all_notes, 'user': user}, request))
