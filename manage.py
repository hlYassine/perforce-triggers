import click
import subprocess
from os import path

BIN_DIR = "./.venv/bin"


def run_format():
    autopep8_cmd_args = [
        path.join(BIN_DIR, "autopep8"),
        "--in-place",
        "--aggressive",
        "-r",
        "./perforce_triggers"
    ]
    subprocess.call(autopep8_cmd_args)


def run_pylint():
    pylint_cmd_args = [
        path.join(BIN_DIR, "pylint"),
        "./perforce_triggers"
    ]
    subprocess.call(pylint_cmd_args)


def run_mypy():
    mypy_cmd_args = [
        path.join(BIN_DIR, "mypy"),
        "--config-file",
        "./.mypy.ini",
        "./perforce_triggers"
    ]
    subprocess.call(mypy_cmd_args)


def run_pytest():
    pytest_cmd_args = [
        path.join(BIN_DIR, "pytest"),
        "./tests"
    ]
    subprocess.call(pytest_cmd_args)


@click.command()
@click.option("--format", "-f", is_flag=True, help="Run autopep8")
@click.option("--pylint", "-l", is_flag=True, help="pylint")
@click.option("--mypy", "-m", is_flag=True, help="mypy")
@click.option("--pytest", "-t", is_flag=True, help="pytest")
@click.option("--all", "-a", is_flag=True, help="in order: format, pylint, mypy and pytest")
def main(format, pylint, mypy, pytest, all):
    if all:
        format = True
        pylint = True
        mypy = True
        pytest = True

    if format:
        click.echo("running manage.py --format")
        run_format()
    if pylint:
        click.echo("running manage.py --pylint")
        run_pylint()

    if mypy:
        click.echo("running manage.py --mypy")
        run_mypy()

    if pytest:
        click.echo("running manage.py --pytest")
        run_pytest()


if __name__ == "__main__":
    main()
