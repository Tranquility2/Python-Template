"""Test the intro module."""

import pytest

from module.main import run


def test_main(capsys: pytest.CaptureFixture) -> None:
    """Test the main function."""
    run()
    captured = capsys.readouterr()
    assert "Working!\n" in captured.out
