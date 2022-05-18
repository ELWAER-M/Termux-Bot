import hikari
import tanjun

import os
from dotenv import load_dotenv
import json
from pathlib import Path

config = json.load(open("config.json", "r"))

def create_bot() -> hikari.impl.GatewayBot:
    load_dotenv()
    token = os.environ.get("BOT_TOKEN")

    bot = hikari.GatewayBot(
            token=str(token),
            # logs="ERROR",
            banner=None,
            intents=hikari.Intents.ALL
            )

    create_client(bot)

    return bot

def create_client(bot: hikari.GatewayBot) -> tanjun.Client:
    prefix = config["prefix"]

    tanjun_client = (
            tanjun.Client.from_gateway_bot(
                bot, 
                declare_global_commands=True
                )
                .add_prefix(prefix)
                .load_modules(*Path("./bot/commands").glob("**/*.py"))
                .load_modules(*Path("./bot/events").glob("**/*.py"))
                .set_human_only(True)
            )
    return tanjun_client

def main(status: hikari.Status) -> None:
    status_text = config["status_text"]
    status_type = config["status_type"]

    create_bot().run(
            activity=hikari.Activity(
                name=status_text,
                type=status_type
                ),
            status=status
            )
