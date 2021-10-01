# -*- coding:utf-8 -*-
"""
This module contains all the necessary functions for
creating buttons for telegram inline keyboards.
"""
from dataclasses import dataclass
from typing import Optional
from telebot.types import InlineKeyboardButton
from keyboa.button_check import ButtonCheck
from keyboa.constants import (
    InlineButtonData,
    CallbackDataMarker,
    callback_data_types,
    button_text_types,
    ButtonText,
)


@dataclass
class Button(ButtonCheck):
    """Default Button class
    :button_data: InlineButtonData - an object from which the button will be created:
    • If string or an integer, it will be used for both text and callback.
    • If tuple, the zero element [0] will be the text, and the first [1] will be the callback.
    • If dictionary, there are two options:
        > if there is no "text" key in dictionary and only one key exists,
            the key will be the text, and the value will be the callback.
            In this case, no verification of the dictionary's contents is performed!
        > if "text" key exists, function passes the whole dictionary to InlineKeyboardButton,
            where dictionary's keys represent object's parameters
            and dictionary's values represent parameters' values accordingly.
        In all other cases ValueError will be called.

    :front_marker: CallbackDataMarker - a string to be added to the left side of callback.
        Optional. The default value is None.

    :back_marker: CallbackDataMarker - a string to be added to the right side of callback.
        Optional. The default value is None.

    :copy_text_to_callback: If enabled and button_data is a string or integer,
        function will copy button text to callback data (and add markers if they exist).
        Optional. The default value is False."""

    button_data: InlineButtonData = None
    front_marker: CallbackDataMarker = str()
    back_marker: CallbackDataMarker = str()
    copy_text_to_callback: Optional[bool] = None

    def __call__(self, *args, **kwargs):
        return self.generate()

    def generate(self) -> InlineKeyboardButton:
        """
        This function creates an InlineKeyboardButton object from various data types,
        such as str, int, tuple, dict.
        :return: InlineKeyboardButton

        Covered by tests.
        """

        if isinstance(self.button_data, InlineKeyboardButton):
            return self.button_data

        if isinstance(self.button_data, dict) and self.button_data.get("text"):
            return InlineKeyboardButton(**self.button_data)

        self.is_auto_copy_text_to_callback()

        button_tuple = self._verified_button_tuple
        text = self.get_text(button_tuple)
        raw_callback = self.get_callback(button_tuple)
        callback_data = self.get_callback_data(
            raw_callback, self.front_marker, self.back_marker
        )

        prepared_button = {"text": text, "callback_data": callback_data}

        return InlineKeyboardButton(**prepared_button)

    @property
    def button(self):
        return self.generate()

    def is_auto_copy_text_to_callback(self):
        """
        Enable copy_text_to_callback parameter if button_data is str or int
        :return:
        """
        if self.copy_text_to_callback is None and isinstance(
            self.button_data, (str, int)
        ):
            self.copy_text_to_callback = True

    @classmethod
    def get_callback(cls, button_data: tuple) -> str:
        """
        :param button_data:
        :return:
        """
        callback = button_data[1]
        cls.is_callback_proper_type(callback)
        return callback

    @classmethod
    def get_callback_data(
        cls,
        raw_callback: CallbackDataMarker,
        front_marker: CallbackDataMarker = str(),
        back_marker: CallbackDataMarker = str(),
    ) -> str:
        """
        :param raw_callback:
        :param front_marker:
        :param back_marker:
        :return:
        """

        front_marker = cls.get_checked_marker(front_marker)
        back_marker = cls.get_checked_marker(back_marker)

        callback_data = "%s%s%s" % (front_marker, raw_callback, back_marker)

        if not callback_data:
            raise ValueError("The callback data cannot be empty.")

        cls.is_callback_data_in_limits(callback_data)

        return callback_data

    @staticmethod
    def get_checked_marker(marker: CallbackDataMarker) -> CallbackDataMarker:
        """
        :param marker:
        :return:
        """
        if marker is None:
            marker = str()

        if not isinstance(marker, callback_data_types):
            type_error_message = "Marker could not have %s type. Only %s allowed." % (
                type(marker),
                CallbackDataMarker,
            )
            raise TypeError(type_error_message)

        return marker

    @staticmethod
    def get_text(button_data: tuple) -> str:
        """
        :param button_data:
        :return:
        """
        raw_text = button_data[0]
        if not isinstance(raw_text, button_text_types):
            type_error_message = "Button text cannot be %s. Only %s allowed." % (
                type(raw_text),
                ButtonText,
            )
            raise TypeError(type_error_message)
        text = str(raw_text)
        if not text:
            raise ValueError("Button text cannot be empty.")
        return text

    @property
    def _verified_button_tuple(self) -> tuple:
        """
        :return:
        """
        self.is_button_data_proper_type(self.button_data)

        btn_tuple = self._raw_tuple_from_button_data

        if len(btn_tuple) == 1 or btn_tuple[1] is None:
            btn_tuple = (
                btn_tuple[0],
                btn_tuple[0] if self.copy_text_to_callback else str(),
            )
        return btn_tuple

    @property
    def _raw_tuple_from_button_data(self) -> tuple:
        """
        :return:
        """
        if isinstance(self.button_data, (str, int)):
            btn_tuple = (
                self.button_data,
                self.button_data if self.copy_text_to_callback else str(),
            )

        elif isinstance(self.button_data, dict):
            if len(self.button_data.keys()) != 1:
                value_type_error = (
                    "Cannot convert dictionary to InlineButtonData object. "
                    "You passed more than one item, but did not add 'text' key."
                )
                raise ValueError(value_type_error)

            btn_tuple = next(iter(self.button_data.items()))
        else:
            btn_tuple = self.button_data
        return btn_tuple
