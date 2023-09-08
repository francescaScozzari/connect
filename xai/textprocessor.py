"""Explainable Artificial Intelligence text processor."""

import string

import ftfy


def process_text(text_list: list[str]) -> list[str]:
    """
    Fix given text list encoding.

    :param text_list: Text to process
    :return: Processed text.
    """
    processed_sentences = []
    for text in text_list:
        text = text.lower()
        translator_digits = str.maketrans("", "", string.digits)
        text = text.translate(translator_digits).lower()
        text = ftfy.fix_text(text)
        text = " ".join(text.split())
        processed_sentences.append(text)
    return processed_sentences
