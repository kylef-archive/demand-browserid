from django import template

from demandapp.models import Site, Vote

register = template.Library()

class QuerySetNode(template.Node):
    @classmethod
    def handle_token(cls, parser, token, qs):
        tokens = token.contents.split()

        if len(tokens) < 2 or tokens[1] != 'as':
            raise template.TemplateSyntaxError(
                    'Queryset nodes must be given a variable name')

        return cls(tokens[2], qs)

    def __init__(self, varname, queryset):
        self.varname = varname
        self.queryset = queryset

    def render(self, context):
        context[self.varname] = self.queryset
        return ''

@register.tag
def get_latest_sites(parser, token):
    return QuerySetNode.handle_token(parser, token, Site.objects.new())

@register.tag
def get_latest_votes(parser, token):
    return QuerySetNode.handle_token(parser, token,
            Vote.objects.order_by('-date')[:5])

