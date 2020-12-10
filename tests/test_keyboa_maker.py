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
    assert result.to_dict()["inline_keyboard"] == []


def test_pass_string_with_copy_to_callback():
    """

    :return:
    """
    result = keyboa_maker(
        items="Text", copy_text_to_callback=True)
    assert isinstance(result, InlineKeyboardMarkup)
    assert result.to_dict()["inline_keyboard"] == [[{'callback_data': 'Text', 'text': 'Text'}]]


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
    assert result.to_dict()["inline_keyboard"] == [[
        {'text': 'text', 'callback_data': 'callback_data'}]]


def test_pass_one_item_dict_with_text_field():
    """

    :return:
    """
    result = keyboa_maker(
        items={"text": "text", "callback_data": "callback_data"})
    assert isinstance(result, InlineKeyboardMarkup)
    assert result.to_dict()["inline_keyboard"] == [[
       {'text': 'text', 'callback_data': 'callback_data'}]]


def test_pass_one_item_dict_without_text_field():
    """

    :return:
    """
    result = keyboa_maker(
        items={"word": "callback_data", })
    assert isinstance(result, InlineKeyboardMarkup)
    assert result.to_dict()["inline_keyboard"] == [[
       {'text': 'word', 'callback_data': 'callback_data'}]]


def test_pass_multi_item_dict_without_text_field():
    """

    :return:
    """
    with pytest.raises(ValueError) as _:
        wrong_dict = {"word_1": "callback_data_1", "word_2": "callback_data_1", }
        keyboa_maker(items=wrong_dict)


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
    assert len(result.to_dict()["inline_keyboard"]) == stop
    assert result.to_dict()["inline_keyboard"][0][0]["callback_data"] == "FRONT_%s" % start


def test_pass_structure():
    """

    :return:
    """
    result = keyboa_maker(
        items=[list(range(4)), list(range(2, 5)), "string", {"t": "cbd"}],
        front_marker="STRUCTURE_",
        copy_text_to_callback=True,
    )

    assert isinstance(result, InlineKeyboardMarkup)
    assert len(result.to_dict()["inline_keyboard"]) == 4
    assert result.to_dict()["inline_keyboard"][0][0]["callback_data"] == "STRUCTURE_0"
    assert result.to_dict()["inline_keyboard"][1][0]["callback_data"] == "STRUCTURE_2"
    assert result.to_dict()["inline_keyboard"][2][0]["callback_data"] == "STRUCTURE_string"
    assert result.to_dict()["inline_keyboard"][3][0]["callback_data"] == "STRUCTURE_cbd"


def test_auto_keyboa_maker_alignment():
    result = keyboa_maker(
        items=list(range(0, 36)),
        copy_text_to_callback=True,
        auto_alignment=True)
    assert isinstance(result, InlineKeyboardMarkup)

    with pytest.raises(TypeError) as _:
        keyboa_maker(
            items=list(range(0, 36)),
            copy_text_to_callback=True,
            auto_alignment="alignment")

    with pytest.raises(ValueError) as _:
        keyboa_maker(
            items=list(range(0, 36)),
            copy_text_to_callback=True,
            auto_alignment=[-1, 0])

    with pytest.raises(ValueError) as _:
        keyboa_maker(
            items=list(range(0, 36)),
            copy_text_to_callback=True,
            auto_alignment=[10, 11, 12])

    result = keyboa_maker(
            items=list(range(0, 36)),
            copy_text_to_callback=True,
            auto_alignment=[3, 4, 6, ])
    assert isinstance(result, InlineKeyboardMarkup)

    result = keyboa_maker(
            items=list(range(0, 36)),
            copy_text_to_callback=True,
            auto_alignment=True,
            reverse_alignment_range=True)
    assert isinstance(result, InlineKeyboardMarkup)

    result = keyboa_maker(
            items=list(range(0, 36)),
            copy_text_to_callback=True,
            auto_alignment=[3, 4, 6, ],
            reverse_alignment_range=True)
    assert isinstance(result, InlineKeyboardMarkup)

    result = keyboa_maker(
            items=list(range(0, 36)),
            copy_text_to_callback=True,
            auto_alignment=[5, 7, ],
            reverse_alignment_range=True)
    assert isinstance(result, InlineKeyboardMarkup)


def test_auto_keyboa_maker_items_in_row():
    result = keyboa_maker(
        items=list(range(0, 36)),
        copy_text_to_callback=True,
        items_in_row=6)
    assert isinstance(result, InlineKeyboardMarkup)
