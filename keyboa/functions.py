# -*- coding:utf-8 -*-
"""
Module for small service functions
"""

from typing import Optional, Iterable

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboa.constants import InlineButtonData, button_text_types, \
    ButtonText, callback_data_types, CallbackDataMarker, \
    BlockItems, MAXIMUM_ITEMS_IN_KEYBOARD, MAXIMUM_ITEMS_IN_LINE, \
    MINIMUM_ITEMS_IN_LINE, AUTO_ALIGNMENT_RANGE, MAXIMUM_CBD_LENGTH


def _keyboa_pre_check(
        items: BlockItems = None,
        items_in_row: int = None,
        keyboard: InlineKeyboardMarkup = None) -> None:
    """
    This function checks whether the keyboard parameters are beyond Telegram limits or not.

    :param items: InlineRowItems - Sequence of elements with optional structure,
        where each top-level item will be a row with one or several buttons.

    :param items_in_row: int - Desired number of buttons in one row. Should be from 1 to 8.
        Optional. The default value is None.

    :param keyboard: InlineKeyboardMarkup object to which we will attach the list items.
        We need to count the existing buttons so as not to go beyond the general limits.
        Optional. The default value is None.

    :return: None if everything is okay.

    Covered by tests.
    """

    if items is None:
        return

    if items and not isinstance(items, list):
        items = [items, ]

    if keyboard and not isinstance(keyboard, InlineKeyboardMarkup):
        type_error_message = \
            "Keyboard to which the new items will be added " \
            "should have InlineKeyboardMarkup type. Now it is a %s" % type(keyboard)
        raise TypeError(type_error_message)

    # We need to count existing buttons too if we passed keyboard object to the function
    items_in_keyboard = get_total_items_number(items, keyboard)
    check_keyboard_items_limits(items_in_keyboard, items_in_row)


def check_keyboard_items_limits(items_in_keyboard: int, items_in_row: int) -> None:
    """
    :param items_in_keyboard:
    :param items_in_row:
    :return:
    """

    if items_in_keyboard > MAXIMUM_ITEMS_IN_KEYBOARD:
        value_error_message_keyboard = \
            "Telegram Bot API limit exceeded: The keyboard should have " \
            "from 1 to %s buttons at all. Your total amount is %s."
        raise ValueError(value_error_message_keyboard %
                         (MAXIMUM_ITEMS_IN_KEYBOARD, items_in_keyboard))

    if items_in_row is not None and \
            (MINIMUM_ITEMS_IN_LINE > items_in_row or items_in_row > MAXIMUM_ITEMS_IN_LINE):
        value_error_message_line = \
            "Telegram Bot API limit exceeded: " \
            "The keyboard line should have from 1 to %s buttons. You entered %s."
        raise ValueError(value_error_message_line %
                         (MAXIMUM_ITEMS_IN_LINE, items_in_row))


def get_total_items_number(items, keyboard) -> int:
    """
    :param items:
    :param keyboard:
    :return:
    """
    total_items_number = sum(
        len(row) if isinstance(row, (list, tuple, set)) else 1 for row in items)

    if not keyboard:
        return total_items_number

    keyboard_items = keyboard.__dict__['keyboard']
    current_keyboard_items_number = sum(len(row) for row in keyboard_items)
    return total_items_number + current_keyboard_items_number


def get_callback_data(
        raw_callback: CallbackDataMarker,
        front_marker: CallbackDataMarker = str(),
        back_marker: CallbackDataMarker = str()) -> str:
    """
    :param raw_callback:
    :param front_marker:
    :param back_marker:
    :return:
    """
    if front_marker is None:
        front_marker = str()
    if back_marker is None:
        back_marker = str()
    for marker in (front_marker, back_marker):
        if not isinstance(marker, callback_data_types):
            type_error_message = \
                "Marker could not have %s type. Only %s allowed." \
                % (type(marker), CallbackDataMarker)
            raise TypeError(type_error_message)
    callback_data = "%s%s%s" % (front_marker, raw_callback, back_marker)

    if not callback_data:
        raise ValueError("The callback data cannot be empty.")

    if len(callback_data.encode()) > MAXIMUM_CBD_LENGTH:
        size_error_message = "The callback data cannot be more than " \
                             "64 bytes for one button. Your size is %s" \
                             % len(callback_data.encode())
        raise ValueError(size_error_message)

    return callback_data


def get_callback(button_data: tuple) -> str:
    """
    :param button_data:
    :return:
    """
    callback = button_data[1]
    if not isinstance(callback, callback_data_types):
        type_error_message = "Callback cannot be %s. Only %s allowed." \
                             % (type(callback), callback_data_types)
        raise TypeError(type_error_message)
    return callback


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


def get_button_tuple(button_data: InlineButtonData, copy_text_to_callback: bool) -> tuple:
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

    if len(btn_tuple) == 1 or btn_tuple[1] is None:
        btn_tuple = btn_tuple[0], btn_tuple[0] if copy_text_to_callback else str()
    return btn_tuple


def calculate_items_in_row(items, auto_alignment, reverse_alignment_range) -> Optional[int]:
    """
    :param items:
    :param auto_alignment:
    :param reverse_alignment_range:
    :return:
    """

    items_in_row = None
    alignment_range = get_alignment_range(auto_alignment)

    if reverse_alignment_range:
        alignment_range = reversed(alignment_range)

    for divider in alignment_range:
        if not len(items) % divider:
            items_in_row = divider
            break

    return items_in_row


def get_alignment_range(auto_alignment):
    """
    :param auto_alignment:
    :return:
    """

    if isinstance(auto_alignment, bool):
        return AUTO_ALIGNMENT_RANGE

    if not (isinstance(auto_alignment, Iterable)
            and all(map(lambda s: isinstance(s, int), auto_alignment))):
        type_error_message = \
            "The auto_alignment variable has not a proper type. " \
            "Only Iterable of integers or boolean type allowed.\n" \
            "You may define it as 'True' to use AUTO_ALIGNMENT_RANGE."
        raise TypeError(type_error_message)

    if max(auto_alignment) > MAXIMUM_ITEMS_IN_LINE \
            or min(auto_alignment) < MINIMUM_ITEMS_IN_LINE:
        value_error_message = \
            "The auto_alignment's item values should be between " \
            "%s and %s. You entered: %s\n" \
            "You may define it as 'True' to use AUTO_ALIGNMENT_RANGE." \
            % (MINIMUM_ITEMS_IN_LINE, MAXIMUM_ITEMS_IN_LINE, auto_alignment)
        raise ValueError(value_error_message)

    return auto_alignment
