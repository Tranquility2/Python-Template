"""Nox configuration file for project."""

import pathlib
import shutil

import nox

MODULE_NAME = "module"
TESTS_PATH = "tests"
DEFAULT_PYTHON_VERSION = "3.9"
SUPPORTED_PYTHON_VERSIONS = ["3.9", "3.10", "3.11", "3.12"]
CLEANABLE_TARGETS = [
    "./dist",
    "./build",
    "./.nox",
    "./.coverage",
    "./.coverage.*",
    "./coverage.xml",
    "./coverage.json",
    "./**/.mypy_cache",
    "./**/.pytest_cache",
    "./**/__pycache__",
    "./**/*.pyc",
    "./**/*.pyo",
]

nox.options.sessions = [
    "tests_with_coverage",
    "coverage_combine_and_report",
]


@nox.session(python=SUPPORTED_PYTHON_VERSIONS)
def tests_with_coverage(session: nox.Session) -> None:
    """Run unit tests with coverage saved to partial file."""

    session.install(".[test]")
    session.run("coverage", "run", "-p", "-m", "pytest", TESTS_PATH)


@nox.session(python=DEFAULT_PYTHON_VERSION)
def coverage_combine_and_report(session: nox.Session) -> None:
    """Combine all coverage files and generate a report."""

    session.install(".[test]")
    session.run("coverage", "combine")
    session.run("coverage", "report")
    session.run("coverage", "xml")


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
