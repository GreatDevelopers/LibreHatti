from django import template

register = template.Library()

@register.filter(name='addcss')


def addcss(field, css):
    """
    This view adds css to the field argument passed
    """
    return field.as_widget(attrs={'class':css})
