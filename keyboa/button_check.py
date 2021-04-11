# -*- coding:utf-8 -*-
"""
This module contains all checks for Keyboa Button class parameters
"""
# pylint: disable = C0116

from keyboa.constants import (
    InlineKeyboardButton,
    InlineButtonData,
    callback_data_types,
    MAXIMUM_CBD_LENGTH,
)


class ButtonCheck:
    """
    This class contains all checks for Keyboa Button class parameters
    """

    @staticmethod
    def is_button_data_proper_type(button_data) -> None:
        if not isinstance(button_data, (tuple, dict, str, int)):
            type_error_message = (
                "Cannot create %s from %s. Please use %s instead.\n"
                "Probably you specified 'auto_alignment' or 'items_in_line' "
                "parameter for StructuredSequence."
                % (InlineKeyboardButton, type(button_data), InlineButtonData)
            )
            raise TypeError(type_error_message)

    @staticmethod
    def is_callback_proper_type(callback) -> None:
        if not isinstance(callback, callback_data_types):
            type_error_message = "Callback cannot be %s. Only %s allowed." % (
                type(callback),
                callback_data_types,
            )
            raise TypeError(type_error_message)

    @staticmethod
    def is_callback_data_in_limits(callback_data) -> None:
        if len(callback_data.encode()) > MAXIMUM_CBD_LENGTH:
            size_error_message = (
                "The callback data cannot be more than "
                "64 bytes for one button. Your size is %s" % len(callback_data.encode())
            )
            raise ValueError(size_error_message)
