from django.utils.functional import SimpleLazyObject


def get_browserid(request):
    if not hasattr(request, '_browserid'):
        request._browserid = request.session.get('browserid', None)
    return request._browserid

class BrowserIDMiddleware(object):
    def process_request(self, request):
        assert hasattr(request, 'session')
        request.browserid = SimpleLazyObject(lambda: get_browserid(request))

