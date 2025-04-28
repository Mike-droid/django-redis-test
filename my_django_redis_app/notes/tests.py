from django.test import TestCase, Client
from django.urls import reverse
from .models import Note
from django.core.cache import cache
import json


RECENT_NOTES_REDIS_KEY = "recent_note_ids"
MAX_RECENT_NOTES = 3


class NoteViewsTests(TestCase):

    def setUp(self):

        self.client = Client()

        self.note1 = Note.objects.create(
            title="First Note", content="Content of the first note"
        )
        self.note2 = Note.objects.create(
            title="Second Note", content="Content of the second note"
        )
        self.note3 = Note.objects.create(
            title="Third Note", content="Content of the third note"
        )
        self.note4 = Note.objects.create(
            title="Fourth Note", content="Content of the fourth note"
        )
        self.note5 = Note.objects.create(
            title="Fifth Note", content="Content of the fifth note"
        )

        cache.clear()

        cache.delete(RECENT_NOTES_REDIS_KEY)

    def test_note_list_view_status_code(self):
        """List view should return HTTP Status Code 200"""
        response = self.client.get(reverse("notes:note_list"))
        self.assertEqual(response.status_code, 200)

    def test_note_list_view_correct_template(self):
        """List view should use the correct template"""
        response = self.client.get(reverse("notes:note_list"))
        self.assertTemplateUsed(response, "notes/note_list.html")
        self.assertTemplateUsed(response, "base.html")

    def test_note_list_view_contains_all_notes(self):
        """List view should return all existings notes"""
        response = self.client.get(reverse("notes:note_list"))
        self.assertContains(response, self.note1.title)
        self.assertContains(response, self.note2.title)
        self.assertContains(response, self.note3.title)
        self.assertContains(response, self.note4.title)
        self.assertContains(response, self.note5.title)

    def test_note_list_view_recent_notes_initially_empty(self):
        """List view should start empty"""
        response = self.client.get(reverse("notes:note_list"))

        self.assertEqual(len(response.context["recent_notes"]), 0)

        self.assertNotContains(response, "Notas Visitadas Recientemente")

    def test_note_list_view_displays_recent_notes_from_redis(self):
        """List view should display recent notes from Redis"""

        recent_ids_list = [
            str(self.note3.id),
            str(self.note1.id),
            str(self.note5.id),
        ]
        cache.set(RECENT_NOTES_REDIS_KEY, json.dumps(recent_ids_list))

        response = self.client.get(reverse("notes:note_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Notas Visitadas Recientemente")

        recent_notes_context = response.context["recent_notes"]

        self.assertEqual(len(recent_notes_context), len(recent_ids_list))
        self.assertEqual(recent_notes_context[0].id, self.note3.id)
        self.assertEqual(recent_notes_context[1].id, self.note1.id)
        self.assertEqual(recent_notes_context[2].id, self.note5.id)

        self.assertContains(response, self.note3.title)
        self.assertContains(response, self.note1.title)
        self.assertContains(response, self.note5.title)

    def test_note_detail_view_status_code(self):
        """Detail view should return HTTP Status Code 200 for existing note"""
        response = self.client.get(reverse("notes:note_detail", args=[self.note1.pk]))
        self.assertEqual(response.status_code, 200)

    def test_note_detail_view_not_found(self):
        """Detail view should return 404 for non-existing note"""
        response = self.client.get(reverse("notes:note_detail", args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_note_detail_view_correct_template(self):
        """Detail view should use the correct template"""
        response = self.client.get(reverse("notes:note_detail", args=[self.note1.pk]))
        self.assertTemplateUsed(response, "notes/note_detail.html")
        self.assertTemplateUsed(response, "base.html")

    def test_note_detail_view_correct_context(self):
        """Detail view should return the correct note in context"""
        response = self.client.get(reverse("notes:note_detail", args=[self.note2.pk]))
        self.assertEqual(response.context["note"], self.note2)
        self.assertContains(response, self.note2.title)
        self.assertContains(response, self.note2.content)

    def test_note_detail_view_adds_to_recent_notes_redis(self):
        """Detail view should add note ID to recent notes in Redis"""

        self.assertIsNone(cache.get(RECENT_NOTES_REDIS_KEY))

        self.client.get(reverse("notes:note_detail", args=[self.note1.pk]))
        recent_ids = json.loads(cache.get(RECENT_NOTES_REDIS_KEY))
        self.assertEqual(recent_ids, [str(self.note1.id)])

        self.client.get(reverse("notes:note_detail", args=[self.note3.pk]))
        recent_ids = json.loads(cache.get(RECENT_NOTES_REDIS_KEY))
        self.assertEqual(recent_ids, [str(self.note3.id), str(self.note1.id)])

        self.client.get(reverse("notes:note_detail", args=[self.note5.pk]))
        recent_ids = json.loads(cache.get(RECENT_NOTES_REDIS_KEY))
        self.assertEqual(
            recent_ids, [str(self.note5.id), str(self.note3.id), str(self.note1.id)]
        )

        self.client.get(reverse("notes:note_detail", args=[self.note2.pk]))
        recent_ids = json.loads(cache.get(RECENT_NOTES_REDIS_KEY))
        self.assertEqual(
            recent_ids, [str(self.note2.id), str(self.note5.id), str(self.note3.id)]
        )
        self.assertEqual(len(recent_ids), MAX_RECENT_NOTES)

        self.client.get(reverse("notes:note_detail", args=[self.note5.pk]))
        recent_ids = json.loads(cache.get(RECENT_NOTES_REDIS_KEY))
        self.assertEqual(
            recent_ids, [str(self.note5.id), str(self.note2.id), str(self.note3.id)]
        )

    def test_note_create_view_status_code(self):
        """Create view should return HTTP Status Code 200 for GET"""
        response = self.client.get(reverse("notes:note_create"))
        self.assertEqual(response.status_code, 200)

    def test_note_create_view_correct_template(self):
        """Create view should use the correct template"""
        response = self.client.get(reverse("notes:note_create"))
        self.assertTemplateUsed(response, "notes/note_form.html")
        self.assertTemplateUsed(response, "base.html")

    def test_note_create_view_valid_post(self):
        """Send a valid POST to the create view should create a note and redirect"""

        self.assertEqual(Note.objects.count(), 5)

        valid_data = {"title": "New Test Note", "content": "Content for the new note"}
        response = self.client.post(reverse("notes:note_create"), valid_data)

        self.assertEqual(response.status_code, 302)

        self.assertEqual(Note.objects.count(), 6)

        new_note = Note.objects.latest("created_at")
        self.assertEqual(new_note.title, valid_data["title"])
        self.assertEqual(new_note.content, valid_data["content"])

        self.assertRedirects(response, new_note.get_absolute_url())

    def test_note_create_view_invalid_post(self):
        """Send an invalid POST to the create view should show errors and not create a note"""
        initial_note_count = Note.objects.count()

        invalid_data = {"title": "", "content": "Some content"}

    def test_note_update_view_status_code(self):
        """Update view should return HTTP Status Code 200 for GET of existing note"""
        response = self.client.get(reverse("notes:note_update", args=[self.note1.pk]))
        self.assertEqual(response.status_code, 200)

    def test_note_update_view_not_found(self):
        """Update view should return 404 for GET of non-existing note"""
        response = self.client.get(reverse("notes:note_update", args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_note_update_view_correct_template(self):
        """Update view should use the correct template"""
        response = self.client.get(reverse("notes:note_update", args=[self.note1.pk]))
        self.assertTemplateUsed(response, "notes/note_form.html")
        self.assertTemplateUsed(response, "base.html")

    def test_note_update_view_form_prefilled(self):
        """Update form should be prefilled with existing note data"""
        response = self.client.get(reverse("notes:note_update", args=[self.note2.pk]))
        self.assertContains(response, f'value="{self.note2.title}"')
        self.assertContains(response, self.note2.content)

    def test_note_update_view_valid_post(self):
        """Send a valid POST to the update view should update the note and redirect"""
        updated_data = {
            "title": "Updated Title",
            "content": "Updated content for the note",
        }
        response = self.client.post(
            reverse("notes:note_update", args=[self.note3.pk]), updated_data
        )

        self.assertEqual(response.status_code, 302)

        self.note3.refresh_from_db()
        self.assertEqual(self.note3.title, updated_data["title"])
        self.assertEqual(self.note3.content, updated_data["content"])

        self.assertRedirects(response, self.note3.get_absolute_url())

    def test_note_update_view_invalid_post(self):
        """Send an invalid POST to the update view should show errors and not update the note"""
        original_title = self.note4.title
        original_content = self.note4.content

    def test_note_delete_view_status_code(self):
        """Delete view should return HTTP Status Code 200 for GET of existing note"""
        response = self.client.get(reverse("notes:note_delete", args=[self.note1.pk]))
        self.assertEqual(response.status_code, 200)

    def test_note_delete_view_not_found(self):
        """Delete view should return 404 for GET of non-existing note"""
        response = self.client.get(reverse("notes:note_delete", args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_note_delete_view_correct_template(self):
        """Delete view should use the correct template"""
        response = self.client.get(reverse("notes:note_delete", args=[self.note1.pk]))
        self.assertTemplateUsed(response, "notes/note_confirm_delete.html")
        self.assertTemplateUsed(response, "base.html")

    def test_note_delete_view_post_deletes_note(self):
        """Send a POST to the delete view should delete the note and redirect"""
        initial_count = Note.objects.count()

        response = self.client.post(reverse("notes:note_delete", args=[self.note2.pk]))

        self.assertEqual(response.status_code, 302)

        self.assertEqual(Note.objects.count(), initial_count - 1)

        self.assertFalse(Note.objects.filter(pk=self.note2.pk).exists())

        self.assertRedirects(response, reverse("notes:note_list"))

    def test_note_delete_view_cleans_up_redis_recent_notes(self):
        """Deleting a note should clean up the recent notes in Redis"""

        initial_recent_ids = [
            str(self.note1.id),
            str(self.note3.id),
            str(self.note5.id),
        ]
        cache.set(RECENT_NOTES_REDIS_KEY, json.dumps(initial_recent_ids))

        response = self.client.post(reverse("notes:note_delete", args=[self.note3.pk]))

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Note.objects.filter(pk=self.note3.pk).exists())

        updated_recent_ids_str = cache.get(RECENT_NOTES_REDIS_KEY)
        self.assertIsNotNone(updated_recent_ids_str)
        updated_recent_ids = json.loads(updated_recent_ids_str)

        self.assertNotIn(str(self.note3.id), updated_recent_ids)

        self.assertIn(str(self.note1.id), updated_recent_ids)
        self.assertIn(str(self.note5.id), updated_recent_ids)

        self.assertEqual(len(updated_recent_ids), len(initial_recent_ids) - 1)

        cache.set(RECENT_NOTES_REDIS_KEY, json.dumps(initial_recent_ids))
        response = self.client.post(reverse("notes:note_delete", args=[self.note2.pk]))

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Note.objects.filter(pk=self.note2.pk).exists())

        recent_ids_after_deleting_non_recent = json.loads(
            cache.get(RECENT_NOTES_REDIS_KEY)
        )

        self.assertEqual(recent_ids_after_deleting_non_recent, initial_recent_ids)
