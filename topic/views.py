from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from topic.models import Redactor, Topic, Newspaper
from topic.forms import (
    LoginForm,
    SignUpForm,
    RedactorCreationForm,
    NewspaperForm,
    NewspaperSearchForm,
    RedactorUpdateForm,
)


class LoginView(generic.FormView):
    template_name = 'registration/login.html'
    form_class = LoginForm

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            return render(self.request, self.template_name, {'form': form, 'msg': 'Invalid credentials'})

    def get_success_url(self):
        return '/'


class RegisterUserView(generic.FormView):
    template_name = 'registration/register.html'
    form_class = SignUpForm
    success_url = reverse_lazy('newspaper_agency:register-success')

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data['username']
        raw_password = form.cleaned_data['password1']
        user = authenticate(username=username, password=raw_password)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['success'] = True
        context['msg'] = 'Account created successfully.'
        return context


class IndexView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'topic/index.html'

    def get_context_data(self, **kwargs):
        num_redactors = Redactor.objects.count()
        num_topics = Topic.objects.count()
        num_newspaper = Newspaper.objects.count()

        list_topics = Topic.objects.all()
        list_redactors = Redactor.objects.all()
        list_newspaper = Newspaper.objects.all()

        context = {
            'num_redactors': num_redactors,
            'num_topics': num_topics,
            'num_newspaper': num_newspaper,
            'list_topics': list_topics,
            'list_redactors': list_redactors,
            'list_newspaper': list_newspaper,
        }
        return context


class RedactorListView(LoginRequiredMixin, generic.ListView):
    model = Redactor
    paginate_by = 5


class RedactorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Redactor
    queryset = Redactor.objects.prefetch_related("newspaper_redactors__publishers")


class RedactorCreateView(LoginRequiredMixin, generic.CreateView):
    model = Redactor
    form_class = RedactorCreationForm
    success_url = reverse_lazy("newspaper_agency:redactor-list")


class RedactorUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Redactor
    form_class = RedactorUpdateForm
    success_url = reverse_lazy("newspaper_agency:index")


class RedactorDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Redactor
    success_url = reverse_lazy("newspaper_agency:redactor-list")


class TopicListView(LoginRequiredMixin, generic.ListView):
    model = Topic
    paginate_by = 5


class TopicCreateView(LoginRequiredMixin, generic.CreateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("newspaper_agency:topic-list")


class TopicUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("newspaper_agency:topic-list")


class TopicDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Topic
    success_url = reverse_lazy("newspaper_agency:topic-list")


class TopicDetailView(LoginRequiredMixin, generic.DetailView):
    model = Topic
    queryset = Topic.objects.all()
    paginate_by = 5


class NewspaperListView(LoginRequiredMixin, generic.ListView):
    model = Newspaper
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewspaperListView, self).get_context_data(**kwargs)
        title = self.request.GET.get("title", "")
        context["search_form"] = NewspaperSearchForm(initial={"title": title})
        return context

    def get_queryset(self):
        queryset = Newspaper.objects.all()
        form = NewspaperSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(title__icontains=form.cleaned_data["title"])
        return queryset


class NewspaperDetailView(LoginRequiredMixin, generic.DetailView):
    model = Newspaper


class NewspaperCreateView(LoginRequiredMixin, generic.CreateView):
    model = Newspaper
    form_class = NewspaperForm
    success_url = reverse_lazy("newspaper_agency:newspaper-list")


class NewspaperUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Newspaper
    form_class = NewspaperForm
    success_url = reverse_lazy("newspaper_agency:newspaper-list")


class NewspaperDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Newspaper
    success_url = reverse_lazy("newspaper_agency:newspaper-list")
