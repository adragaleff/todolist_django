from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from .models import *
from .forms import *
from .utils import *
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.db.models import Q
import secrets

def license_check(func):

    def wrapper(request):
        try:
            clicense = License.objects.get(login=request.user)
        except Exception as e:
            return redirect(f'/profile/{request.user.pk}')
        return func(request)
    return wrapper

# Create your views here.
@login_required(login_url='/login')
@license_check
def home_view(request):
    CheckLicense = ""
    user = request.user
    if user.is_staff:
        tasks = Task.objects.all()
        print(request)
        if request.method == 'POST':
            form = GiveLicense(request.POST, request.user)
            if form.is_valid:
                CheckLicense = ""
                try:
                    CheckLicense = License.objects.get(login=form.data.get('login'))
                    CheckLicense.delete()
                    return redirect('home')
                except Exception as e:
                    licenses = form.save(commit=False)
                    licenses.token = secrets.token_hex(16)
                    licenses.war_token = secrets.token_hex(18)
                    licenses.telegram_id = '0'
                    licenses.save()
                    return redirect('home')
            else:
                print(form.errors)
        else:
            form = GiveLicense()

        context = {
            'tasks': tasks,
            'form': form,
        }

        return render(request, 'home.html', context)
    else:
        tasks = Task.objects.filter(
            Q(owner=user.username) | Q(executor=user.pk)
        )

        context = {
            'tasks': tasks,
        }

        return render(request, 'home.html', context)

@login_required(login_url='/login')
def view_task(request, id):
    user = request.user

    task = Task.objects.get(id=id)

    if task.owner == user.username or user.is_staff == 1 or task.executor.username == user.username :

        comments = CommentsTask.objects.filter(task_id=id)

        if request.method == 'POST':
            if task.is_archive == '0':
                form = AddComment(request.POST, request.user)
                if form.is_valid:
                    saveform = form.save(commit=False)
                    saveform.login = request.user
                    saveform.task_id = id
                    saveform.save()
                    context = {
                        'task': task,
                        'comments': comments,
                        'form': form,
                    }
                    return redirect(f'/task/{id}')
            else:
                return redirect(f'/task/{id}')
        else:
            form = AddComment()

        context = {
            'task': task,
            'comments': comments,
            'form': form,
            'user': user,
        }

        return render(request, 'task.html', context)
    else:
        return redirect('home')

@login_required(login_url='/login')
def delete_comment(request, id):
    user = request.user
    comment = CommentsTask.objects.get(id=id)

    if user.username == comment.login.username or user.is_staff == 1:
        comment.delete()
        return redirect(f'/task/{comment.task_id}')
    else:
        return redirect(f'/task/{comment.task_id}')

@login_required(login_url='/login')
@license_check
def addtask_view(request):
    time = datetime.now().strftime('%Y-%m-%d %H:%M')
    user = request.user

    if request.method == 'POST':
        form = AddTaskForm(request.POST, request.user)
        if form.is_valid:
            task = form.save(commit=False)
            task.date_create = time
            task.owner=user.username
            task.save()
            return redirect('home')
        else:
            print(form.errors)
    else:
        form = AddTaskForm()
    
    context = {
        'time': time,
        'form': form,
    }
        
    return render(request, 'addtask.html', context)

@login_required(login_url='/login')
def delete_task(request, id):
    user = request.user
    delete = Task.objects.get(id=id)
    if user.is_staff or str(delete.owner) == str(user.username):
        try:
            delete.delete()
            return redirect('home')
        except Exception as e:
            return redirect('home')
    else:
        return redirect('home')
        
def profile_view(request, pk):
    user = User.objects.get(pk=pk)
    try:
        lic = License.objects.get(login=request.user)
        context = {
        'name': user,
        'lic': lic,
        }   
    except Exception as e:
        context = {
        'name': user,
        }
    

    return render(request, 'profile.html', context)

    

class LoginUser(DataMixin, LoginView):
    form_class = AuthForm
    template_name = 'login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('/login')

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

@login_required(login_url='/login')
def edittask_view(request, id):

    task = Task.objects.get(id=id)
    savetask = Task.objects.get(id=id)

    answer = ""

    if request.method == 'POST':
        form = EditTaskForm(request.POST, instance=task)
        if form.is_valid():
            formsave = form.save(commit=False)
            if formsave.name != savetask.name:
                answer += f"Пользователь изменил название на {formsave.name}\n"
            if formsave.description != savetask.description:
                answer += f"Пользователь изменил описание на {formsave.description}\n"
            if formsave.priority != savetask.priority:
                answer += f"Пользователь изменил приоритет задачи на {formsave.priority}\n"
            if formsave.date_of_staging != savetask.date_of_staging:
                answer += f"Пользователь дату исполнения на {formsave.date_of_staging}\n"
            if formsave.executor != savetask.executor:
                answer += f"Пользователь изменил исполнителя на {formsave.executor}\n"
            formsave.save()

            if answer == "":
                pass
            else:
                saveform = CommentsTask.objects.create(login=request.user,comments=f"{answer}", task_id=id)
                saveform.save()

            return redirect(f'/task/{id}')
        else:
            print(form.errors)
    else:
        form = EditTaskForm(instance=task)

    context = {
        'task': task,
        'form': form,
    }

    return render(request, 'edittask.html', context)

@login_required(login_url='/login')
def archive_task(request, id):
    task = Task.objects.get(id=id)

    user = request.user

    if (task.executor.username == user.username or user.is_staff == 1) and task.is_archive == '0':
        task.is_archive = '1'
        task.save()
        return redirect(f'/task/{id}')
    elif (task.owner == user.username or user.is_staff == 1) and task.is_archive == '1':
        task.is_archive = '0'
        task.save()
        return redirect(f'/task/{id}')