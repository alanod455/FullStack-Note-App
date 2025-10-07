from django.views.generic.detail import DetailView
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Note
def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')

def notes_index(request):
    notes = Note.objects.all()
    return render(request, 'notes/index.html', {'notes': notes})



def note_detail(request, note_id):
    note = Note.objects.get(id=note_id)
    return render(request, 'notes/detail.html', {'note': note})


class NoteCreate(CreateView):
    model = Note
    fields = ['title', 'content']
    success_url = '/notes/'
    

class NoteUpdate(UpdateView):
    model = Note
    fields = ['title', 'content']
    template_name = 'main_app/note_form.html'

    def get_success_url(self):
        return reverse('note-detail', kwargs={'pk': self.object.pk})


class NoteDetail(DetailView):
    model = Note
    template_name = 'notes/detail.html'

class NoteDelete(DeleteView):
    model = Note
    success_url = '/notes/'
