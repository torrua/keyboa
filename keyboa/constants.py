# -*- coding:utf-8 -*-
"""
Module for constants and types
"""

from typing import Union, List

from telebot.types import InlineKeyboardButton

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

MAXIMUM_ITEMS_IN_KEYBOARD = 100
MAXIMUM_ITEMS_IN_LINE = 8
MINIMUM_ITEMS_IN_LINE = 1
DEFAULT_ITEMS_IN_LINE = MINIMUM_ITEMS_IN_LINE
AUTO_ALIGNMENT_RANGE = range(3, 6)
MAXIMUM_CBD_LENGTH = 64
