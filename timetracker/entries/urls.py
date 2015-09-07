from django.conf.urls import url
from django.contrib.auth.urls import views as auth_views

from . import views

urlpatterns = [
    url(r'^accounts/login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'logout.html'}, name='logout'),
    url(r'^$', views.clientRedirectView, name='entries-root'),
    url(r'^clients/$', views.ClientCreateView.as_view(), name='client-list'),
    url(r'^clients/(?P<pk>\d+)/$', views.ClientUpdateView.as_view(),
        name='client-detail'),
    url(r'^entries/$', views.EntryCreateView.as_view(), name='entry-list'),
    url(r'^projects/$', views.ProjectCreateView.as_view(),
        name='project-list'),
    url(r'^projects/(?P<pk>\d+)/$', views.ProjectUpdateView.as_view(),
        name='project-detail'),
]
