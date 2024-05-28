"""Nox configuration file for project."""

import pathlib
import shutil

import nox

MODULE_NAME = "module"
TESTS_PATH = "tests"
DEFAULT_PYTHON_VERSION = "3.9"
VERBOSE = True

PYTHON_MATRIX = ["3.9", "3.10", "3.11", "3.12"]

CLEANABLE_TARGETS = [
    "./dist",
    "./build",
    "./.nox",
    "./.coverage",
    "./.coverage.*",
    "./coverage.json",
    "./**/.mypy_cache",
    "./**/.pytest_cache",
    "./**/__pycache__",
    "./**/*.pyc",
    "./**/*.pyo",
]

nox.options.sessions = [
    "tests",
    "mypy_check",
]


@nox.session(python=DEFAULT_PYTHON_VERSION)
def tests(session: nox.Session) -> None:
    """Run unit tests with coverage and output to terminal."""

    session.install(".[test]")
    session.run("pytest", "--cov-report", "term-missing", f"--cov={MODULE_NAME}", TESTS_PATH)


@nox.session(python=DEFAULT_PYTHON_VERSION)
def mypy_check(session: nox.Session) -> None:
    """Run mypy against package and all required dependencies."""

    session.install(".")
    session.install("mypy")
    session.run("mypy", "-p", MODULE_NAME, "--no-incremental")


@nox.session(python=DEFAULT_PYTHON_VERSION)
def build(session: nox.Session) -> None:
    """Build distribution files."""

    session.install("hatch")
    session.run("hatch", "build")


@nox.session(python=False)
def install(session: nox.Session) -> None:
    """Setup a development environment. Uses active venv if available, builds one if not."""
    session.run("python", "-m", "pip", "install", "-e", ".[dev,test]")
    session.run("pre-commit", "install")


@nox.session(python=False)
def clean(session: nox.Session) -> None:
    """Clean cache, .pyc, .pyo, and test/build artifact files from project."""
    count = 0
    for searchpath in CLEANABLE_TARGETS:
        for filepath in pathlib.Path(".").glob(searchpath):
            if filepath.is_dir():
                session.log(f"Removing directory: {filepath}")
                shutil.rmtree(filepath)
            else:
                session.log(f"Removing file: {filepath}")
                filepath.unlink()
            count += 1

    session.log(f"{count} files cleaned.")
