from demandapp.forms import BrowserIDForm

def browserid_form(request):
    return {'browserid_form': BrowserIDForm(), 'browserid': request.browserid}
