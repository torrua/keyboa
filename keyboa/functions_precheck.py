# -*- coding:utf-8 -*-
"""
Module with functions for keyboard precheck
"""
from telebot.types import InlineKeyboardMarkup

from keyboa.constants import BlockItems, MAXIMUM_ITEMS_IN_KEYBOARD, \
    MINIMUM_ITEMS_IN_LINE, MAXIMUM_ITEMS_IN_LINE


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

    check_keyboard_type(keyboard)

    items_in_keyboard = get_total_items_number(items, keyboard)

    check_keyboard_items_limits(items_in_keyboard, items_in_row)


def check_keyboard_type(keyboard):
    """
    :param keyboard:
    :return:
    """
    if keyboard and not isinstance(keyboard, InlineKeyboardMarkup):
        type_error_message = \
            "Keyboard to which the new items will be added " \
            "should have InlineKeyboardMarkup type. Now it is a %s" % type(keyboard)
        raise TypeError(type_error_message)


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
