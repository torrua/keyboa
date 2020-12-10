# -*- coding:utf-8 -*-
"""
Test for _button_data_extractor() function
"""
import os
import sys

sys.path.insert(0, "%s/../" % os.path.dirname(os.path.abspath(__file__)))

import pytest

from keyboa.keyboards import _button_data_extractor


def test_button_data_extractor():
    with pytest.raises(TypeError) as _:
        _button_data_extractor(True)

    with pytest.raises(TypeError) as _:
        _button_data_extractor((1, {"wrong": "text", }))
