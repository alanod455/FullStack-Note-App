
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from .models import EmojiReact, Note, Task
from .forms import TaskForm, EmojiForm
from django.views.decorators.http import require_POST

from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

class Home(LoginView):
    template_name = 'home.html'


def about(request):
    return render(request, 'about.html')


def notes_index(request):
    notes = Note.objects.filter(user=request.user).order_by('-is_pinned', '-created_at')
    return render(request, 'notes/index.html', {'notes': notes})


def note_detail(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    emojis = note.emojis.all()
    tasks = note.tasks.all()
    task_form = TaskForm()

    if request.method == 'POST':

        for task in tasks:
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

        if 'toggle_pin' in request.POST:
            note.is_pinned = not note.is_pinned
            note.save()

        return redirect('note-detail', note_id=note.id)

    return render(request, 'notes/detail.html', {
        'note': note,
        'tasks': tasks,
        'task_form': task_form,
        'emojis': EmojiReact.objects.all(),
        'note_emojis': emojis
    })

@require_POST
def add_emoji(request):
    if request.method == 'POST':
        form = EmojiForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('emoji-index')
    else:
        form = EmojiForm()
    return render(request, 'notes/add_emoji.html', {'form': form})


class NoteCreate(LoginRequiredMixin,CreateView):
    model = Note
    fields = ['title', 'content']
    success_url = '/notes/'
    def form_valid(self, form):
        form.instance.user = self.request.user  
        return super().form_valid(form)

class NoteUpdate(LoginRequiredMixin,UpdateView):
    model = Note
    fields = ['title', 'content']
    template_name = 'main_app/note_form.html'

    def get_success_url(self):
        return reverse('note-detail', kwargs={'note_id': self.object.pk})


class NoteDelete(LoginRequiredMixin, DeleteView):
    model = Note
    success_url = '/notes/'


class EmojiCreate(LoginRequiredMixin,CreateView):
    model = EmojiReact
    fields = '__all__'
    success_url = reverse_lazy('emoji-index') 


class EmojiList(LoginRequiredMixin,ListView):
    model = EmojiReact


class EmojiDetail(LoginRequiredMixin,DetailView):
    model = EmojiReact


class EmojiUpdate(LoginRequiredMixin,UpdateView):
    model = EmojiReact
    fields = ['emoji']
    template_name = 'main_app/emojireact_form.html'
    success_url = reverse_lazy('emoji-index')

class EmojiDelete(LoginRequiredMixin,DeleteView):
    model = EmojiReact
    success_url = reverse_lazy('emoji-index')
    template_name = 'main_app/emojireact_confirm_delete.html'



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



def toggle_pin(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    note.is_pinned = not note.is_pinned
    note.save()
    return redirect('notes_index')


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('notes_index')  
        else:
            error_message = 'Invalid sign up - try again'
    else:
        form = UserCreationForm()
    
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)