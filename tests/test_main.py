"""Test the intro module."""

import pytest

from module.main import do_calculation, print_info, run


def test_print_info(capsys: pytest.CaptureFixture) -> None:
    """Test the print_info function."""
    print_info()
    captured = capsys.readouterr()
    assert "Python version: " in captured.out
    assert "Platform: " in captured.out


def test_do_calculation() -> None:
    """Test the do_calculation function."""
    assert do_calculation(1, 2) == 3


def test_main(capsys: pytest.CaptureFixture) -> None:
    """Test the main function."""
    run()
    captured = capsys.readouterr()
    assert "Working!\n" in captured.out
