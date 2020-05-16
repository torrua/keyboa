# -*- coding:utf-8 -*-
"""
Test for keyboa_maker() function
"""
import os
import sys

sys.path.insert(0, "%s/../" % os.path.dirname(os.path.abspath(__file__)))

import pytest
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboa.keyboards import keyboa_maker


def test_pass_none():
    """

    :return:
    """
    result = keyboa_maker()
    assert isinstance(result, InlineKeyboardMarkup)
    assert result.__dict__["keyboard"] == []


def test_pass_string_with_copy_to_callback():
    """

    :return:
    """
    result = keyboa_maker(
        items="Text", copy_text_to_callback=True)
    assert isinstance(result, InlineKeyboardMarkup)
    assert result.__dict__["keyboard"] == [[{'callback_data': 'Text', 'text': 'Text'}]]


def test_pass_string_without_copy_to_callback():
    """

    :return:
    """
    with pytest.raises(Exception) as _:
        assert isinstance(keyboa_maker(items="Text"), InlineKeyboardMarkup)


def test_pass_one_button():
    """

    :return:
    """
    result = keyboa_maker(
        items=InlineKeyboardButton(
            **{"text": "text", "callback_data": "callback_data"}))
    assert isinstance(result, InlineKeyboardMarkup)
    assert result.__dict__["keyboard"] == [[
        {'text': 'text', 'callback_data': 'callback_data'}]]


def test_pass_one_row():
    """

    :return:
    """
    start = 0
    stop = 8
    result = keyboa_maker(
        items=list(range(start, stop)),
        front_marker="FRONT_",
        copy_text_to_callback=True,
    )
    assert isinstance(result, InlineKeyboardMarkup)
    assert len(result.__dict__["keyboard"]) == stop
    assert result.__dict__["keyboard"][0][0]["callback_data"] == "FRONT_%s" % start


def test_pass_structure():
    """

    :return:
    """
    result = keyboa_maker(
        items=[list(range(4)), list(range(2, 5)), "string"],
        front_marker="STRUCTURE_",
        copy_text_to_callback=True,
    )

    assert isinstance(result, InlineKeyboardMarkup)
    assert len(result.__dict__["keyboard"]) == 3
    assert result.__dict__["keyboard"][0][0]["callback_data"] == "STRUCTURE_0"
    assert result.__dict__["keyboard"][1][0]["callback_data"] == "STRUCTURE_2"
    assert result.__dict__["keyboard"][2][0]["callback_data"] == "STRUCTURE_string"
