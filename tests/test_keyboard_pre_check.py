# -*- coding:utf-8 -*-
"""
Test for keyboard_pre_check() function
"""
import os
import sys

sys.path.insert(0, "%s/../" % os.path.dirname(os.path.abspath(__file__)))

import pytest
from keyboa.functions import _keyboa_pre_check
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def test_precheck_with_nothing():
    assert _keyboa_pre_check(items=None) is None


def test_precheck_with_no_list():
    assert _keyboa_pre_check(items=1) is None


def test_acceptable_number_of_passed_elements():
    """

    :return:
    """
    assert _keyboa_pre_check(items=list(range(99))) is None

    with pytest.raises(Exception) as _:
        _keyboa_pre_check(items=list(range(101)))


def test_acceptable_number_of_nested_elements():
    """

    :return:
    """
    range_105 = [list(range(0, 7)) for i in range(0, 15)]

    with pytest.raises(Exception) as _:
        _keyboa_pre_check(items=range_105)


@pytest.mark.parametrize("number_in_line", (0, 9))
def test_unacceptable_number_in_line(number_in_line):
    """

    :param number_in_line:
    :return:
    """
    with pytest.raises(Exception) as _:
        _keyboa_pre_check(items=list(range(50)), items_in_row=number_in_line)


@pytest.mark.parametrize("number_in_line", (1, 8, None))
def test_acceptable_number_in_line(number_in_line):
    """

    :param number_in_line:
    :return:
    """
    assert (
        _keyboa_pre_check(items=list(range(50)), items_in_row=number_in_line)
        is None
    )


def test_count_items_with_existing_keyboard():
    """

    :return:
    """
    existing_keyboard = InlineKeyboardMarkup().row(
        *[
            InlineKeyboardButton(**{"text": item, "callback_data": item})
            for item in list(range(8))
        ]
    )

    with pytest.raises(Exception) as _:
        _keyboa_pre_check(items=list(range(99)), keyboard=existing_keyboard)


def test_unacceptable_add_to_keyboard_variable_type():
    """

    :return:
    """
    with pytest.raises(Exception) as _:
        _keyboa_pre_check(items=list(range(99)), keyboard="not a keyboard")
