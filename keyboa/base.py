# -*- coding:utf-8 -*-
"""
This module contains basic class with initial Keyboa data.
"""
# pylint: disable = C0116

from typing import Union, Iterable, Optional
from telebot.types import InlineKeyboardMarkup
from keyboa.button import Button
from keyboa.constants import (
    BlockItems,
    CallbackDataMarker,
    MAXIMUM_ITEMS_IN_KEYBOARD,
    MINIMUM_ITEMS_IN_LINE,
    MAXIMUM_ITEMS_IN_LINE,
)


class Check:
    """
    This class contains all checks for Keyboa Base class values
    """

    @staticmethod
    def is_all_items_in_limits(items) -> None:
        items_in_keyboard = sum(
            len(row) if isinstance(row, (list, tuple, set)) else 1 for row in items
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


class Base(Check):  # pylint: disable = R0902
    """
    Base initial class for Keyboa
    """

    def __init__(  # pylint: disable = R0913
        self,
        items: BlockItems,
        items_in_row: int = None,
        front_marker: CallbackDataMarker = str(),
        back_marker: CallbackDataMarker = str(),
        copy_text_to_callback: Optional[bool] = None,
        alignment: Union[bool, Iterable] = None,
        alignment_reverse_range: Optional[bool] = None,
    ):
        self._items = None
        self.items = items

        self._items_in_row = None
        self.items_in_row = items_in_row

        self._front_marker = str()
        self.front_marker = front_marker

        self._back_marker = str()
        self.back_marker = back_marker

        self._copy_text_to_callback = None
        self.copy_text_to_callback = copy_text_to_callback

        self._alignment = None
        self.alignment = alignment

        self._alignment_reverse_range = None
        self.alignment_reverse_range = alignment_reverse_range

        self._items_sliced = None

    @property
    def items(self) -> BlockItems:
        return self._items

    @items.setter
    def items(self, items_value) -> None:
        if items_value is None or not items_value:
            raise ValueError("Items should not be None")
        if not isinstance(items_value, list):
            items_value = [
                items_value,
            ]

        self.is_all_items_in_limits(items_value)
        self.is_row_in_limits(items_value)
        self._items = items_value

    @property
    def items_in_row(self) -> int:
        return self._items_in_row

    @items_in_row.setter
    def items_in_row(self, items_in_row_value) -> None:
        self.is_items_in_row_limits(items_in_row_value)
        self._items_in_row = items_in_row_value

    @property
    def front_marker(self) -> CallbackDataMarker:
        return self._front_marker

    @front_marker.setter
    def front_marker(self, front_marker_value) -> None:
        Button.get_checked_marker(front_marker_value)
        self._front_marker = front_marker_value

    @property
    def back_marker(self) -> CallbackDataMarker:
        return self._back_marker

    @back_marker.setter
    def back_marker(self, back_marker_value) -> None:
        Button.get_checked_marker(back_marker_value)
        self._back_marker = back_marker_value

    @property
    def copy_text_to_callback(self) -> bool:
        return self._copy_text_to_callback

    @copy_text_to_callback.setter
    def copy_text_to_callback(self, copy_text_to_callback_value) -> None:
        if not isinstance(copy_text_to_callback_value, (bool, type(None))):
            raise TypeError(
                "'copy_text_to_callback' should have only bool or none type"
            )
        self._copy_text_to_callback = copy_text_to_callback_value

    @property
    def alignment(self) -> Union[bool, Iterable]:

        return self._alignment

    @alignment.setter
    def alignment(self, alignment_value) -> None:
        if alignment_value is None or isinstance(alignment_value, bool):
            self._alignment = alignment_value
            return
        self.is_alignment_iterable(alignment_value)
        self.is_alignment_in_limits(alignment_value)
        self._alignment = alignment_value

    @property
    def alignment_reverse_range(self) -> bool:
        return self._alignment_reverse_range

    @alignment_reverse_range.setter
    def alignment_reverse_range(self, alignment_reverse_range_value) -> None:
        self._alignment_reverse_range = alignment_reverse_range_value
