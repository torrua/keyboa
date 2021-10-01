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
        assert isinstance(
            Keyboa(items="Text", copy_text_to_callback=False).keyboard,
            InlineKeyboardMarkup,
        )


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
        kb = Keyboa(items=wrong_dict).keyboard


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
        kb = Keyboa(
            items=list(range(0, 36)),
            copy_text_to_callback=True,
            alignment="alignment",
        ).keyboard

    with pytest.raises(ValueError) as _:
        kb = Keyboa(
            items=list(range(0, 36)), copy_text_to_callback=True, alignment=[-1, 0]
        ).keyboard

    with pytest.raises(ValueError) as _:
        kb = Keyboa(
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
        alignment_reverse=True,
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
        alignment_reverse=True,
    ).keyboard
    assert isinstance(result, InlineKeyboardMarkup)

    result = Keyboa(
        items=list(range(0, 36)),
        copy_text_to_callback=True,
        alignment=[
            5,
            7,
        ],
        alignment_reverse=True,
    ).keyboard
    assert isinstance(result, InlineKeyboardMarkup)


def test_auto_keyboa_maker_items_in_row():
    result = Keyboa(
        items=list(range(0, 36)), copy_text_to_callback=True, items_in_row=6
    ).keyboard
    assert isinstance(result, InlineKeyboardMarkup)
    assert len(result.to_dict()["inline_keyboard"]) == 6


def test_slice():
    result = Keyboa(items=list(range(0, 36)), copy_text_to_callback=True).slice(
        slice_=slice(0, 12)
    )
    assert len(result.keyboard) == 12


def test_minimal_kb_with_copy_text_to_callback_specified_none():
    keyboa = Keyboa(items=list(range(0, 6)))
    result = keyboa.keyboard
    assert isinstance(result, InlineKeyboardMarkup)


def test_minimal_kb_with_items_out_of_limits():
    with pytest.raises(ValueError) as _:
        keyboa = Keyboa(items=list(range(0, 120)))


def test_minimal_kb_with_copy_text_to_callback_specified_true():
    keyboa = Keyboa(items=list(range(0, 6)), copy_text_to_callback=True)
    result = keyboa.keyboard
    assert isinstance(result, InlineKeyboardMarkup)


def test_minimal_kb_with_copy_text_to_callback_specified_false():
    keyboa = Keyboa(items=list(range(0, 6)), copy_text_to_callback=False)
    with pytest.raises(ValueError) as _:
        result = keyboa.keyboard


@pytest.mark.parametrize("items_in_row", [2, 3, 4, 6])
def test_minimal_kb_with_fixed_items_in_row(items_in_row):
    keyboa = Keyboa(items=list(range(0, 12)), items_in_row=items_in_row).keyboard
    kb_rows = keyboa.to_dict().get("inline_keyboard")
    assert len(kb_rows) == 12 / items_in_row


def test_minimal_kb_with_front_marker():
    keyboa = Keyboa(items=list(range(0, 3)), front_marker="front_").keyboard
    kb_rows = keyboa.to_dict().get("inline_keyboard")
    callbacks = [bnt[0].get("callback_data") for bnt in kb_rows]
    assert callbacks == [
        "front_0",
        "front_1",
        "front_2",
    ]


def test_minimal_kb_with_front_marker_and_copy_text_to_callback():
    keyboa = Keyboa(
        items=list(range(0, 3)), front_marker="front_", copy_text_to_callback=True
    ).keyboard
    kb_rows = keyboa.to_dict().get("inline_keyboard")
    callbacks = [bnt[0].get("callback_data") for bnt in kb_rows]
    assert callbacks == [
        "front_0",
        "front_1",
        "front_2",
    ]


def test_minimal_kb_with_back_marker():
    keyboa = Keyboa(items=list(range(0, 3)), back_marker="_back").keyboard
    kb_rows = keyboa.to_dict().get("inline_keyboard")
    callbacks = [bnt[0].get("callback_data") for bnt in kb_rows]
    assert callbacks == [
        "0_back",
        "1_back",
        "2_back",
    ]


def test_minimal_kb_with_back_marker_out_of_limits():
    with pytest.raises(ValueError) as _:
        marker_65 = "_1234567890123456789012345678901234567890123456789012345678901234"
        keyboa = Keyboa(items=list(range(0, 3)), back_marker=marker_65).keyboard


def test_minimal_kb_with_back_marker_out_of_limits_with_text():
    with pytest.raises(ValueError) as _:
        marker_64 = "1234567890123456789012345678901234567890123456789012345678901234"
        keyboa = Keyboa(
            items=list(range(0, 3)), back_marker=marker_64, copy_text_to_callback=True
        ).keyboard


def test_minimal_kb_with_empty_back_marker():
    with pytest.raises(ValueError) as _:
        keyboa = Keyboa(
            items=list(range(0, 3)), back_marker=str(), copy_text_to_callback=False
        ).keyboard


def test_minimal_kb_with_back_marker_and_copy_text_to_callback():
    keyboa = Keyboa(
        items=list(range(0, 3)), back_marker="_back", copy_text_to_callback=True
    ).keyboard
    kb_rows = keyboa.to_dict().get("inline_keyboard")
    callbacks = [bnt[0].get("callback_data") for bnt in kb_rows]
    assert callbacks == [
        "0_back",
        "1_back",
        "2_back",
    ]


def test_minimal_kb_with_front_and_back_markers():
    keyboa = Keyboa(
        items=list(range(0, 3)), front_marker="front_", back_marker="_back"
    ).keyboard
    kb_rows = keyboa.to_dict().get("inline_keyboard")
    callbacks = [bnt[0].get("callback_data") for bnt in kb_rows]
    assert callbacks == [
        "front_0_back",
        "front_1_back",
        "front_2_back",
    ]


def test_minimal_kb_with_front_and_back_markers_and_copy_text_to_callback():
    keyboa = Keyboa(
        items=list(range(0, 3)),
        copy_text_to_callback=True,
        front_marker="front_",
        back_marker="_back",
    ).keyboard
    kb_rows = keyboa.to_dict().get("inline_keyboard")
    callbacks = [bnt[0].get("callback_data") for bnt in kb_rows]
    assert callbacks == [
        "front_0_back",
        "front_1_back",
        "front_2_back",
    ]


def test_minimal_kb_with_front_and_back_markers_and_copy_text_to_callback_is_false():
    keyboa = Keyboa(
        items=list(range(0, 3)),
        copy_text_to_callback=False,
        front_marker="front_",
        back_marker="_back",
    ).keyboard
    kb_rows = keyboa.to_dict().get("inline_keyboard")
    callbacks = [bnt[0].get("callback_data") for bnt in kb_rows]
    assert callbacks == [
        "front__back",
        "front__back",
        "front__back",
    ]


def test_minimal_kb_with_alignment_true():
    keyboa = Keyboa(items=list(range(0, 12)), alignment=True).keyboard
    kb_rows = keyboa.to_dict().get("inline_keyboard")
    assert 12 / len(kb_rows) == 3


def test_minimal_kb_with_items_in_row():
    keyboa = Keyboa(items=list(range(0, 12)), items_in_row=6).keyboard
    kb_rows = keyboa.to_dict().get("inline_keyboard")
    assert 12 / len(kb_rows) == 6


def test_minimal_kb_with_items_in_row_out_of_limits():
    with pytest.raises(ValueError) as _:
        keyboa = Keyboa(items=list(range(0, 12)), items_in_row=12).keyboard


def test_minimal_kb_with_alignment_true_slice():
    keyboa = Keyboa(items=list(range(0, 12)), alignment=True).slice(slice_=slice(0, 6))
    kb_rows = keyboa.to_dict().get("inline_keyboard")
    assert 6 / len(kb_rows) == 3


def test_minimal_kb_with_alignment_true_and_reversed_alignment_true():
    keyboa = Keyboa(
        items=list(range(0, 12)), alignment=True, alignment_reverse=True
    ).keyboard
    kb_rows = keyboa.to_dict().get("inline_keyboard")
    assert 12 / len(kb_rows) == 4


def test_minimal_kb_with_alignment_specified():
    keyboa = Keyboa(items=list(range(0, 12)), alignment=range(2, 7)).keyboard
    kb_rows = keyboa.to_dict().get("inline_keyboard")
    assert 12 / len(kb_rows) == 2


def test_minimal_kb_with_alignment_specified_out_of_limits():
    with pytest.raises(ValueError) as _:
        keyboa = Keyboa(items=list(range(0, 12)), alignment=range(0, 12)).keyboard


def test_minimal_kb_with_alignment_specified_and_reversed_alignment_true():
    keyboa = Keyboa(
        items=list(range(0, 12)), alignment=range(2, 7), alignment_reverse=True
    ).keyboard
    kb_rows = keyboa.to_dict().get("inline_keyboard")
    assert 12 / len(kb_rows) == 6


def test_minimal_kb_with_reversed_alignment_true():
    # usually there is no needs and no sense for doing so
    keyboa = Keyboa(items=list(range(0, 12)), alignment_reverse=True).keyboard
    kb_rows = keyboa.to_dict().get("inline_keyboard")
    assert 12 / len(kb_rows) == 1


def test_minimal_kb_with_all_parameters_specified_reversed_range_true():
    keyboa = Keyboa(
        items=list(range(0, 12)),
        alignment=range(2, 7),
        copy_text_to_callback=True,
        front_marker="front_",
        back_marker="_back",
        alignment_reverse=True,
    ).keyboard
    kb_rows = keyboa.to_dict().get("inline_keyboard")
    assert len(kb_rows) == 2

    items_in_row = 12 / len(kb_rows)
    assert items_in_row == 6

    callbacks = [bnt[0].get("callback_data") for bnt in kb_rows]
    assert callbacks == [
        "front_0_back",
        "front_6_back",
    ]


def test_minimal_kb_with_all_parameters_specified_reversed_range_false():
    keyboa = Keyboa(
        items=list(range(0, 12)),
        alignment=range(2, 7),
        copy_text_to_callback=True,
        front_marker="front_",
        back_marker="_back",
        alignment_reverse=False,
    ).keyboard
    kb_rows = keyboa.to_dict().get("inline_keyboard")
    assert len(kb_rows) == 6

    items_in_row = 12 / len(kb_rows)
    assert items_in_row == 2

    callbacks = [bnt[0].get("callback_data") for bnt in kb_rows]
    assert callbacks == [
        "front_0_back",
        "front_2_back",
        "front_4_back",
        "front_6_back",
        "front_8_back",
        "front_10_back",
    ]


def test_structured_kb():
    keyboa = Keyboa(
        items=[
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
        ],
    ).keyboard
    kb_rows = keyboa.to_dict().get("inline_keyboard")
    assert len(kb_rows) == 3

    callbacks = [bnt[0].get("callback_data") for bnt in kb_rows]
    assert callbacks == [
        "1",
        "4",
        "7",
    ]


def test_structured_kb_with_alignment():
    with pytest.raises(TypeError) as _:
        keyboa = Keyboa(
            items=[
                [1, 2, 3],
                [4, 5, 6],
                [7, 8, 9],
            ],
            alignment=True,
        ).keyboard


def test_structured_kb_with_items_in_row():
    with pytest.raises(TypeError) as _:
        keyboa = Keyboa(
            items=[
                [1, 2, 3],
                [4, 5, 6],
                [7, 8, 9],
            ],
            items_in_row=6,
        ).keyboard


def test_structured_kb_with_front_marker():
    keyboa = Keyboa(
        items=[
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
        ],
        copy_text_to_callback=True,
        front_marker="front_",
    ).keyboard
    kb_rows = keyboa.to_dict().get("inline_keyboard")
    callbacks = [bnt[0].get("callback_data") for bnt in kb_rows]
    assert callbacks == [
        "front_1",
        "front_4",
        "front_7",
    ]


def test_structured_kb_with_front_marker_no_copy_text_to_callback():
    keyboa = Keyboa(
        items=[
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
        ],
        front_marker="front_",
    ).keyboard
    kb_rows = keyboa.to_dict().get("inline_keyboard")
    callbacks = [bnt[0].get("callback_data") for bnt in kb_rows]
    assert callbacks == [
        "front_1",
        "front_4",
        "front_7",
    ]


def test_kb_from_tuples():
    keyboa = Keyboa(
        items=[
            (1, "a"),
            (2, "b"),
            (3, "c"),
            (4, "d"),
            (5, "e"),
            (6, "f"),
        ]
    ).keyboard
    kb_rows = keyboa.to_dict().get("inline_keyboard")
    callbacks = [bnt[0].get("callback_data") for bnt in kb_rows]
    assert callbacks == ["a", "b", "c", "d", "e", "f"]


def test_kb_from_tuples_with_front_marker():
    keyboa = Keyboa(
        items=[
            (1, "a"),
            (2, "b"),
            (3, "c"),
            (4, "d"),
            (5, "e"),
            (6, "f"),
        ],
        front_marker="front_",
    ).keyboard
    kb_rows = keyboa.to_dict().get("inline_keyboard")
    callbacks = [bnt[0].get("callback_data") for bnt in kb_rows]
    assert callbacks == [
        "front_a",
        "front_b",
        "front_c",
        "front_d",
        "front_e",
        "front_f",
    ]


def test_kb_from_tuples_with_back_marker_and_items_in_row():
    keyboa = Keyboa(
        items=[
            (1, "a"),
            (2, "b"),
            (3, "c"),
            (4, "d"),
            (5, "e"),
            (6, "f"),
        ],
        back_marker="_back",
        items_in_row=2,
    ).keyboard
    kb_rows = keyboa.to_dict().get("inline_keyboard")
    callbacks = [bnt[0].get("callback_data") for bnt in kb_rows]
    assert callbacks == [
        "a_back",
        "c_back",
        "e_back",
    ]


def test_kb_with_items_in_row_and_last_buttons():
    keyboa = Keyboa(
        items=[
            (1, "a"),
            (2, "b"),
            (3, "c"),
            (4, "d"),
            (5, "e"),
            (6, "f"),
            (7, "g"),
        ],
        items_in_row=2,
    ).keyboard
    assert len(keyboa.keyboard) == 4


def test_kb_is_callable():
    keyboa = Keyboa(
        items=[
            (1, "a"),
            (2, "b"),
            (3, "c"),
            (4, "d"),
            (5, "e"),
            (6, "f"),
        ],
        back_marker="_is_callable",
        items_in_row=2,
    )
    assert type(keyboa.keyboard) == type(keyboa())
    assert keyboa.keyboard.to_json() == keyboa().to_json() == keyboa.slice().to_json()
    assert keyboa.slice(slice(3)).to_json() == keyboa(slice(3)).to_json()
    assert keyboa.slice(slice(2, 4, 2)).to_json() == keyboa(slice(2, 4, 2)).to_json()
