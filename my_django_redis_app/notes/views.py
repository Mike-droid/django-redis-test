from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from .models import Note
from django.core.cache import cache
import json
from django.http import HttpResponseRedirect

RECENT_NOTES_REDIS_KEY = "recent_note_ids"
MAX_RECENT_NOTES = 3


class NoteListView(ListView):
    model = Note
    template_name = "notes_note_list.html"
    context_object_name = "notes"
    ordering = ["-created_at"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        recent_ids_str = cache.get(RECENT_NOTES_REDIS_KEY)
        recent_ids = json.loads(recent_ids_str) if recent_ids_str else []

        unique_recent_ids = []
        for id in recent_ids:
            if id not in unique_recent_ids:
                unique_recent_ids.append(id)

        recent_notes = []
        recent_ids_int = [int(id) for id in unique_recent_ids]

        if recent_ids_int:
            notes_dict = {
                note.id: note for note in Note.objects.filter(id__in=recent_ids_int)
            }
            recent_notes = [notes_dict[id] for id in recent_ids_int if id in notes_dict]

        context["recent_notes"] = recent_notes

        return context


class NoteDetailView(DetailView):
    model = Note
    template_name = "notes/note_detail.html"
    context_object_name = "note"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        note_id_str = str(obj.id)

        recent_ids_str = cache.get(RECENT_NOTES_REDIS_KEY)
        recent_ids = json.loads(recent_ids_str) if recent_ids_str else []

        if note_id_str in recent_ids:
            recent_ids.remove(note_id_str)

        recent_ids.insert(0, note_id_str)
        recent_ids = recent_ids[:MAX_RECENT_NOTES]
        cache.set(RECENT_NOTES_REDIS_KEY, json.dumps(recent_ids))

        return obj


class NoteCreateView(CreateView):
    model = Note
    template_name = "notes/note_form.html"
    fields = ["title", "content"]


class NoteUpdateView(UpdateView):
    model = Note
    template_name = "notes/note_form.html"
    fields = ["title", "content"]


class NoteDeleteView(DeleteView):
    model = Note
    template_name = "notes/note_confirm_delete.html"
    success_url = reverse_lazy("notes:note_list")
    context_object_name = "note"

    def form_valid(self, form):
        note_to_delete_id_str = str(self.object.id)
        self.object.delete()

        try:
            recent_ids_str = cache.get(RECENT_NOTES_REDIS_KEY)
            if recent_ids_str:
                recent_ids = json.loads(recent_ids_str)
                updated_ids = [id for id in recent_ids if id != note_to_delete_id_str]
                cache.set(RECENT_NOTES_REDIS_KEY, json.dumps(updated_ids))
        except Exception as e:
            print(
                f"Error al limpiar la lista de notas recientes en Redis después de la eliminación: {e}"
            )

        return HttpResponseRedirect(self.get_success_url())
