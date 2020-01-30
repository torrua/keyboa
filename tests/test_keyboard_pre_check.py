# -*- coding:utf-8 -*-
"""
Test for keyboard_pre_check() function
"""
import os
import sys

sys.path.insert(0, f"{os.path.dirname(os.path.abspath(__file__))}/../")

import pytest
from keyboa.keyboards import _keyboard_pre_check
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def test_acceptable_number_of_passed_elements():
    """

    :return:
    """
    assert _keyboard_pre_check(items=list(range(0, 99))) is None

    with pytest.raises(Exception) as _:
        _keyboard_pre_check(items=list(range(0, 101)))


@pytest.mark.parametrize("number_in_line", (0, 9))
def test_unacceptable_number_in_line(number_in_line):
    """

    :param number_in_line:
    :return:
    """
    with pytest.raises(Exception) as _:
        _keyboard_pre_check(
            items=list(range(0, 50)),
            items_in_line=number_in_line, )


@pytest.mark.parametrize("number_in_line", (1, 8, None))
def test_acceptable_number_in_line(number_in_line):
    """

    :param number_in_line:
    :return:
    """
    assert _keyboard_pre_check(
        items=list(range(0, 50)),
        items_in_line=number_in_line, ) is None


def test_count_items_with_existing_keyboard():
    """

    :return:
    """
    existing_keyboard = InlineKeyboardMarkup().row(
        *[InlineKeyboardButton(
            **{"text": item, "callback_data": item})
            for item in list(range(0, 8))]
    )
    with pytest.raises(Exception) as _:
        _keyboard_pre_check(
            items=list(range(0, 99)),
            keyboard=existing_keyboard, )


def test_unacceptable_add_to_keyboard_variable_type():
    """

    :return:
    """
    with pytest.raises(Exception) as _:
        _keyboard_pre_check(
            items=list(range(0, 99)),
            keyboard="not a keyboard", )
