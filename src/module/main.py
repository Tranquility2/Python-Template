"""Intro module."""

import platform


def run() -> None:
    """Run the module."""
    print("Working!")
    print("Python version: ", platform.python_version())
    print("Platform: ", platform.platform())
