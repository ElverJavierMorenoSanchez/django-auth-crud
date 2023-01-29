from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import CreateTask, Singup
from django.utils import timezone


def home(request):
    return render(request, 'home.html')


def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if not user:
            return render(request, 'signin.html', {'form': Singup(), 'error': 'username or password incorrect'})

        login(request, user)
        return redirect('home')

    return render(request, 'signin.html', {'form': Singup()})


def signup(request):

    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']

            user = User.objects.create_user(
                username=username, password=password)

            user.save()

            login(request, user)
            return redirect('tasks')
        except:
            return render(request, 'signup.html', {'form': Singup(), 'error': 'Username already exists'})

    return render(request, 'signup.html', {'form': Singup()})


def signout(request):
    logout(request)
    return redirect('home')


@login_required
def tasks(request):
    tasks = list(Task.objects.filter(
        user=request.user))
    return render(request, 'tasks.html', {'tasks': tasks})


@login_required
def create_task(request):
    if request.method == 'POST':
        try:

            form = CreateTask(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except:
            return render(request, 'create_task.html', {'form': CreateTask, 'error': 'Something went wrong'})

    return render(request, 'create_task.html', {'form': CreateTask})


@login_required
def task_detail(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    form = CreateTask(instance=task)

    if request.method == 'POST':
        try:
            form = CreateTask(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except:
            return render(request, 'task_detail.html', {'task': task, 'form': form, 'error': 'Somthing went wrong'})
    return render(request, 'task_detail.html', {'task': task, 'form': form})


@login_required
def task_complete(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

    return redirect('tasks')


@login_required
def task_delete(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
