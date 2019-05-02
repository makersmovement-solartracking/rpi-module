import pytest
import i2c_connector

def test_aggregate_bytes():
    left = 0b10000000
    right = 0b00000001
    assert i2c_connector.aggregate_bytes(left,right) == 32769
