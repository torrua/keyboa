# -*- coding:utf-8 -*-
"""
Test for button_maker() function
"""
import os
import sys

sys.path.insert(0, "%s/../" % os.path.dirname(os.path.abspath(__file__)))

import pytest
from telebot.types import InlineKeyboardButton
from keyboa import Button

BUTTON_SOURCE_TYPES_ACCEPTABLE_WITH_COPY_TO_CALLBACK = (
    2,
    "a",
    "2",
    {
        2: "a",
    },
    {
        "a": 2,
    },
    (2, "a"),
    ("a", 2),
    ("a", None),
)

BUTTON_SOURCE_TYPES_UNACCEPTABLE_WITHOUT_COPY_TO_CALLBACK = (
    2,
    "a",
    "2",
    ("a", None),
)

UNACCEPTABLE_BUTTON_SOURCE_TYPES = (
    {2, "a"},
    {"a", 2},
    [2, "a"],
    (2, {}),
    ["a", 2],
    (None, 2),
    (None, None),
    None,
)

COMBO_BUTTON_DATA = (
    {"button_text": "button_callback_data"},
    ("button_text", "button_callback_data"),
)

UNACCEPTABLE_BUTTON_TEXTS = [
    [None, "button_callback_data"],
    (None, "button_callback_data"),
    [{"test_data": "test_data"}, "button_callback_data"],
]

STRING_INT = ["12345", 12345]


@pytest.mark.parametrize(
    "button_data", BUTTON_SOURCE_TYPES_ACCEPTABLE_WITH_COPY_TO_CALLBACK
)
def test_acceptable_button_source_types(button_data):
    """

    :param button_data:
    :return:
    """
    assert isinstance(
        Button(button_data=button_data, copy_text_to_callback=True).generate(),
        InlineKeyboardButton,
    )


@pytest.mark.parametrize(
    "button_data", BUTTON_SOURCE_TYPES_UNACCEPTABLE_WITHOUT_COPY_TO_CALLBACK
)
def test_unacceptable_button_source_types_without_callback(button_data):
    """

    :param button_data:
    :return:
    """
    with pytest.raises(Exception) as _:
        Button(button_data=button_data, copy_text_to_callback=False).generate()


@pytest.mark.parametrize("button_data", UNACCEPTABLE_BUTTON_SOURCE_TYPES)
def test_unacceptable_button_source_types(button_data):
    """

    :param button_data:
    :return:
    """
    with pytest.raises(Exception) as _:
        Button(button_data=button_data).generate()


def test_unacceptable_front_marker_type():
    """

    :return:
    """
    with pytest.raises(Exception) as _:
        Button(
            button_data="button_text",
            front_marker={
                1,
                2,
                3,
            },
        ).generate()


def test_unacceptable_back_marker_type():
    """

    :return:
    """
    with pytest.raises(Exception) as _:
        Button(
            button_data="button_text",
            back_marker={
                1,
                2,
                3,
            },
        ).generate()


def test_unacceptable_callback_data_type():
    """

    :return:
    """
    with pytest.raises(Exception) as _:
        Button(
            button_data=[
                "button_text",
                {
                    1,
                    2,
                    3,
                },
            ]
        ).generate()


@pytest.mark.parametrize("button_data", UNACCEPTABLE_BUTTON_TEXTS)
def test_unacceptable_text_type(button_data):
    """

    :param button_data:
    :return:
    """
    with pytest.raises(Exception) as _:
        Button(button_data=button_data).generate()


@pytest.mark.parametrize("button_data", COMBO_BUTTON_DATA)
def test_create_button_from_dict_tuple_list(button_data):
    """

    :param button_data:
    :return:
    """
    button = Button(
        button_data=button_data,
        front_marker="front_",
        back_marker="_back",
    ).generate()
    assert isinstance(button, InlineKeyboardButton)
    assert button.text == "button_text"
    assert button.callback_data == "front_button_callback_data_back"


@pytest.mark.parametrize("button_data", STRING_INT)
def test_create_button_from_int_or_str_with_copy_option(button_data):
    """

    :param button_data:
    :return:
    """
    button = Button(
        button_data=button_data,
        front_marker="front_",
        back_marker="_back",
        copy_text_to_callback=True,
    ).generate()
    assert isinstance(button, InlineKeyboardButton)
    assert button.text == "12345"
    assert button.callback_data == "front_12345_back"


@pytest.mark.parametrize("button_data", STRING_INT)
def test_create_button_from_int_or_str_without_copy_option(button_data):
    """

    :param button_data:
    :return:
    """
    button = Button(
        button_data=button_data,
        front_marker="front_",
        copy_text_to_callback=False,
    ).generate()
    assert isinstance(button, InlineKeyboardButton)
    assert button.text == "12345"
    assert button.callback_data == "front_"


@pytest.mark.parametrize("button_data", STRING_INT)
def test_create_button_from_int_or_str_without_callback(button_data):
    """

    :param button_data:
    :return:
    """
    with pytest.raises(Exception) as _:
        Button(
            button_data=button_data,
            copy_text_to_callback=False,
        ).generate()


def test_create_button_from_button():
    """

    :return:
    """
    test_button = Button(
        button_data="button_text",
        front_marker="front_",
        back_marker="_back",
        copy_text_to_callback=True,
    ).generate()
    button = Button(button_data=test_button).generate()
    assert button == test_button
    assert button is test_button
    assert isinstance(button, InlineKeyboardButton)
    assert button.text == "button_text"
    assert button.callback_data == "front_button_text_back"


def test_empty_text():
    """

    :return:
    """
    with pytest.raises(Exception) as _:
        Button(button_data=("", "button_callback_data")).generate()


def test_empty_callback_data():
    """
    :return:
    """
    with pytest.raises(Exception) as _:
        Button(button_data=("button_text", ""), copy_text_to_callback=False).generate()


def test_big_callback_data():
    """
    :return:
    """
    with pytest.raises(Exception) as _:
        Button(
            button_data=("button_text", "limit" * 13), copy_text_to_callback=False
        ).generate()


def test_none_as_markers():
    Button(button_data="button_text", copy_text_to_callback=True).generate()

    Button(
        button_data="button_text",
        front_marker=None,
        back_marker=None,
        copy_text_to_callback=True,
    ).generate()


def test_button_property():
    btn = Button(button_data="button_text", copy_text_to_callback=True).button
    assert isinstance(btn, InlineKeyboardButton)
