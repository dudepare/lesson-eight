from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import ClientForm, EntryForm, ProjectForm
from .models import Client, Entry, Project


class FormAuthorMixin(object):

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(FormAuthorMixin, self).form_valid(form)


class OwnerDataMixin(object):

    def get_queryset(self):
        qs = super(OwnerDataMixin, self).get_queryset()
        qs = qs.filter(author=self.request.user)
        return qs


class LoginRequiredMixin(object):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class ClientCreateView(LoginRequiredMixin, OwnerDataMixin, FormAuthorMixin, CreateView):
    """
    CBV version of above "clients" view function

    This view has a form for creating new clients. It also displays a list of
    clients. We could have used ListView for the latter part but then we
    wouldn't have the form handling of CreateView. It could be possible to mix
    in the functionality of CreateView and ListView classes with a combination
    of the mixin classes they comprise of but for the sake of simplicity we'll
    just pass the client queryset into the template context via
    get_context_data().
    """
    model = Client
    form_class = ClientForm
    template_name = 'clients.html'
    # Alternately to defining a get_success_url method returning
    # reverse('client-list'), reverse_lazy allows us to provide a url reversal
    # before the project's URLConf is loaded
    success_url = reverse_lazy('client-list')

    def get_context_data(self, **kwargs):
        context = super(ClientCreateView, self).get_context_data(**kwargs)
        context['client_list'] = self.get_queryset()
        return context


class ClientUpdateView(LoginRequiredMixin, OwnerDataMixin, FormAuthorMixin, UpdateView):
    """
    CBV version of above "client_detail" view function
    """
    model = Client
    form_class = ClientForm
    template_name = 'client_detail.html'
    success_url = reverse_lazy('client-list')


class EntryCreateView(LoginRequiredMixin, OwnerDataMixin, FormAuthorMixin, CreateView):
    """
    CBV version of above "entries" view function
    """
    model = Entry
    form_class = EntryForm
    success_url = reverse_lazy('entry-list')
    template_name = 'entries.html'

    def get_context_data(self, **kwargs):
        context = super(EntryCreateView, self).get_context_data(**kwargs)
        context['entry_list'] = self.get_queryset()
        return context


class ProjectCreateView(LoginRequiredMixin, OwnerDataMixin, FormAuthorMixin, CreateView):
    """
    CBV version of above "projects" view function
    """
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy('project-list')
    template_name = 'projects.html'

    def time_spent(self, entrylist):
        summary = {}
        for entry in entrylist:
            project_name = entry.project.name
            if project_name in summary.keys():
                summary[project_name] += entry.duration
            else:
                summary[project_name] = entry.duration
        return summary

    def get_context_data(self, **kwargs):
        context = super(ProjectCreateView, self).get_context_data(**kwargs)
        project_totals = self.time_spent(Entry.objects.all())
        user_totals = self.time_spent(Entry.objects.filter(author=self.request.user))
        project_list = self.get_queryset()
        for p in project_list:
            if p.name in project_totals.keys():
                p.total_time = project_totals[p.name]
            else:
                p.total_time = 0.0

            if p.name in user_totals.keys():
                p.user_total = user_totals[p.name]
            else:
                p.user_total = 0.0

        context['project_list'] = project_list
        return context


class ProjectUpdateView(LoginRequiredMixin, OwnerDataMixin, FormAuthorMixin, UpdateView):
    """
    CBV version of above "project_detail" view function
    """
    model = Project
    form_class = ProjectForm
    template_name = 'project_detail.html'
    success_url = reverse_lazy('project-list')

    def get_context_data(self, **kwargs):
        context = super(ProjectUpdateView, self).get_context_data(**kwargs)
        return context


def clientRedirectView(request):
    if request.user.is_authenticated():
        return redirect('client-list')
    else:
        return redirect('login')
