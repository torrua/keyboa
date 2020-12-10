# -*- coding:utf-8 -*-
"""
Test for keyboa_combiner() function
"""
import os
import sys

import pytest

sys.path.insert(0, "%s/../" % os.path.dirname(os.path.abspath(__file__)))

from keyboa.keyboards import keyboa_combiner, keyboa_maker
from telebot.types import InlineKeyboardMarkup


def test_keyboards_is_none():
    assert isinstance(keyboa_combiner(), InlineKeyboardMarkup)
    assert keyboa_combiner().__dict__ == InlineKeyboardMarkup().__dict__


def test_keyboards_is_single_keyboard():
    kb = keyboa_maker(items=list(range(0, 4)), copy_text_to_callback=True)
    result = keyboa_combiner(keyboards=kb)

    assert isinstance(result, InlineKeyboardMarkup)
    assert result.__dict__ == kb.__dict__


def test_keyboards_is_multi_keyboards():
    kb_1 = keyboa_maker(items=list(range(0, 4)), copy_text_to_callback=True)
    kb_2 = keyboa_maker(items=list(range(10, 15)), copy_text_to_callback=True)

    result = keyboa_combiner(keyboards=(kb_1, kb_2))
    assert isinstance(result, InlineKeyboardMarkup)

    result = keyboa_combiner(keyboards=(kb_1, None, kb_2))
    assert isinstance(result, InlineKeyboardMarkup)

    with pytest.raises(TypeError) as _:
        keyboa_combiner(keyboards=(kb_1, 1))
