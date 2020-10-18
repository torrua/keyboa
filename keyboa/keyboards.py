# -*- coding:utf-8 -*-
"""
This module contains all the necessary functions for
creating complex and functional inline keyboards.
"""

from collections.abc import Iterable
from typing import Union, List, Optional, Tuple

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# pylint: disable=R0913

InlineButtonData = Union[str, int, tuple, dict, InlineKeyboardButton]

button_text_types = (str, int)
ButtonText = Union[button_text_types]

callback_data_types = (str, int, type(None))
CallbackDataMarker = Union[callback_data_types]

# structureless sequence of InlineButtonData objects
FlatSequence = List[InlineButtonData]

# structured sequence of InlineButtonData objects
StructuredSequence = List[Union[FlatSequence, InlineButtonData]]

# unified type that allows you to use any available data types for the keyboard
BlockItems = Union[StructuredSequence, InlineButtonData]

MAXIMUM_ITEMS_IN_LINE = 8
MINIMUM_ITEMS_IN_LINE = 1
DEFAULT_ITEMS_IN_LINE = MINIMUM_ITEMS_IN_LINE
AUTO_ALIGNMENT_RANGE = range(3, 6)


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
    total_items_number = sum(
        len(row) if isinstance(row, (list, tuple, set)) else 1 for row in items)

    if keyboard:
        keyboard_items = keyboard.__dict__['keyboard']
        current_keyboard_items_number = sum(len(row) for row in keyboard_items)
        expecting_items_number = total_items_number + current_keyboard_items_number
    else:
        expecting_items_number = total_items_number

    items_in_keyboard_allowed_range = range(1, 101)  # Telegram limitation
    if expecting_items_number not in items_in_keyboard_allowed_range:
        value_error_message_keyboard = \
            "Telegram Bot API limit exceeded: The keyboard should have " \
            "from 1 to %s buttons at all. Your total amount is %s."
        raise ValueError(value_error_message_keyboard %
                         (items_in_keyboard_allowed_range[-1], expecting_items_number))

    items_in_line_allowed_range = range(1, 9)  # Telegram limitation
    if items_in_row is not None and items_in_row not in items_in_line_allowed_range:
        value_error_message_line = \
            "Telegram Bot API limit exceeded: " \
            "The keyboard line should have from 1 to %s buttons. You entered %s."

        raise ValueError(value_error_message_line %
                         (items_in_line_allowed_range[-1], items_in_row))


def button_maker(
        button_data: InlineButtonData,
        front_marker: CallbackDataMarker = None,
        back_marker: CallbackDataMarker = None,
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

    if front_marker is None:
        front_marker = ""

    if back_marker is None:
        back_marker = ""

    if not isinstance(front_marker, callback_data_types):
        type_error_message = \
            "Marker could not have %s type. Only %s allowed." \
            % (type(front_marker), CallbackDataMarker)
        raise TypeError(type_error_message)

    if not isinstance(back_marker, callback_data_types):
        type_error_message = \
            "Marker could not have %s type. Only %s allowed." \
            % (type(back_marker), CallbackDataMarker)
        raise TypeError(type_error_message)

    if isinstance(button_data, InlineKeyboardButton):
        return button_data

    if isinstance(button_data, (str, int)):
        text = str(button_data)
        callback = str(button_data) if copy_text_to_callback else ""

    elif isinstance(button_data, tuple):
        text, callback = _button_data_extractor(button_data)

    elif isinstance(button_data, dict):
        if button_data.get("text", None):
            return InlineKeyboardButton(**button_data)
        if len(button_data.keys()) == 1:
            text, callback = _button_data_extractor(next(iter(button_data.items())))
        else:
            value_type_error = \
                "Cannot convert dictionary to InlineButtonData object. " \
                "You passed more than one item, but did not add 'text' key." % button_data
            raise ValueError(value_type_error)

    else:
        type_error_message = \
            "Cannot create %s from %s. Please use %s instead.\n" \
            "Probably you specified 'auto_alignment' or 'items_in_line' " \
            "parameter for StructuredSequence." \
            % (InlineKeyboardButton, type(button_data), InlineButtonData)
        raise TypeError(type_error_message)

    if not text:
        raise ValueError("Button text cannot be empty.")

    callback_data = "%s%s%s" % (front_marker, callback, back_marker)

    if not callback_data:
        raise ValueError("The callback data cannot be empty.")

    if len(callback_data.encode()) > 64:
        size_error_message = "The callback data cannot be more than " \
                             "64 bytes for one button. Your size is %s" \
                             % len(callback_data.encode())
        raise ValueError(size_error_message)

    prepared_button = {"text": text, "callback_data": callback_data if callback_data else None}

    return InlineKeyboardButton(**prepared_button)


def _button_data_extractor(button_data: Union[tuple, dict]) -> (str, str):
    """
    This small function extract button text and callback from passed object and make a check.
    :param button_data: Union[tuple, dict] - as a part of InlineButtonData type.
    :return: str, str - button text and callback
    """
    raw_text = button_data[0]
    if not isinstance(raw_text, button_text_types):
        type_error_message = "Button text cannot be %s. Only %s allowed." \
                             % (type(raw_text), ButtonText)
        raise TypeError(type_error_message)
    text = str(raw_text)
    raw_callback = button_data[1]

    if not isinstance(raw_callback, callback_data_types):
        type_error_message = "Callback cannot be %s. Only %s allowed." \
                             % (type(raw_callback), callback_data_types)
        raise TypeError(type_error_message)
    callback = str(raw_callback)
    return text, callback


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

    if items and not isinstance(items, list):
        items = [items, ]

    items = items[slice_start:slice_stop:slice_step] if items else items

    _keyboa_pre_check(items=items, items_in_row=items_in_row, keyboard=keyboard)

    if items_in_row or auto_alignment:

        if auto_alignment:

            if isinstance(auto_alignment, bool):
                alignment_range = AUTO_ALIGNMENT_RANGE
            elif not (isinstance(auto_alignment, Iterable)
                      and all(map(lambda s: isinstance(s, int), auto_alignment))):
                type_error_message = \
                    "The auto_alignment variable has not a proper type. " \
                    "Only Iterable of integers or boolean type allowed.\n" \
                    "You may define it as 'True' to use AUTO_ALIGNMENT_RANGE."
                raise TypeError(type_error_message)
            elif max(auto_alignment) > MAXIMUM_ITEMS_IN_LINE \
                    or min(auto_alignment) < MINIMUM_ITEMS_IN_LINE:
                value_error_message = \
                    "The auto_alignment's item values should be between " \
                    "%s and %s. You entered: %s\n" \
                    "You may define it as 'True' to use AUTO_ALIGNMENT_RANGE." \
                    % (MINIMUM_ITEMS_IN_LINE, MAXIMUM_ITEMS_IN_LINE, auto_alignment)
                raise ValueError(value_error_message)
            else:
                alignment_range = auto_alignment

            if reverse_alignment_range:
                alignment_range = reversed(alignment_range)

            for divider in alignment_range:
                if not len(items) % divider:
                    items_in_row = divider
                    break

        items_in_row = items_in_row if items_in_row else DEFAULT_ITEMS_IN_LINE

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

    return keyboa_maker(data)
