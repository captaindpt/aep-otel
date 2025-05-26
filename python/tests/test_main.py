import pytest
from aep_otel import __version__

def test_version():
    assert __version__ == "0.0.1a0"

def test_example():
    assert True 