from django import template

register = template.Library()

@register.filter(name='add_attributes')
def add_attributes(field, attrs):

    # atributos que vamos a setear al elemento
    set_attrs = {}

    # dividimos cada atributo con su valor 'attr:value'
    list_attrs = attrs.split(',')

    for i in list_attrs:
        k, v = i.split(':')
        set_attrs[k] = v

    return field.as_widget(attrs=set_attrs)
