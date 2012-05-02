from django.conf.urls.defaults import patterns, url
from django.views.generic import ListView, DetailView

from demandapp.views import Verify, Logout, DemandView
from demandapp.models import Site

urlpatterns = patterns('',
    url(r'^browserid/verify/$', Verify.as_view(), name='verify'),
    url(r'^browserid/logout/$', Logout.as_view(), name='logout'),
    url(r'^$', ListView.as_view(queryset=Site.objects.top())),
    url(r'^demand/((?P<site>[\.\w]+)/)?$', DemandView.as_view(), name='demand'),
    url(r'^(?P<slug>[\.\w]+)/$', DetailView.as_view(model=Site,
        slug_field='domain')),
)
