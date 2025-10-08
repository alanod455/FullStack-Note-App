from django.contrib import admin
from .models import EmojiReact, Note,Task, Pin

admin.site.register(Note)
admin.site.register(Task)
admin.site.register(EmojiReact)
admin.site.register(Pin)