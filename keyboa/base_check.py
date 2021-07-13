# -*- coding:utf-8 -*-
"""
This module contains all checks for Keyboa Base class parameters
"""
# pylint: disable = C0116

from typing import Iterable

from telebot.types import InlineKeyboardMarkup

from keyboa.constants import (
    MAXIMUM_ITEMS_IN_KEYBOARD,
    MINIMUM_ITEMS_IN_LINE,
    MAXIMUM_ITEMS_IN_LINE,
)


class BaseCheck:
    """
    This class contains all checks for Keyboa Base class parameters
    """

    @staticmethod
    def is_all_items_in_limits(items) -> None:
        items_in_keyboard = sum(
            len(row) if isinstance(row, list) else 1 for row in items
        )
        if items_in_keyboard > MAXIMUM_ITEMS_IN_KEYBOARD:
            value_error_message_keyboard = (
                "Telegram Bot API limit exceeded: The keyboard should have "
                "from 1 to %s buttons at all. Your total amount is %s."
            )
            raise ValueError(
                value_error_message_keyboard
                % (MAXIMUM_ITEMS_IN_KEYBOARD, items_in_keyboard)
            )

    @classmethod
    def is_row_in_limits(cls, items) -> None:
        if all(isinstance(line, list) for line in items):
            for line in items:
                cls.is_items_in_row_limits(len(line))

    @staticmethod
    def is_items_in_row_limits(items_in_row) -> None:
        if items_in_row is not None and (
            MINIMUM_ITEMS_IN_LINE > items_in_row or items_in_row > MAXIMUM_ITEMS_IN_LINE
        ):
            value_error_message_line = (
                "Telegram Bot API limit exceeded: "
                "The keyboard line should have from 1 to %s buttons. You entered %s."
            )
            raise ValueError(
                value_error_message_line % (MAXIMUM_ITEMS_IN_LINE, items_in_row)
            )

    @staticmethod
    def is_alignment_in_limits(auto_alignment) -> None:
        """
        :param auto_alignment:
        :return:
        """
        if (
            max(auto_alignment) > MAXIMUM_ITEMS_IN_LINE
            or min(auto_alignment) < MINIMUM_ITEMS_IN_LINE
        ):
            value_error_message = (
                "The auto_alignment's item values should be between "
                "%s and %s. You entered: %s\n"
                "You may define it as 'True' to use AUTO_ALIGNMENT_RANGE."
                % (MINIMUM_ITEMS_IN_LINE, MAXIMUM_ITEMS_IN_LINE, auto_alignment)
            )
            raise ValueError(value_error_message)

    @staticmethod
    def is_alignment_iterable(auto_alignment) -> None:
        """
        :param auto_alignment:
        :return:
        """
        if not (
            isinstance(auto_alignment, Iterable)
            and all(map(lambda s: isinstance(s, int), auto_alignment))
        ):
            type_error_message = (
                "The auto_alignment variable has not a proper type. "
                "Only Iterable of integers or boolean type allowed.\n"
                "You may define it as 'True' to use AUTO_ALIGNMENT_RANGE."
            )
            raise TypeError(type_error_message)

    @staticmethod
    def is_keyboard_proper_type(keyboard) -> None:
        if keyboard and not isinstance(keyboard, InlineKeyboardMarkup):
            type_error_message = (
                "Keyboard to which the new items will be added "
                "should have InlineKeyboardMarkup type. Now it is a %s" % type(keyboard)
            )
            raise TypeError(type_error_message)
