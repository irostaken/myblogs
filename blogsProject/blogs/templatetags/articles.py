import datetime

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def getRequest(request):
    article_type = request.GET.get("article_type")
    date = request.GET.get("date")
    payload = request.path
    if date:
        payload += "?date=" + date + "&"
    if article_type:
        payload += "?article_type=" + article_type + "&"
    return mark_safe(payload)


@register.simple_tag
def dateformat(pub_date):
    pub_date = pub_date.strftime("%Y-%m-%d %X")
    return pub_date


@register.simple_tag
def dateformat2(pub_date):
    pub_date = pub_date.strftime("%Y-%m-%d")
    return pub_date


@register.simple_tag
@mark_safe
def fieldFormat(field):
    add_class = ' class="form-control">'
    return str(field).replace(">", add_class, 1)
