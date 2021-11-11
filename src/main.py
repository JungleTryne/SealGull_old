import argparse
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

    return parser.parse_args()


def main(bot_args):
    bot = SealgullClient(bot_args)

    modules = [
        polls
    ]

    for module in modules:
        module.setup(bot, bot_args)

    bot_token = os.environ["SEALGULL_TOKEN"]
    bot.run(bot_token)


if __name__ == "__main__":
    args = parse_arguments()

    logging.basicConfig(
        level=logging.getLevelName(args.log_level.upper()),
        format="[%(levelname)s] - %(asctime)s - %(name)s - : %(message)s",
    )

    main(args)
