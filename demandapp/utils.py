from urlparse import urlparse
import re

def normalise_site(site):
    o = urlparse(site)

    if o.hostname:
        domain = o.hostname
    elif '/' in o.path:
        domain = o.path.split('/')[0]
    else:
        domain = o.path

    domain = re.sub(r'^(www|secure|get)\.', '', str(domain))

    if not (domain and '.' in domain):
        return

    return domain
 
