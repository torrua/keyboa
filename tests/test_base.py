# -*- coding:utf-8 -*-
"""
Test for button_maker() function
"""
import os
import sys

sys.path.insert(0, "%s/../" % os.path.dirname(os.path.abspath(__file__)))

import pytest
from keyboa.keyboards import Keyboa


def test_items_is_none_or_empty():
    """

    :return:
    """
    with pytest.raises(ValueError) as _:
        Keyboa(items=list())
    with pytest.raises(ValueError) as _:
        Keyboa(items=None)


def test_copy_text_to_callback_is_not_bool():
    """

    :return:
    """
    with pytest.raises(TypeError) as _:
        Keyboa(items=[1, 2, 3], copy_text_to_callback="text")


def test_number_of_items_out_of_limits():
    """

    :return:
    """
    with pytest.raises(ValueError) as _:
        Keyboa(items=list(range(200)), copy_text_to_callback=True)


def test_number_of_items_in_row_out_of_limits():
    """

    :return:
    """
    with pytest.raises(ValueError) as _:
        Keyboa(items=[[1, 2, 3], list(range(10))], copy_text_to_callback=True)
