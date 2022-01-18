from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .models import Task
from .forms import AddTaskForm

# Homepage
def home_view(request):
    return render(request, 'task/home.html')


# Add / View Tasks
@login_required
def tasks(request):
    task = Task.objects.filter( user = request.user )
    # pagination limit( 5)
    paginator = Paginator(task, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # form post
    if request.method == 'POST':
        form = AddTaskForm(request.POST, request.FILES,)
        if form.is_valid():
            form.save()
            return redirect('task:my_tasks')

    else: 
        form = AddTaskForm()
        context = {
            'task': task,
            'form': form,
            'page_obj': page_obj,
        }
    return render(request, 'task/tasks.html', context)

# Task Detail


@login_required
def task_detail(request, pk):
    task = Task.objects.get(id=pk)
    context = {
        'task': task
    }
    return render(request, 'task/task_detail.html', context)

# Task Update


@login_required
def task_update(request, pk):
    task = Task.objects.get(id=pk)
    form = AddTaskForm(request.POST, request.FILES, instance = task)

    if form.is_valid():
        form.save()
        return redirect('task:task_detail', pk=task.id)
    else:
        form = AddTaskForm(instance = task)
    context = {
        'form': form,
        'task': task,
    }

    return render(request, 'task/task_update.html', context)



# Delete Task
@login_required
def task_delete(request, pk):
    try:
        task = Task.objects.get(id=pk, user=request.user)
        task.delete()
    except:
        pass
    return redirect('task:my_tasks')


# errors
def custom_page_not_found_view(request, exception):
    return render(request, "task/404.html", {})


def custom_error_view(request, exception=None):
    return render(request, "task/500.html", {})


def custom_permission_denied_view(request, exception=None):
    return render(request, "task/403.html", {})


def custom_bad_request_view(request, exception=None):
    return render(request, "task/400.html", {})
