from django.core.exceptions import ValidationError


def validate_youtube_link(value):
    """
        Описываю свой валидатор для проверки того, не приложил ли полльзователть какую-то ссылку,
        кроме как на ютуб
    """

    if 'youtube.com' not in value:
        raise ValidationError('Разрешены только ссылки на YouTube.')
    return value
