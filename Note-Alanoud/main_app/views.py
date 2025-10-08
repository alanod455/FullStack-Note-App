
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from .models import EmojiReact, Note, Task
from .forms import TaskForm, EmojiForm


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def notes_index(request):
    notes = Note.objects.all()
    return render(request, 'notes/index.html', {'notes': notes})


def note_detail(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    emojis = note.emojis.all()
    tasks = note.tasks.all()
    task_form = TaskForm()

    if request.method == 'POST':

        for task in note.tasks.all():
            task.completed = f'task_{task.id}' in request.POST
            task.save()

        task_form = TaskForm(request.POST)

        if task_form.is_valid() and task_form.cleaned_data['title']:
            new_task = task_form.save(commit=False)
            new_task.note = note
            new_task.save()

        if 'emoji_id' in request.POST:
            emoji_id = request.POST.get('emoji_id')
            emoji = EmojiReact.objects.get(id=emoji_id)
            note.emojis.add(emoji)

        return redirect('note-detail', note_id=note.id)

    return render(request, 'notes/detail.html', {
        'note': note,
        'tasks': tasks,
        'task_form': task_form,
        'emojis': EmojiReact.objects.all(),
        'note_emojis': emojis
    })


def add_emoji(request):
    if request.method == 'POST':
        form = EmojiForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('emoji-index')
    else:
        form = EmojiForm()
    return render(request, 'notes/add_emoji.html', {'form': form})


class NoteCreate(CreateView):
    model = Note
    fields = ['title', 'content']
    success_url = '/notes/'


class NoteUpdate(UpdateView):
    model = Note
    fields = ['title', 'content']
    template_name = 'main_app/note_form.html'

    def get_success_url(self):
        return reverse('note-detail', kwargs={'note_id': self.object.pk})


class NoteDelete(DeleteView):
    model = Note
    success_url = '/notes/'


class EmojiCreate(CreateView):
    model = EmojiReact
    fields = '__all__'


class EmojiList(ListView):
    model = EmojiReact


class EmojiDetail(DetailView):
    model = EmojiReact


class EmojiUpdate(UpdateView):
    model = EmojiReact
    fields = ['emoji'] 
    template_name = 'main_app/emojireact_form.html'
    success_url = reverse_lazy('emoji-index') 


class EmojiDelete(DeleteView):
    model = EmojiReact
    success_url = reverse_lazy('emoji-index')
    template_name = 'main_app/emojireact_confirm_delete.html'\



def associate_emoji(request, note_id, emoji_id):
    if request.method == 'POST':
        note = get_object_or_404(Note, id=note_id)
        note.emojis.add(emoji_id)
    return redirect('note-detail', note_id=note_id)

def remove_emoji(request, note_id, emoji_id):
    note = get_object_or_404(Note, id=note_id)
    emoji = get_object_or_404(EmojiReact, id=emoji_id)
    note.emojis.remove(emoji)
    return redirect('note-detail', note_id=note.id)