"""Test the intro module."""

from module.intro import main


def test_main(capsys):
    """Test the main function."""
    main()
    captured = capsys.readouterr()
    assert "Working!\n" in captured.out
