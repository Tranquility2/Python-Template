"""Nox configuration file for project."""

import pathlib
import shutil

import nox
from nox.sessions import Session

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
    "./**/*.egg-info",
]

nox.options.sessions = [
    "tests_with_coverage",
    "coverage_combine_and_report",
]
REQUIREMENTS = [
    "requirements/requirements.txt",
    "requirements/requirements-dev.txt",
    "requirements/requirements-test.txt",
]


@nox.session(python=SUPPORTED_PYTHON_VERSIONS)
def tests_with_coverage(session: Session) -> None:
    """Run unit tests with coverage saved to partial file."""

    session.install(".[test]")
    session.run("coverage", "run", "-p", "-m", "pytest", TESTS_PATH)


@nox.session(python=DEFAULT_PYTHON_VERSION)
def coverage_combine_and_report(session: Session) -> None:
    """Combine all coverage files and generate a report."""

    session.install(".[test]")
    session.run("coverage", "combine")
    session.run("coverage", "report")
    session.run("coverage", "xml")


@nox.session(python=DEFAULT_PYTHON_VERSION, reuse_venv=True)
def isort(session: Session) -> None:
    """Run isort import formatter."""

    session.install("isort")
    session.run("isort", ".")


@nox.session(python=DEFAULT_PYTHON_VERSION, reuse_venv=True)
def black(session: Session) -> None:
    """Run black code formatter."""

    session.install("black")
    session.run("black", ".")


@nox.session(python=DEFAULT_PYTHON_VERSION, reuse_venv=True)
def mypy(session: nox.Session) -> None:
    """Run mypy against package and all required dependencies."""

    session.install(".")
    session.install("mypy")
    session.run("mypy", "-p", MODULE_NAME, "--no-incremental")


@nox.session(python=DEFAULT_PYTHON_VERSION, reuse_venv=True)
def check(session: Session) -> None:
    """Run all checks."""

    isort(session)
    black(session)
    mypy(session)


@nox.session(python=DEFAULT_PYTHON_VERSION)
def build(session: Session) -> None:
    """Build distribution files."""

    session.install("build")
    session.run("python", "-m", "build")


@nox.session(python=False)
def install(session: Session) -> None:
    """Setup a development environment. Uses active venv if available, builds one if not."""

    session.run("python", "-m", "pip", "install", "-e", ".[dev,test]")
    session.run("pre-commit", "install")


@nox.session(python=False)
def requirements(session: Session) -> None:
    """Compile the project requirements."""

    session.run("pip", "install", "pip-tools", silent=True)

    for req_file in REQUIREMENTS:
        session.run("pip-compile", "-o", req_file, f"{req_file.replace('.txt', '.in')}")


@nox.session(python=False)
def sync(session: Session) -> None:
    """Sync the project requirements."""

    session.run("pip", "install", "pip-tools", silent=True)
    session.run("pip-sync", "requirements-dev.txt")


@nox.session(python=False)
def clean(session: Session) -> None:
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
