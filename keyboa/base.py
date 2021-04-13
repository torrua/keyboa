# -*- coding:utf-8 -*-
"""
This module contains basic class with initial Keyboa data.
"""
# pylint: disable = C0116

from typing import Union, Iterable, Optional
from keyboa.button import Button
from keyboa.base_check import BaseCheck
from keyboa.constants import (
    BlockItems,
    CallbackDataMarker,
)


class Base(BaseCheck):  # pylint: disable = R0902
    """
    Base initial class for Keyboa
    """

    def __init__(  # pylint: disable = R0913
        self,
        items: BlockItems,
        items_in_row: int = None,
        front_marker: CallbackDataMarker = str(),
        back_marker: CallbackDataMarker = str(),
        copy_text_to_callback: Optional[bool] = True,
        alignment: Union[bool, Iterable] = None,
        alignment_reverse: Optional[bool] = None,
    ):
        self._items = None
        self.items = items

        self._items_in_row = None
        self.items_in_row = items_in_row

        self._front_marker = str()
        self.front_marker = front_marker

        self._back_marker = str()
        self.back_marker = back_marker

        self._copy_text_to_callback = True
        self.copy_text_to_callback = copy_text_to_callback

        self._alignment = None
        self.alignment = alignment

        self._alignment_reverse = None
        self.alignment_reverse = alignment_reverse

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
    def alignment_reverse(self) -> bool:
        return self._alignment_reverse

    @alignment_reverse.setter
    def alignment_reverse(self, alignment_reverse_value) -> None:
        self._alignment_reverse = alignment_reverse_value
