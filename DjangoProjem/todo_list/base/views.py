from typing import Any, Dict
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from .models import Task
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView ,UpdateView ,DeleteView,FormView

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login 

# Create your views here.


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self) -> str:
        return  reverse_lazy("tasks")



class RegisterPage(FormView):
    tamplate_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')







class tasklist(LoginRequiredMixin,ListView):
    model = Task 
    context_object_name = "tasks"

    def get_context_data(self, **kwargs) : 
      
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complate=False).count()


        search_input = self.request.GET.get('search-area') 
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title_startswith =search_input)

        context['search_input'] = search_input
        return context


class taskdetail(DetailView):
    model = Task
    context_object_name = "task"
    template_name = 'base/task.html'


class taskcreate(CreateView):
    model = Task
    fields = ['title','description','complate']
    success_url = reverse_lazy('tasks')

    def form_valid(self,form):
        form.instance.user = self.request.user
        return super(taskcreate,self).form_valid(form)

class taskupdate(UpdateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('tasks')


class taskdelete(DeleteView):
    model = Task
    context_object_name = "task "
    success_url = reverse_lazy('tasks')

