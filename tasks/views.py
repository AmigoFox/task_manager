from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Case, Value, When

from .forms import TaskForm
from .models import Task


def index(request):
    return render(request, 'tasks/index.html')


@login_required
def tasks_list(request):
    tasks = Task.objects.filter(owner=request.user).annotate(
        priority_order=Case(
            When(priority=Task.HIGH, then=Value(0)),
            When(priority=Task.NORMAL, then=Value(1)),
            When(priority=Task.LOW, then=Value(2)),
            default=Value(3),
        ),
        due_missing=Case(
            When(due_date__isnull=True, then=Value(1)),
            default=Value(0),
        ),
    ).order_by('completed', 'priority_order', 'due_missing', 'due_date')
    return render(request, 'tasks/tasks_list.html', {'tasks': tasks})


@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            task.save()
            return redirect('tasks:tasks_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/create_task.html', {'form': form})


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, owner=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks:tasks_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/edit_task.html', {'form': form, 'task': task})


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, owner=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks:tasks_list')
    return render(request, 'tasks/delete_task.html', {'task': task})


@login_required
def toggle_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, owner=request.user)
    if request.method == 'POST':
        task.completed = not task.completed
        task.save()
    return redirect('tasks:tasks_list')