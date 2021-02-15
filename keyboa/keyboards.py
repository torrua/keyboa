# -*- coding:utf-8 -*-
"""
This module contains all the necessary functions for
creating complex and functional inline keyboards.
"""
# pylint: disable=R0913

from collections.abc import Iterable
from typing import Union, Optional, Tuple

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboa.constants import InlineButtonData, CallbackDataMarker, \
    BlockItems, DEFAULT_ITEMS_IN_LINE
from keyboa.functions_alignment import calculate_items_in_row
from keyboa.functions_button_data import get_text, get_verified_button_tuple
from keyboa.functions_callback import get_callback_data, get_callback
from keyboa.functions_precheck import _keyboa_pre_check


def button_maker(
        button_data: InlineButtonData,
        front_marker: CallbackDataMarker = str(),
        back_marker: CallbackDataMarker = str(),
        copy_text_to_callback: bool = False,
) -> InlineKeyboardButton:
    """
    This function creates an InlineKeyboardButton object from various data types,
    such as str, int, tuple, dict.

    :param button_data: InlineButtonData - an object from which the button will be created:
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

    :param front_marker: CallbackDataMarker - a string to be added to the left side of callback.
        Optional. The default value is None.

    :param back_marker: CallbackDataMarker - a string to be added to the right side of callback.
        Optional. The default value is None.

    :param copy_text_to_callback: If enabled and button_data is a string or integer,
        function will copy button text to callback data (and add markers if they exist).
        Optional. The default value is False.

    :return: InlineKeyboardButton

    Covered by tests.
    """

    if isinstance(button_data, InlineKeyboardButton):
        return button_data

    if isinstance(button_data, dict) and button_data.get("text"):
        return InlineKeyboardButton(**button_data)

    button_tuple = get_verified_button_tuple(button_data, copy_text_to_callback)

    text = get_text(button_tuple)
    raw_callback = get_callback(button_tuple)
    callback_data = get_callback_data(raw_callback, front_marker, back_marker)

    prepared_button = {"text": text, "callback_data": callback_data}

    return InlineKeyboardButton(**prepared_button)


def keyboa_maker(
        items: BlockItems = None,
        front_marker: CallbackDataMarker = None,
        back_marker: CallbackDataMarker = None,

        items_in_row: int = None,
        auto_alignment: Union[bool, Iterable] = False,
        reverse_alignment_range: bool = False,
        slice_start: int = None,
        slice_stop: int = None,
        slice_step: int = None,

        copy_text_to_callback: bool = False,
        add_to_keyboard: InlineKeyboardMarkup = None,
) -> InlineKeyboardMarkup:
    """
    :param items:
    :param front_marker:
    :param back_marker:
    :param items_in_row:
    :param auto_alignment:
    :param reverse_alignment_range:
    :param slice_start:
    :param slice_stop:
    :param slice_step:
    :param copy_text_to_callback:
    :param add_to_keyboard:
    :return:
    """
    keyboard = add_to_keyboard if add_to_keyboard else InlineKeyboardMarkup()

    if items is None:
        return keyboard

    items = get_verified_items(items, slice_start, slice_stop, slice_step)

    _keyboa_pre_check(items=items, items_in_row=items_in_row, keyboard=keyboard)

    if items_in_row or auto_alignment:
        return get_generated_keyboard(
            items, front_marker, back_marker, items_in_row, auto_alignment,
            reverse_alignment_range, copy_text_to_callback, keyboard)

    return get_preformatted_keyboard(
        items, front_marker, back_marker,
        copy_text_to_callback, keyboard)


def get_verified_items(items, slice_start, slice_stop, slice_step):
    """
    :param items:
    :param slice_start:
    :param slice_stop:
    :param slice_step:
    :return:
    """

    if items and not isinstance(items, list):
        items = [items, ]

    return items[slice_start:slice_stop:slice_step] if items else items


def get_preformatted_keyboard(
        items, front_marker, back_marker,
        copy_text_to_callback, keyboard):
    """
    :param items:
    :param front_marker:
    :param back_marker:
    :param copy_text_to_callback:
    :param keyboard:
    :return:
    """
    for index, item in enumerate(items):
        if not isinstance(item, list):
            items[index] = [item, ]
    for row in items:
        buttons = [button_maker(
            button_data=item,
            front_marker=front_marker,
            back_marker=back_marker,
            copy_text_to_callback=copy_text_to_callback
        ) for item in row]
        keyboard.row(*buttons)
    return keyboard


def get_generated_keyboard(
        items, front_marker, back_marker, items_in_row,
        auto_alignment, reverse_alignment_range,
        copy_text_to_callback, keyboard):
    """
    :param items:
    :param front_marker:
    :param back_marker:
    :param items_in_row:
    :param auto_alignment:
    :param reverse_alignment_range:
    :param copy_text_to_callback:
    :param keyboard:
    :return:
    """

    items_in_row = get_verified_items_in_row(
        items, items_in_row, auto_alignment, reverse_alignment_range)

    rows_in_keyboard = (len(items) // items_in_row)

    buttons = [button_maker(
        button_data=item,
        front_marker=front_marker,
        back_marker=back_marker,
        copy_text_to_callback=copy_text_to_callback,
    ) for item in items]

    for _row in range(rows_in_keyboard):
        keyboard.row(*[buttons.pop(0) for _button in range(items_in_row)])
    keyboard.row(*buttons)

    return keyboard


def get_verified_items_in_row(
        items, items_in_row,
        auto_alignment, reverse_alignment_range):
    """
    :param items:
    :param items_in_row:
    :param auto_alignment:
    :param reverse_alignment_range:
    :return:
    """
    if auto_alignment:
        items_in_row = calculate_items_in_row(
            items, auto_alignment, reverse_alignment_range)
    if not items_in_row:
        items_in_row = DEFAULT_ITEMS_IN_LINE
    return items_in_row


def keyboa_combiner(
        keyboards: Optional[Union[Tuple[InlineKeyboardMarkup, ...], InlineKeyboardMarkup]] = None
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
        keyboards = (keyboards, )

    data = merge_keyboards_data(keyboards)

    return keyboa_maker(data)


def merge_keyboards_data(keyboards):
    data = []
    for keyboard in keyboards:
        if keyboard is None:
            continue

        if not isinstance(keyboard, InlineKeyboardMarkup):
            type_error_message = \
                "Keyboard element cannot be %s. Only InlineKeyboardMarkup allowed." \
                % type(keyboard)
            raise TypeError(type_error_message)

        data.extend(keyboard.keyboard)
    return data
