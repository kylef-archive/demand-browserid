from django.shortcuts import redirect
from django.views.generic.edit import BaseFormView
from django.views.generic import RedirectView
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

from browserid import verify
from demandapp.forms import BrowserIDForm
from demandapp.models import Site, Vote
from demandapp.utils import normalise_site


class Verify(BaseFormView):
    form_class = BrowserIDForm

    def get_audience(self):
        return 'https://demand-browserid.herokuapp.com'

    def login_success(self):
        messages.success(self.request, 'Welcome %s' %
                self.request.session['browserid'])
        return redirect('/')

    def login_failure(self):
        messages.error(self.request, 'Login failed')
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


class DemandException(Exception): pass


class DemandView(RedirectView):
    def get_redirect_url(self, **kwargs):
        if self.site:
            return self.site.get_absolute_url()
        return '/'

    def handle_site(self, request, domain):
        self.site = None

        # we silently fail on errors

        if not request.browserid:
            messages.error(request, 'You are not logged in')
            return

        domain = normalise_site(domain)
        if not domain:
            messages.error(request, "The domain '%s' does not look valid" % domain)
            return

        try:
            self.site = Site.objects.filter(domain=domain).get()
        except ObjectDoesNotExist:
            self.site = Site(domain=domain)
            self.site.save()
            messages.success(request, 'You have voted for %s' % self.site)

        vote = Vote(voter=unicode(request.browserid), website=self.site)

        try:
            vote.save()
        except:
            messages.error(request, 'You have already voted for this site.')
            return

    def get(self, request, site):
        self.handle_site(request, site)
        return super(DemandView, self).get(request)

    def post(self, request, site=None):
        self.handle_site(request, request.POST.get('site'))
        return super(DemandView, self).get(request)

