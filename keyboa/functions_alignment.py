# -*- coding:utf-8 -*-
"""
Module with functions for work with alignment
"""
from typing import Optional, Iterable

from keyboa.constants import AUTO_ALIGNMENT_RANGE, \
    MAXIMUM_ITEMS_IN_LINE, MINIMUM_ITEMS_IN_LINE


def calculate_items_in_row(
        items, auto_alignment, reverse_alignment_range) -> Optional[int]:
    """
    :param items:
    :param auto_alignment:
    :param reverse_alignment_range:
    :return:
    """

    items_in_row = None
    alignment_range = get_alignment_range(auto_alignment)

    if reverse_alignment_range:
        alignment_range = reversed(alignment_range)

    for divider in alignment_range:
        if not len(items) % divider:
            items_in_row = divider
            break

    return items_in_row


def get_alignment_range(auto_alignment):
    """
    :param auto_alignment:
    :return:
    """

    if isinstance(auto_alignment, bool):
        return AUTO_ALIGNMENT_RANGE

    check_alignment_settings(auto_alignment)
    return auto_alignment


def check_alignment_settings(auto_alignment):
    """
    :param auto_alignment:
    :return:
    """
    check_is_alignment_iterable(auto_alignment)
    check_is_alignment_in_limits(auto_alignment)


def check_is_alignment_in_limits(auto_alignment):
    """
    :param auto_alignment:
    :return:
    """
    if max(auto_alignment) > MAXIMUM_ITEMS_IN_LINE \
            or min(auto_alignment) < MINIMUM_ITEMS_IN_LINE:
        value_error_message = \
            "The auto_alignment's item values should be between " \
            "%s and %s. You entered: %s\n" \
            "You may define it as 'True' to use AUTO_ALIGNMENT_RANGE." \
            % (MINIMUM_ITEMS_IN_LINE, MAXIMUM_ITEMS_IN_LINE, auto_alignment)
        raise ValueError(value_error_message)


def check_is_alignment_iterable(auto_alignment):
    """
    :param auto_alignment:
    :return:
    """
    if not (isinstance(auto_alignment, Iterable)
            and all(map(lambda s: isinstance(s, int), auto_alignment))):
        type_error_message = \
            "The auto_alignment variable has not a proper type. " \
            "Only Iterable of integers or boolean type allowed.\n" \
            "You may define it as 'True' to use AUTO_ALIGNMENT_RANGE."
        raise TypeError(type_error_message)
