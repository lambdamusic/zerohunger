from django import template
from django.urls import reverse
import re


# from config.linkeddata.triplestore import *

register = template.Library()


@register.filter
def replace(value, arg):
    """
    Replacing filter
    Use `{{ "aaa"|replace:"a|b" }}`
    """
    if len(arg.split('|')) != 2:
        return value

    what, to = arg.split('|')
    return value.replace(what, to)




@register.filter
def url_safe(value):
    """
    Turn spaces into dashes and lowercase.
    """
    if value:
        return value.replace(" ", "-").lower()






@register.filter()
def powerup(x):
    """
    Make sizes more interesting for force directed graph 
    """
    try:
        xmax = 500
        xmin = 1
        out = (x - xmin) / (xmax - xmin) * 100
        print(x, "becomes", out)
        return out
    except:
        return s


@register.filter(name='trim_unwanted_words')
def trim_unwanted_words(s):
    """
    Remove 'abstract' keyword from text
    """
    try:
        if s.startswith("Abstract"):
            return s[8:]
    except:
        return s

