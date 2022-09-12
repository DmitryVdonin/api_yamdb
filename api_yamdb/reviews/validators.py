import datetime

from django.core.exceptions import ValidationError


def validate_year(value):
    now_year = datetime.datetime.now().year
    if not (now_year >= value):
        raise ValidationError(
            'Проверьте год выпуска произведения!')

    return value
