# models.py
from django.db import models

class EmojiReact(models.Model):
    emoji = models.CharField(max_length=5)  

    def __str__(self):
        return self.emoji


class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    emojis = models.ManyToManyField(EmojiReact, blank=True, related_name='notes')  
    is_pinned = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    

class Task(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title



class Pin(models.Model):
    note = models.OneToOneField('Note', on_delete=models.CASCADE, related_name='pin')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Pin for note: {self.note.title}"
