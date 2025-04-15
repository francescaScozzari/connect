"""Explainable Artificial Intelligence text processor."""

import string

import ftfy


def process_text(text: str) -> str:
    """
    Fix given text list encoding.

    :param text_list: Text to process
    :return: Processed text.
    """
    text = text.lower()
    translator_digits = str.maketrans("", "", string.digits)
    text = text.translate(translator_digits).lower()
    text = ftfy.fix_text(text)
    text = " ".join(text.split())
    return text
