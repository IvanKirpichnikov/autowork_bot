from fluent_compiler.bundle import FluentBundle
from fluentogram import FluentTranslator, TranslatorHub


def create_translator_hub() -> TranslatorHub:
    """
    Create TranslatorHub
    
    :return: fluentogram.TranslatorHub
    
    """
    return TranslatorHub(
        dict(
            ru=('ru',)
        ),
        [
            FluentTranslator(
                'ru', FluentBundle.from_files(
                    'ru_RU',
                    filenames=[
                        'resources/locales/ru/txt.ftl'
                    ]
                )
            )
        ],
        root_locale='ru'
    )
