from django import template

register = template.Library()

@register.filter(name='range_from')
def range_from(num, arg):
    num = int(num)
    arg = arg.split(',')
    fr = int(arg[0])
    by = int(arg[1]) if len(arg) > 1 else 1
    return range(fr, fr + num * by, by)
