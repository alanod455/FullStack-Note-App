# forms.py
from django import forms
from .models import Note, Task
from .models import EmojiReact

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title']  
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter a new task'}),
        }

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'emojis']
        widgets = {
            'emojis': forms.CheckboxSelectMultiple(),  
        }   


class EmojiForm(forms.ModelForm):
    class Meta:
        model = EmojiReact
        fields = ['emoji']
        widgets = {
            'emoji': forms.TextInput(attrs={
                'placeholder': 'Enter emoji here 😊',
                'class': 'emoji-input',
            }),
        }

