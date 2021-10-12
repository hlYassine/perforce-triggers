import logging
from os import path, makedirs
from perforce_triggers import config
from perforce_triggers import cli

log = logging.getLogger(__name__)


def setup_logging(level):
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=level
    )

    # log file handler
    log_dir_abspath = config.get_log_dir()
    if not path.exists(log_dir_abspath):
        makedirs(log_dir_abspath, exist_ok=True)

    log_file_abspath = path.join(log_dir_abspath, "log.txt")
    log_file_handler = logging.FileHandler(log_file_abspath)
    log_file_handler.setLevel(level)
    log.addHandler(log_file_handler)


def main():
    setup_logging(logging.INFO)
    cli.cli()


if __name__ == "__main__":
    main()
