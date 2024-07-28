"""Intro module."""

import platform


def print_info() -> None:
    """Print info."""
    print("Python version: ", platform.python_version())
    print("Platform: ", platform.platform())


def do_calculation(a: int, b: int) -> int:
    """Do a calculation."""
    return a + b


def run() -> None:
    """Run the module."""
    print("Working!")
