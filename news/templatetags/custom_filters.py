from django import template
from news.resources import BAD_WORDS

register = template.Library()

@register.filter()
def nofoobar(value):
    for word in BAD_WORDS:
        value = value.replace(word, word[0:1] + ('*' * (len(word) - 1)))
    return value

