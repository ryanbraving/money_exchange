from django import template

register = template.Library()

EN_TO_FA_DIGITS = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')

@register.filter
def persian_digits(value):
    if value is None:
        return ''
    return str(value).translate(EN_TO_FA_DIGITS)