# -*- coding:utf-8 -*-
"""
This module contains all the necessary functions for
creating complex and functional inline keyboards.
"""


from typing import Union, Optional, Tuple
from telebot.types import InlineKeyboardMarkup

from keyboa.base import Base
from keyboa.button import Button
from keyboa.constants import (
    DEFAULT_ITEMS_IN_LINE,
    AUTO_ALIGNMENT_RANGE,
)


class Keyboa(Base):
    """Default Keyboa class"""

    def __call__(
        self,
        slice_: slice = slice(None, None, None),
    ) -> InlineKeyboardMarkup:
        """
        :return:
        """
        return self.slice(slice_)

    def slice(
        self,
        slice_: slice = slice(None, None, None),
    ) -> InlineKeyboardMarkup:
        """
        :return:
        """
        self._items_sliced = self.items[slice_]

        keyboard = (
            self._generated_keyboa
            if self.items_in_row or self.alignment
            else self._preformatted_keyboa
        )
        self._items_sliced = None
        return keyboard

    @property
    def keyboard(self) -> InlineKeyboardMarkup:
        """
        :return:
        """
        return self.slice()

    @property
    def _calculated_items_in_row(self) -> Optional[int]:
        """
        :return:
        """

        items_in_row = None

        for divider in self.alignment_range:
            if not len(self._items_sliced) % divider:
                items_in_row = divider
                break

        return items_in_row

    @property
    def _verified_items_in_row(self) -> int:
        """
        :return:
        """
        items_in_row = self.items_in_row
        if self.alignment:
            items_in_row = self._calculated_items_in_row

        if not items_in_row:
            items_in_row = DEFAULT_ITEMS_IN_LINE
        return items_in_row

    @property
    def alignment_range(self):
        """
        :return:
        """

        alignment_range = (
            AUTO_ALIGNMENT_RANGE if isinstance(self.alignment, bool) else self.alignment
        )
        return reversed(alignment_range) if self.alignment_reverse else alignment_range

    @property
    def _preformatted_keyboa(self) -> InlineKeyboardMarkup:
        """
        :return:
        """
        self.verify_preformatted_items()
        keyboard = InlineKeyboardMarkup()
        for row in self._items_sliced:
            buttons = self.convert_items_to_buttons(row)
            keyboard.row(*buttons)
        return keyboard

    def verify_preformatted_items(self) -> None:
        """
        Check that every row in kb is a list
        :return:
        """
        for index, item in enumerate(self._items_sliced):
            if not isinstance(item, list):
                self._items_sliced[index] = [
                    item,
                ]

    def convert_items_to_buttons(self, items) -> list:
        """
        :param items:
        :return:
        """
        return [
            Button(
                button_data=item,
                front_marker=self.front_marker,
                back_marker=self.back_marker,
                copy_text_to_callback=self.copy_text_to_callback,
            ).generate()
            for item in items
        ]

    @property
    def _generated_keyboa(self) -> InlineKeyboardMarkup:
        """
        :return:
        """
        keyboard = InlineKeyboardMarkup()
        items_in_row = self._verified_items_in_row
        rows_in_keyboard = len(self._items_sliced) // items_in_row
        buttons = self.convert_items_to_buttons(self._items_sliced)

        for _row in range(rows_in_keyboard):
            keyboard.row(*[buttons.pop(0) for _button in range(items_in_row)])

        if buttons:
            keyboard.row(*buttons)

        return keyboard

    @staticmethod
    def merge_keyboards_data(keyboards):
        """
        :param keyboards:
        :return:
        """
        data = []
        for keyboard in keyboards:
            if keyboard is None:
                continue

            if not isinstance(keyboard, InlineKeyboardMarkup):
                type_error_message = (
                    "Keyboard cannot be %s. Only InlineKeyboardMarkup allowed."
                    % type(keyboard)
                )
                raise TypeError(type_error_message)
            data.extend(keyboard.keyboard)
        return data

    @classmethod
    def combine(
        cls,
        keyboards: Optional[
            Union[Tuple[InlineKeyboardMarkup, ...], InlineKeyboardMarkup]
        ] = None,
    ) -> InlineKeyboardMarkup:
        """
        This function combines multiple InlineKeyboardMarkup objects into one.

        :param keyboards: Sequence of InlineKeyboardMarkup objects.
            Also could be presented as a standalone InlineKeyboardMarkup.

        :return: InlineKeyboardMarkup
        """

        if keyboards is None:
            return InlineKeyboardMarkup()

        if isinstance(keyboards, InlineKeyboardMarkup):
            keyboards = (keyboards,)

        for keyboard in keyboards:
            cls.is_keyboard_proper_type(keyboard)

        data = cls.merge_keyboards_data(keyboards)

        return cls(items=data).keyboard
