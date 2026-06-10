from django import template

register = template.Library()


@register.simple_tag
def locale_pageurl(page):
    return page.specific.get_url() or "/"
