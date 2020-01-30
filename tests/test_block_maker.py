# -*- coding:utf-8 -*-
"""
Test for block_maker() function
"""
import os
import sys

sys.path.insert(0, f"{os.path.dirname(os.path.abspath(__file__))}/../")

import pytest
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboa.keyboards import block_maker


def test_pass_none():
    """

    :return:
    """
    result = block_maker()
    assert isinstance(result, InlineKeyboardMarkup)
    assert result.__dict__["keyboard"] == []


def test_pass_string_with_copy_to_callback():
    """

    :return:
    """
    result = block_maker(
        items="Text", copy_text_to_callback=True)
    assert isinstance(result, InlineKeyboardMarkup)
    assert result.__dict__["keyboard"] == [[{'callback_data': 'Text', 'text': 'Text'}]]


def test_pass_string_without_copy_to_callback():
    """

    :return:
    """
    with pytest.raises(Exception) as _:
        assert isinstance(block_maker(items="Text"), InlineKeyboardMarkup)


def test_pass_one_button():
    """

    :return:
    """
    result = block_maker(
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
    result = block_maker(
        items=list(range(start, stop)),
        front_marker="FRONT_",
        copy_text_to_callback=True,
    )
    assert isinstance(result, InlineKeyboardMarkup)
    assert len(result.__dict__["keyboard"]) == stop
    assert result.__dict__["keyboard"][0][0]["callback_data"] == f"FRONT_{start}"


def test_pass_structure():
    """

    :return:
    """
    result = block_maker(
        items=[list(range(0, 4)), list(range(2, 5)), "string"],
        front_marker="STRUCTURE_",
        copy_text_to_callback=True)
    assert isinstance(result, InlineKeyboardMarkup)
    assert len(result.__dict__["keyboard"]) == 3
    assert result.__dict__["keyboard"][0][0]["callback_data"] == f"STRUCTURE_{0}"
    assert result.__dict__["keyboard"][1][0]["callback_data"] == f"STRUCTURE_{2}"
    assert result.__dict__["keyboard"][2][0]["callback_data"] == f"STRUCTURE_string"
