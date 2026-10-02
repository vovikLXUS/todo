from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from tasks.models import Task, Tag


class ModelTests(TestCase):
    def test_tag_str(self):
        tag = Tag.objects.create(name="work")
        self.assertEqual(str(tag), "work")

    def test_task_str(self):
        task = Task.objects.create(content="Test task", is_done=False)
        self.assertEqual(str(task), "Test task (Not done)")
        task.is_done = True
        self.assertEqual(str(task), "Test task (Done)")

    def test_task_ordering(self):
        now = timezone.now()
        # Create completed task earlier
        task1 = Task.objects.create(content="Task 1", is_done=True)
        # Create uncompleted task
        task2 = Task.objects.create(content="Task 2", is_done=False)
        # Create another uncompleted task later
        task3 = Task.objects.create(content="Task 3", is_done=False)

        tasks = list(Task.objects.all())
        # Uncompleted tasks should come first, and among them newer first
        self.assertEqual(tasks[0], task3)
        self.assertEqual(tasks[1], task2)
        self.assertEqual(tasks[2], task1)

    def test_task_datetime_property(self):
        task = Task.objects.create(content="Test")
        self.assertEqual(task.datetime, task.created_at)


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.tag1 = Tag.objects.create(name="home")
        self.tag2 = Tag.objects.create(name="shop")
        self.task = Task.objects.create(content="Buy milk", is_done=False)
        self.task.tags.add(self.tag1, self.tag2)

    def test_home_page_status_and_content(self):
        response = self.client.get(reverse("tasks:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/index.html")
        self.assertTemplateUsed(response, "base.html")
        self.assertContains(response, "TODO list")
        self.assertContains(response, "Buy milk")
        self.assertContains(response, "Not done")
        self.assertContains(response, "Complete")
        self.assertContains(response, "home")
        self.assertContains(response, "shop")

    def test_toggle_task_status_view(self):
        url = reverse("tasks:toggle-task-status", args=[self.task.id])
        # Post request toggles to done
        response = self.client.post(url)
        self.assertRedirects(response, reverse("tasks:index"))
        self.task.refresh_from_db()
        self.assertTrue(self.task.is_done)

        # Calling again toggles back to not done
        response = self.client.get(url)
        self.assertRedirects(response, reverse("tasks:index"))
        self.task.refresh_from_db()
        self.assertFalse(self.task.is_done)

    def test_tag_list_page(self):
        response = self.client.get(reverse("tasks:tag-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/tag_list.html")
        self.assertContains(response, "Tag list")
        self.assertContains(response, "home")
        self.assertContains(response, "shop")

    def test_task_create(self):
        url = reverse("tasks:task-create")
        response = self.client.post(url, {
            "content": "New task",
            "tags": [self.tag1.id]
        })
        self.assertRedirects(response, reverse("tasks:index"))
        self.assertTrue(Task.objects.filter(content="New task").exists())

    def test_task_update(self):
        url = reverse("tasks:task-update", args=[self.task.id])
        response = self.client.post(url, {
            "content": "Updated task",
            "tags": [self.tag2.id]
        })
        self.assertRedirects(response, reverse("tasks:index"))
        self.task.refresh_from_db()
        self.assertEqual(self.task.content, "Updated task")

    def test_task_delete(self):
        url = reverse("tasks:task-delete", args=[self.task.id])
        response = self.client.post(url)
        self.assertRedirects(response, reverse("tasks:index"))
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_tag_create(self):
        url = reverse("tasks:tag-create")
        response = self.client.post(url, {"name": "urgent"})
        self.assertRedirects(response, reverse("tasks:tag-list"))
        self.assertTrue(Tag.objects.filter(name="urgent").exists())

    def test_tag_update(self):
        url = reverse("tasks:tag-update", args=[self.tag1.id])
        response = self.client.post(url, {"name": "house"})
        self.assertRedirects(response, reverse("tasks:tag-list"))
        self.tag1.refresh_from_db()
        self.assertEqual(self.tag1.name, "house")

    def test_tag_delete(self):
        url = reverse("tasks:tag-delete", args=[self.tag1.id])
        response = self.client.post(url)
        self.assertRedirects(response, reverse("tasks:tag-list"))
        self.assertFalse(Tag.objects.filter(id=self.tag1.id).exists())
