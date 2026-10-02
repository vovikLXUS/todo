from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import View, generic

from tasks.forms import TaskForm, TagForm
from tasks.models import Task, Tag


class TaskListView(generic.ListView):
    model = Task
    template_name = "tasks/index.html"
    context_object_name = "task_list"
    queryset = Task.objects.prefetch_related("tags")


class TaskCreateView(generic.CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("tasks:index")


class TaskUpdateView(generic.UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("tasks:index")


class TaskDeleteView(generic.DeleteView):
    model = Task
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy("tasks:index")


class TaskToggleStatusView(View):
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.is_done = not task.is_done
        task.save()
        return HttpResponseRedirect(reverse_lazy("tasks:index"))

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.is_done = not task.is_done
        task.save()
        return HttpResponseRedirect(reverse_lazy("tasks:index"))


class TagListView(generic.ListView):
    model = Tag
    template_name = "tasks/tag_list.html"
    context_object_name = "tag_list"
    queryset = Tag.objects.all()


class TagCreateView(generic.CreateView):
    model = Tag
    form_class = TagForm
    template_name = "tasks/tag_form.html"
    success_url = reverse_lazy("tasks:tag-list")


class TagUpdateView(generic.UpdateView):
    model = Tag
    form_class = TagForm
    template_name = "tasks/tag_form.html"
    success_url = reverse_lazy("tasks:tag-list")


class TagDeleteView(generic.DeleteView):
    model = Tag
    template_name = "tasks/tag_confirm_delete.html"
    success_url = reverse_lazy("tasks:tag-list")