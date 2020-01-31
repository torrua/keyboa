# -*- coding:utf-8 -*-
"""
This module contains all the necessary functions for
creating complex and functional inline keyboards.
"""

from typing import Union, List, Optional, Tuple, Dict

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# pylint: disable=R0913

InlineButtonData = Union[str, int, tuple, dict, InlineKeyboardButton]

ButtonText = Union[str, int]
CallbackDataMarker = Optional[Union[str, int]]

# structureless sequence of InlineButtonData objects
FlatSequence = List[InlineButtonData]

# structured sequence of InlineButtonData objects
StructuredSequence = List[Union[FlatSequence, InlineButtonData]]

# unified type that allows you to use any available data types for the keyboard
BlockItems = Union[StructuredSequence, InlineButtonData]

DEFAULT_ITEMS_IN_LINE = 1
AUTO_ALIGNMENT_RANGE = range(3, 6)


def _keyboard_pre_check(
        items: BlockItems = None,
        items_in_line: int = None,
        keyboard: InlineKeyboardMarkup = None) -> None:
    """
    This function checks whether the keyboard parameters are beyond Telegram limits or not.

    :param items: InlineRowItems - Sequence of elements with optional structure,
        where each top-level item will be a row with one or several buttons.

    :param items_in_line: int - Desired number of buttons in one row. Should be from 1 to 8.
        Optional. The default value is None.

    :param keyboard: InlineKeyboardMarkup object to which we will attach the list items.
        We need to count the existing buttons so as not to go beyond the general limits.
        Optional. The default value is None.

    :return: None if everything is okay.

    Covered by tests.
    """

    if items is None:
        return

    if items and not isinstance(items, List):
        items = [items, ]

    if keyboard and not isinstance(keyboard, InlineKeyboardMarkup):
        type_error_message = \
            "Keyboard to which the new items will be added " \
            "should have InlineKeyboardMarkup type. Now it is a %s" % type(keyboard)
        raise TypeError(type_error_message)

    # We need to count existing buttons too if we passed keyboard object to the function
    if keyboard:
        keyboard_items = keyboard.__dict__['keyboard']
        current_keyboard_items_number = sum([len(row) for row in keyboard_items])
        expecting_items_number = len(items) + current_keyboard_items_number
    else:
        expecting_items_number = len(items)

    value_error_message_keyboard = \
        "Telegram Bot API limit exceeded: The keyboard should have " \
        "from 1 to %s buttons at all. Your total amount is %s."
    value_error_message_line = \
        "Telegram Bot API limit exceeded: " \
        "The keyboard line should have from 1 to %s buttons. You entered %s."

    items_in_keyboard_allowed_range = range(1, 101)  # Telegram limitation
    if expecting_items_number not in items_in_keyboard_allowed_range:
        raise ValueError(value_error_message_keyboard %
                         (items_in_keyboard_allowed_range[-1], expecting_items_number))

    items_in_line_allowed_range = range(1, 9)  # Telegram limitation
    if items_in_line is not None and items_in_line not in items_in_line_allowed_range:
        raise ValueError(value_error_message_line %
                         (items_in_line_allowed_range[-1], items_in_line))


def button_maker(
        button_data: InlineButtonData,
        front_marker: CallbackDataMarker = None,
        back_marker: CallbackDataMarker = None,
        copy_text_to_callback: bool = True,
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
        Optional. The default value is True.

    :return: InlineKeyboardButton

    Covered by tests.
    """

    if front_marker is None:
        front_marker = ""

    if back_marker is None:
        back_marker = ""

    if not isinstance(front_marker, CallbackDataMarker.__args__):
        type_error_message = \
            "Marker could not have %s type. Only %s allowed." \
            % (type(front_marker), CallbackDataMarker)
        raise TypeError(type_error_message)

    if not isinstance(back_marker, CallbackDataMarker.__args__):
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
        elif len(button_data.keys()) == 1:
            text, callback = _button_data_extractor(next(iter(button_data.items())))
        else:
            value_type_error = \
                "Cannot convert dictionary to InlineButtonData object. " \
                "You passed more than one item, but did not add 'text' key." % button_data
            raise ValueError(value_type_error)

    else:
        type_error_message = "Cannot create %s from %s. Please use %s instead." \
            % (InlineKeyboardButton, type(button_data), InlineButtonData)
        raise TypeError(type_error_message)

    if not text:
        raise ValueError("Button text cannot be empty.")

    callback_data = "%s%s%s" % (front_marker, callback, back_marker)

    if not callback_data:
        raise ValueError("The callback data cannot be empty.")

    prepared_button = {"text": text, "callback_data": callback_data if callback_data else None}

    return InlineKeyboardButton(**prepared_button)


def _button_data_extractor(button_data: Union[tuple, dict]) -> (str, str):
    """
    This small function extract button text and callback from passed object and make a check.
    :param button_data: Union[tuple, dict] - as a part of InlineButtonData type.
    :return: str, str - button text and callback
    """
    raw_text = button_data[0]
    if not isinstance(raw_text, ButtonText.__args__):
        type_error_message = "Button text cannot be %s. Only %s allowed." \
            % (type(raw_text), ButtonText)
        raise TypeError(type_error_message)
    text = str(raw_text)
    raw_callback = button_data[1]
    if not isinstance(raw_callback, CallbackDataMarker.__args__):
        type_error_message = "Callback cannot be %s. Only %s allowed." \
            % (type(raw_callback), CallbackDataMarker)
        raise TypeError(type_error_message)
    callback = str(raw_callback)
    return text, callback


def body_maker(
        items: FlatSequence,
        front_marker: CallbackDataMarker = None,
        back_marker: CallbackDataMarker = None,

        items_in_line: int = DEFAULT_ITEMS_IN_LINE,
        auto_alignment: bool = False,
        slice_start: int = None,
        slice_stop: int = None,
        slice_step: int = None,

        copy_text_to_callback: bool = False,
        add_to_keyboard: InlineKeyboardMarkup = None,
) -> InlineKeyboardMarkup:
    """
    This function creates an InlineKeyboardMarkup from a
    sequence of InlineButtonData elements (FlatSequence).
    Additionally, you can set the number of buttons in each
    row using variable "items_in_line".
    Also you can make a slice of sequence with
    ["slice_start":"slice_stop":"slice_step"] variables.

    :param items: InlineRowItems - Iterable sequence of InlineButtonData elements.

    :param front_marker: CallbackDataMarker - Front part of callback data,
        which is common for all buttons.
        Optional. The default value is empty string.

    :param back_marker: CallbackDataMarker - Back part of callback data,
        which is common for all buttons.
        Optional. The default value is empty string.

    :param items_in_line: The number of buttons in one keyboard line
        must be from one to eight due to the Telegram Bot API limitation.
        Optional. The default value is 1.

    :param auto_alignment: Bool - If enabled, will try to split all items into equal rows.
        This enabled option replaces variable "items_in_line".
        But if a suitable divisor cannot be found, function
        will use the value of variable "items_in_line".
        Optional. The default value is False.

    :param slice_start: int - Refers to the index of the element
        which is used as a start of the slice.
        Optional. The default value is None.

    :param slice_stop: int - Refers to the index of the element
        we should stop just before to finish slice.
        Optional. The default value is None.

    :param slice_step: int - Allows you to take each
        nth-element within a [start:stop] range.
        Optional. The default value is None.

    :param copy_text_to_callback: If enabled and button_data is a string or integer,
        function will copy button text to callback data (and add markers if they exist).
        Optional. The default value is False.

    :param add_to_keyboard: InlineKeyboardMarkup -
        Keyboard to which the specified items will be added.
        Optional. The default value is None.

    :return: InlineKeyboardMarkup
    """

    keyboard = add_to_keyboard if add_to_keyboard else InlineKeyboardMarkup()

    items = items[slice_start:slice_stop:slice_step]

    if items is None:
        return keyboard

    if auto_alignment:
        for divider in AUTO_ALIGNMENT_RANGE:
            if not len(items) % divider:
                items_in_line = divider
                break

    _keyboard_pre_check(items=items, items_in_line=items_in_line, keyboard=keyboard)

    rows_in_keyboard = (len(items) // items_in_line)
    buttons = [button_maker(
        button_data=b_item,
        front_marker=front_marker,
        back_marker=back_marker,
        copy_text_to_callback=copy_text_to_callback,
    ) for b_item in items]

    for _row in range(0, rows_in_keyboard):
        keyboard.row(*[buttons.pop(0) for _button in range(0, items_in_line)])
    keyboard.row(*buttons)

    return keyboard


def block_maker(
        items: BlockItems = None,
        front_marker: CallbackDataMarker = None,
        back_marker: CallbackDataMarker = None,
        copy_text_to_callback: bool = False,
        add_to_keyboard: InlineKeyboardMarkup = None,
) -> InlineKeyboardMarkup:
    """
    This function creates an InlineKeyboardMarkup
    from a sequence of BlockItems elements.

    :param items: InlineKeyboardItems -
    Iterable collection of InlineButtonData elements.
        Optional. The default value is None.

    :param front_marker: CallbackDataMarker -
    Callback data, which is common for all buttons.
        Optional. The default value is None.

    :param back_marker: CallbackDataMarker -
    Callback data, which is common for all buttons.
        Optional. The default value is empty string.

    :param copy_text_to_callback: If enabled and button_data is a string or integer,
        function will copy button text to callback data (and add markers if they exist).
        Optional. The default value is False.

    :param add_to_keyboard: InlineKeyboardMarkup -
        Keyboard to which the specified items will be added.

    :return: InlineKeyboardMarkup
    """

    keyboard = add_to_keyboard if add_to_keyboard else InlineKeyboardMarkup()

    if items is None:
        return keyboard

    if items and not isinstance(items, List):
        items = [items, ]

    _keyboard_pre_check(items=items, keyboard=keyboard)

    for index, item in enumerate(items):
        if not isinstance(item, list):
            items[index] = [item, ]

    for row in items:
        keyboard.row(*[button_maker(
            button_data=item,
            front_marker=front_marker,
            back_marker=back_marker,
            copy_text_to_callback=copy_text_to_callback
        ) for item in row])
    return keyboard


def keyboard_combiner(
        keyboards: Union[Tuple, Dict],
        add_to_keyboard: InlineKeyboardMarkup = None,
) -> InlineKeyboardMarkup:
    """
    This function combines multiple data sets into one InlineKeyboardMarkup object.
    Each set must be passed in a dictionary whose keys
    are the names of variables for makers functions.

    :param keyboards: Sequence of dictionaries with prepared data.
        Also could be presented as a standalone dictionary.

    :param add_to_keyboard: InlineKeyboardMarkup -
        Keyboard to which the specified keyboards will be added.

    :return: InlineKeyboardMarkup
    """

    keyboard = add_to_keyboard if add_to_keyboard else InlineKeyboardMarkup()

    if isinstance(keyboards, dict):
        keyboards = (keyboards,)

    for data in keyboards:
        if not isinstance(data, dict):
            type_error_message = \
                "Cannot create %s from %s. Please use a dict to pass data instead." \
                % (InlineKeyboardMarkup, type(data))
            raise TypeError(type_error_message)

        body_trigger = any([
            data.get("items_in_line", None),
            data.get("auto_alignment", None),
            data.get("slice_start", None),
            data.get("slice_stop", None),
            data.get("slice_step", None),
        ])

        if body_trigger:
            keyboard = body_maker(**data, add_to_keyboard=keyboard, )
        else:
            keyboard = block_maker(**data, add_to_keyboard=keyboard, )

    return keyboard
