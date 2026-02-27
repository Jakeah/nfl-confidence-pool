from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary"""
    if dictionary and key in dictionary:
        return dictionary[key]
    return None

@register.filter
def get_attr(obj, attr):
    """Get an attribute from an object or dict"""
    if isinstance(obj, dict):
        return obj.get(attr)
    return getattr(obj, attr, None)
