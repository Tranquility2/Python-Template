"""Test the intro module."""

import pytest

from module.intro import main


def test_main(capsys: pytest.CaptureFixture) -> None:
    """Test the main function."""
    main()
    captured = capsys.readouterr()
    assert "Working!\n" in captured.out
