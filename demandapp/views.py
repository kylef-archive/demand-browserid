from urlparse import urlparse
import re

from django.shortcuts import redirect
from django.views.generic.edit import BaseFormView
from django.views.generic import RedirectView
from django.core.exceptions import ObjectDoesNotExist

from browserid import verify
from demandapp.forms import BrowserIDForm
from demandapp.models import Site, Vote


class Verify(BaseFormView):
    form_class = BrowserIDForm

    def get_audience(self):
        return '*'

    def login_success(self):
        return redirect('/')

    def login_failure(self):
        return redirect('/')

    def form_valid(self, form):
        assertion = form.cleaned_data['assertion']
        data = verify(assertion, self.get_audience())
        if data:
            self.request.session['browserid'] = data['email']
            print self.request.session['browserid']
            return self.login_success()

        return self.login_failure()

    def form_invalid(self, *args, **kwargs):
        return self.login_failure()


class Logout(RedirectView):
    url = '/'

    def get_redirect_url(self, **kwargs):
        return self.request.META['HTTP_REFERER']

    def get(self, request, *args, **kwargs):
        if 'browserid' in request.session:
            del request.session['browserid']

        return super(Logout, self).get(request, *args, **kwargs)


class DemandView(RedirectView):
    def get_redirect_url(self, **kwargs):
        if self.site:
            return self.site.get_absolute_url()
        return '/'

    def handle_site(self, request, domain):
        self.site = None

        # we silently fail on errors

        if not request.browserid:
            return  # we ain't logged in

        o = urlparse(domain)
        domain = re.sub(r'^www\.', '', str(o.hostname))

        if not domain:
            return
        if '.' not in domain:
            return  # if it looks like a domain, then we will allow it

        try:
            self.site = Site.objects.filter(domain=domain).get()
        except ObjectDoesNotExist:
            self.site = Site(domain=domain)
            self.site.save()

        vote = Vote(voter=unicode(request.browserid), website=self.site)

        try:
            vote.save()
        except:
           pass

    def get(self, request, site):
        self.handle_site(request, site)
        return super(DemandView, self).get(request)

    def post(self, request, site=None):
        self.handle_site(request, request.POST.get('site'))
        return super(DemandView, self).get(request)

