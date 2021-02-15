# -*- coding:utf-8 -*-
"""
Module with functions for work with button data and button text
"""

from telebot.types import InlineKeyboardButton

from keyboa.constants import InlineButtonData, button_text_types, ButtonText


def get_text(button_data: tuple) -> str:
    """
    :param button_data:
    :return:
    """
    raw_text = button_data[0]
    if not isinstance(raw_text, button_text_types):
        type_error_message = "Button text cannot be %s. Only %s allowed." \
                             % (type(raw_text), ButtonText)
        raise TypeError(type_error_message)
    text = str(raw_text)
    if not text:
        raise ValueError("Button text cannot be empty.")
    return text


def get_verified_button_tuple(
        button_data: InlineButtonData,
        copy_text_to_callback: bool) -> tuple:
    """
    :param button_data:
    :param copy_text_to_callback:
    :return:
    """
    if not isinstance(button_data, (tuple, dict, str, int)):
        type_error_message = \
            "Cannot create %s from %s. Please use %s instead.\n" \
            "Probably you specified 'auto_alignment' or 'items_in_line' " \
            "parameter for StructuredSequence." \
            % (InlineKeyboardButton, type(button_data), InlineButtonData)
        raise TypeError(type_error_message)

    btn_tuple = get_raw_tuple_from_button_data(button_data, copy_text_to_callback)

    if len(btn_tuple) == 1 or btn_tuple[1] is None:
        btn_tuple = btn_tuple[0], btn_tuple[0] if copy_text_to_callback else str()
    return btn_tuple


def get_raw_tuple_from_button_data(button_data, copy_text_to_callback):
    """
    :param button_data:
    :param copy_text_to_callback:
    :return:
    """
    if isinstance(button_data, (str, int)):
        btn_tuple = button_data, button_data if copy_text_to_callback else str()

    elif isinstance(button_data, dict):
        if len(button_data.keys()) != 1:
            value_type_error = \
                "Cannot convert dictionary to InlineButtonData object. " \
                "You passed more than one item, but did not add 'text' key."
            raise ValueError(value_type_error)

        btn_tuple = next(iter(button_data.items()))
    else:
        btn_tuple = button_data
    return btn_tuple
