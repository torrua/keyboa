# -*- coding:utf-8 -*-
"""
Module with functions for work with callback
"""

from keyboa.constants import CallbackDataMarker, \
    MAXIMUM_CBD_LENGTH, callback_data_types


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

    front_marker = get_checked_marker(front_marker)
    back_marker = get_checked_marker(back_marker)

    callback_data = "%s%s%s" % (front_marker, raw_callback, back_marker)

    if not callback_data:
        raise ValueError("The callback data cannot be empty.")

    if len(callback_data.encode()) > MAXIMUM_CBD_LENGTH:
        size_error_message = "The callback data cannot be more than " \
                             "64 bytes for one button. Your size is %s" \
                             % len(callback_data.encode())
        raise ValueError(size_error_message)

    return callback_data


def get_checked_marker(marker: CallbackDataMarker) -> CallbackDataMarker:
    """
    :param marker:
    :return:
    """

    if marker is None:
        marker = str()

    if not isinstance(marker, callback_data_types):
        type_error_message = \
            "Marker could not have %s type. Only %s allowed." \
            % (type(marker), CallbackDataMarker)
        raise TypeError(type_error_message)

    return marker


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
