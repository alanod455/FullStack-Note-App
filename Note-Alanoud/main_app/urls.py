from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('notes/', views.notes_index, name='notes_index'),

    path('notes/<int:note_id>/', views.note_detail, name='note-detail'),

    path('notes/create/', views.NoteCreate.as_view(), name='note-create'),
    path('notes/<int:pk>/update/', views.NoteUpdate.as_view(), name='note-update'),
    path('notes/<int:pk>/delete/', views.NoteDelete.as_view(), name='note-delete'),

    path('emoji/create/', views.add_emoji, name='emoji-create'),
    path('emoji/<int:pk>/', views.EmojiDetail.as_view(), name='emoji-detail'),
    path('emoji/', views.EmojiList.as_view(), name='emoji-index'),
    path('emoji/<int:pk>/edit/', views.EmojiUpdate.as_view(), name='emoji-edit'),  
    path('emoji/<int:pk>/delete/', views.EmojiDelete.as_view(), name='emoji-delete'), 
    path('notes/<int:note_id>/associate-emoji/<int:emoji_id>/', views.associate_emoji, name='associate-emoji'),
    path('notes/<int:note_id>/remove-emoji/<int:emoji_id>/', views.remove_emoji, name='remove-emoji'),

]
