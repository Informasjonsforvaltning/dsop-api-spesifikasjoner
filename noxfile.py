"""Nox sessions."""
import tempfile
from typing import Any

import nox
from nox.sessions import Session

package = "dsop_api_spesifikasjoner"
locations = "src", "tests", "noxfile.py"
nox.options.stop_on_first_error = True
nox.options.sessions = (
    "lint",
    "mypy",
)


def install_with_constraints(session: Session, *args: str, **kwargs: Any) -> None:
    """Install packages constrained by Poetry's lock file."""
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            f"--output={requirements.name}",
            external=True,
        )
        session.install(f"--constraint={requirements.name}", *args, **kwargs)


@nox.session(python=["3.7", "3.8", "3.9"])
def tests(session: Session) -> None:
    """Run the test suite."""
    args = session.posargs
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(
        session,
        "pytest",
    )
    session.run(
        "pytest",
        "-rA",
        *args,
        env={"DATASERVICE_PUBLISHER_URL": "http://dataservice-publisher:8080"},
    )


@nox.session(python=["3.7", "3.8", "3.9"])
def black(session: Session) -> None:
    """Run black code formatter."""
    args = session.posargs or locations
    install_with_constraints(session, "black")
    session.run("black", *args)


@nox.session(python=["3.7", "3.8", "3.9"])
def lint(session: Session) -> None:
    """Lint using flake8."""
    args = session.posargs or locations
    install_with_constraints(
        session,
        "flake8",
        "flake8-annotations",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-docstrings",
        "flake8-import-order",
        "darglint",
        "flake8-assertive",
    )
    session.run("flake8", *args)


@nox.session(python=["3.7", "3.8", "3.9"])
def safety(session: Session) -> None:
    """Scan dependencies for insecure packages."""
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        install_with_constraints(session, "safety")
        session.run("safety", "check", f"--file={requirements.name}", "--full-report")


@nox.session(python=["3.7", "3.8", "3.9"])
def mypy(session: Session) -> None:
    """Type-check using mypy."""
    args = session.posargs or locations
    install_with_constraints(session, "mypy")
    session.run("mypy", *args)


@nox.session(python=["3.7", "3.8", "3.9"])
def coverage(session: Session) -> None:
    """Upload coverage data."""
    install_with_constraints(session, "coverage[toml]", "codecov")
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)
