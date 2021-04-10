# -*- coding:utf-8 -*-
"""
Test for button_maker() function
"""
import os
import sys

sys.path.insert(0, "%s/../" % os.path.dirname(os.path.abspath(__file__)))

import pytest
from keyboa.keyboard import Keyboa
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def test_keyboards_is_none():
    assert isinstance(Keyboa.combine(), InlineKeyboardMarkup)
    assert Keyboa.combine().__dict__ == InlineKeyboardMarkup().__dict__


def test_keyboards_is_single_keyboard():
    kb = Keyboa(items=list(range(0, 4)), copy_text_to_callback=True).keyboard
    result = Keyboa.combine(keyboards=kb)

    assert isinstance(result, InlineKeyboardMarkup)
    assert result.__dict__ == kb.__dict__


def test_keyboards_is_multi_keyboards():
    kb_1 = Keyboa(items=list(range(0, 4)), copy_text_to_callback=True).keyboard
    kb_2 = Keyboa(items=list(range(10, 15)), copy_text_to_callback=True).keyboard

    result = Keyboa.combine(keyboards=(kb_1, kb_2))
    assert isinstance(result, InlineKeyboardMarkup)

    result = Keyboa.combine(keyboards=(kb_1, None, kb_2))
    assert isinstance(result, InlineKeyboardMarkup)

    with pytest.raises(TypeError) as _:
        Keyboa.combine(keyboards=(kb_1, 1))


def test_not_keyboard_for_merge():
    """

    :return:
    """
    with pytest.raises(TypeError) as _:
        Keyboa.merge_keyboards_data(keyboards="not_a_keyboard")


def test_merge_two_keyboard_into_one_out_of_limits():
    """

    :return:
    """
    k1 = Keyboa(items=list(range(60)), copy_text_to_callback=True)
    k2 = Keyboa(items=list(range(60)), copy_text_to_callback=True)

    with pytest.raises(ValueError) as _:
        Keyboa.combine(keyboards=(k1.keyboard, k2.keyboard))


def test_pass_string_with_copy_to_callback():
    """

    :return:
    """
    result = Keyboa(items="Text", copy_text_to_callback=True).keyboard
    assert isinstance(result, InlineKeyboardMarkup)
    assert result.to_dict()["inline_keyboard"] == [
        [{"callback_data": "Text", "text": "Text"}]
    ]


def test_pass_string_without_copy_to_callback():
    """

    :return:
    """
    with pytest.raises(Exception) as _:
        assert isinstance(Keyboa(items="Text").keyboard, InlineKeyboardMarkup)


def test_pass_one_button():
    """

    :return:
    """
    result = Keyboa(
        items=InlineKeyboardButton(**{"text": "text", "callback_data": "callback_data"})
    ).keyboard
    assert isinstance(result, InlineKeyboardMarkup)
    assert result.to_dict()["inline_keyboard"] == [
        [{"text": "text", "callback_data": "callback_data"}]
    ]


def test_pass_one_item_dict_with_text_field():
    """

    :return:
    """
    result = Keyboa(items={"text": "text", "callback_data": "callback_data"}).keyboard
    assert isinstance(result, InlineKeyboardMarkup)
    assert result.to_dict()["inline_keyboard"] == [
        [{"text": "text", "callback_data": "callback_data"}]
    ]


def test_pass_one_item_dict_without_text_field():
    """

    :return:
    """
    result = Keyboa(
        items={
            "word": "callback_data",
        }
    ).keyboard
    assert isinstance(result, InlineKeyboardMarkup)
    assert result.to_dict()["inline_keyboard"] == [
        [{"text": "word", "callback_data": "callback_data"}]
    ]


def test_pass_multi_item_dict_without_text_field():
    """

    :return:
    """
    with pytest.raises(ValueError) as _:
        wrong_dict = {
            "word_1": "callback_data_1",
            "word_2": "callback_data_1",
        }
        Keyboa(items=wrong_dict).keyboard


def test_pass_one_row():
    """

    :return:
    """
    start = 0
    stop = 8
    result = Keyboa(
        items=list(range(start, stop)),
        front_marker="FRONT_",
        copy_text_to_callback=True,
    ).keyboard
    assert isinstance(result, InlineKeyboardMarkup)
    assert len(result.to_dict()["inline_keyboard"]) == stop
    assert (
        result.to_dict()["inline_keyboard"][0][0]["callback_data"] == "FRONT_%s" % start
    )


def test_pass_structure():
    """

    :return:
    """
    result = Keyboa(
        items=[list(range(4)), list(range(2, 5)), "string", {"t": "cbd"}],
        front_marker="STRUCTURE_",
        copy_text_to_callback=True,
    ).keyboard

    assert isinstance(result, InlineKeyboardMarkup)
    assert len(result.to_dict()["inline_keyboard"]) == 4
    assert result.to_dict()["inline_keyboard"][0][0]["callback_data"] == "STRUCTURE_0"
    assert result.to_dict()["inline_keyboard"][1][0]["callback_data"] == "STRUCTURE_2"
    assert (
        result.to_dict()["inline_keyboard"][2][0]["callback_data"] == "STRUCTURE_string"
    )
    assert result.to_dict()["inline_keyboard"][3][0]["callback_data"] == "STRUCTURE_cbd"


def test_auto_keyboa_maker_alignment():
    result = Keyboa(
        items=list(range(0, 36)), copy_text_to_callback=True, alignment=True
    ).keyboard
    assert isinstance(result, InlineKeyboardMarkup)

    with pytest.raises(TypeError) as _:
        Keyboa(
            items=list(range(0, 36)),
            copy_text_to_callback=True,
            alignment="alignment",
        ).keyboard

    with pytest.raises(ValueError) as _:
        Keyboa(
            items=list(range(0, 36)), copy_text_to_callback=True, alignment=[-1, 0]
        ).keyboard

    with pytest.raises(ValueError) as _:
        Keyboa(
            items=list(range(0, 36)),
            copy_text_to_callback=True,
            alignment=[10, 11, 12],
        ).keyboard

    result = Keyboa(
        items=list(range(0, 36)),
        copy_text_to_callback=True,
        alignment=[
            3,
            4,
            6,
        ],
    ).keyboard
    assert isinstance(result, InlineKeyboardMarkup)

    result = Keyboa(
        items=list(range(0, 36)),
        copy_text_to_callback=True,
        alignment=True,
        alignment_reverse_range=True,
    ).keyboard
    assert isinstance(result, InlineKeyboardMarkup)

    result = Keyboa(
        items=list(range(0, 36)),
        copy_text_to_callback=True,
        alignment=[
            3,
            4,
            6,
        ],
        alignment_reverse_range=True,
    ).keyboard
    assert isinstance(result, InlineKeyboardMarkup)

    result = Keyboa(
        items=list(range(0, 36)),
        copy_text_to_callback=True,
        alignment=[
            5,
            7,
        ],
        alignment_reverse_range=True,
    ).keyboard
    assert isinstance(result, InlineKeyboardMarkup)


def test_auto_keyboa_maker_items_in_row():
    result = Keyboa(
        items=list(range(0, 36)), copy_text_to_callback=True, items_in_row=6
    ).keyboard
    assert isinstance(result, InlineKeyboardMarkup)


def test_slice():
    result = Keyboa(items=list(range(0, 36)), copy_text_to_callback=True).slice(
        slice_=slice(0, 12)
    )
    assert len(result.keyboard) == 12


def test_slice_with_markers():
    keyboa = Keyboa(items=list(range(0, 6)))
    keyboa.front_marker = "front"
    keyboa.back_marker = "back"

    result = keyboa.keyboard
    assert len(result.keyboard) == 6
