from django.contrib import admin
from .models import EmojiReact, Note,Task

admin.site.register(Note)
admin.site.register(Task)
admin.site.register(EmojiReact)