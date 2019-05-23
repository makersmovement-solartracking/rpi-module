import pytest
import i2c_connector as i2c


def test_aggregate_bytes():
    """ Tests if the aggreate_bytes function is working correctly"""
    left = 0b10000000
    right = 0b00000001
    assert i2c.aggregate_bytes(left, right) == 32769


def test_empty_ldr_list():
    """ Tests the answer if the ldr list is empty"""
    ldr_list = []
    with pytest.raises(i2c.EmptyLDRListException) as EmptyListException:
        i2c.check_ldr_list_length(ldr_list)


def test_odd_ldr_list():
    """ Tests the answer if the ldr list is odd."""
    ldr_list = [255, 255, 255]
    with pytest.raises(i2c.OddLDRListException) as OddListException:
        i2c.check_ldr_list_length(ldr_list)


def test_even_ldr_list():
    """ Tests the software behavior when the ldr list is
    even. """
    ldr_list = [255, 255, 255, 255]
    assert i2c.check_ldr_list_length(ldr_list) is True


def test_invalid_ldr_values_list():
    """ Tests the validation of an invalid ldr values
    list. """
    ldr_list = [300, 487, 908, 65535]
    assert i2c.validates_ldr_data(ldr_list) is False


def test_valid_ldr_values_list():
    """ Tests the validation of a valid ldr values
    list. """
    ldr_list = [300, 487, 908, 920]
    assert i2c.validates_ldr_data(ldr_list) is True
