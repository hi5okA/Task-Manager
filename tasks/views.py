from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from .models import Task
from .forms import TaskForm

def signup(request):
    """
    User signup view. Automatically logs in user upon successful registration.
    """
    if request.user.is_authenticated:
        return redirect('task_list')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to Task Manager, {user.username}!")
            return redirect('task_list')
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def task_list(request):
    """
    Displays personal tasks for the logged-in user with filter and search capabilities.
    Enforces server-side data ownership: filter(owner=request.user).
    """
    tasks = Task.objects.filter(owner=request.user)
    
    # Search filter
    search_query = request.GET.get('q', '').strip()
    if search_query:
        tasks = tasks.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query)
        )
    
    # Status filter
    status_filter = request.GET.get('status', 'all')
    if status_filter == 'completed':
        tasks = tasks.filter(completed=True)
    elif status_filter == 'pending':
        tasks = tasks.filter(completed=False)

    # Metric summaries
    all_user_tasks = Task.objects.filter(owner=request.user)
    total_count = all_user_tasks.count()
    completed_count = all_user_tasks.filter(completed=True).count()
    pending_count = all_user_tasks.filter(completed=False).count()
    
    today = timezone.now().date()
    overdue_count = all_user_tasks.filter(
        completed=False, 
        due_date__lt=today
    ).count()

    context = {
        'tasks': tasks,
        'search_query': search_query,
        'status_filter': status_filter,
        'total_count': total_count,
        'completed_count': completed_count,
        'pending_count': pending_count,
        'overdue_count': overdue_count,
        'today': today,
    }
    return render(request, 'tasks/task_list.html', context)


@login_required
def task_create(request):
    """
    View to create a new task. Sets task.owner = request.user upon saving.
    """
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            task.save()
            messages.success(request, f"Task '{task.title}' created successfully!")
            return redirect('task_list')
    else:
        form = TaskForm()

    return render(request, 'tasks/task_form.html', {
        'form': form,
        'action_title': 'Create Task',
        'submit_text': 'Create Task'
    })


@login_required
def task_update(request, pk):
    """
    View to edit an existing task. Strict owner verification using get_object_or_404.
    """
    task = get_object_or_404(Task, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, f"Task '{task.title}' updated successfully!")
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)

    return render(request, 'tasks/task_form.html', {
        'form': form,
        'task': task,
        'action_title': 'Edit Task',
        'submit_text': 'Save Changes'
    })


@login_required
def task_delete(request, pk):
    """
    View to confirm and delete a task. Strict owner verification using get_object_or_404.
    """
    task = get_object_or_404(Task, pk=pk, owner=request.user)

    if request.method == 'POST':
        task_title = task.title
        task.delete()
        messages.success(request, f"Task '{task_title}' deleted.")
        return redirect('task_list')

    return render(request, 'tasks/task_confirm_delete.html', {'task': task})


@login_required
def task_toggle_complete(request, pk):
    """
    POST view to toggle completion status of a task. Enforces owner check.
    """
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    if request.method in ['POST', 'GET']:  # allow quick POST or action link
        task.completed = not task.completed
        task.save()
        status_str = "completed" if task.completed else "marked pending"
        messages.info(request, f"Task '{task.title}' {status_str}.")
    
    return redirect('task_list')
