import re
from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def get_setting_var(name):
    return getattr(settings, name)
