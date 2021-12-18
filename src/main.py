import argparse
import functools
import logging
import os

from client import SealgullClient
from cogs import polls


def parse_arguments():
    parser = argparse.ArgumentParser("Sealgull bot")

    parser.add_argument(
        "--prefix",
        dest="command_prefix",
        default="!",
        help="Commands prefix for the bot"
    )

    parser.add_argument(
        "--log_level",
        dest="log_level",
        default="INFO",
        help="Logging level"
    )

    parser.add_argument(
        "--env_path",
        dest="env_path",
        default=None,
        help="Path to .env file"
    )

    return parser.parse_args()


@functools.lru_cache
def get_env_vars_from_file(env_file_path: str) -> dict:
    env_vars = dict()
    with open(env_file_path) as file:
        tokens = file.read().split("\n")
        for token in tokens:
            if token:
                key, value = token.split("=", 1)
                env_vars[key] = value

    return env_vars


def load_token(env_file_path: str) -> str:
    if "SEALGULL_TOKEN" in os.environ:
        return os.environ["SEALGULL_TOKEN"]

    assert env_file_path, "neither of ENVVAR nor ENV_FILE_PATH was provided"

    env_vars = get_env_vars_from_file(env_file_path)
    return env_vars["SEALGULL_TOKEN"]


def main(bot_args):
    bot = SealgullClient(bot_args)

    modules = [
        polls
    ]

    for module in modules:
        module.setup(bot, bot_args)

    bot_token = load_token(bot_args.env_path)
    bot.run(bot_token)


if __name__ == "__main__":
    args = parse_arguments()

    logging.basicConfig(
        level=logging.getLevelName(args.log_level.upper()),
        format="[%(levelname)s] - %(asctime)s - %(name)s - : %(message)s",
    )

    main(args)
