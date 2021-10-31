import hikari
import tanjun
import os
from dotenv import load_dotenv
import json
from pathlib import Path

load_dotenv()
token = os.environ.get("TOKEN")
config = json.load(open("config.json", "r"))
prefix = config["prefix"]

bot = hikari.GatewayBot(
        token=token,
        banner=None,
        logs="ERROR"
        )

client = tanjun.Client.from_gateway_bot(
            bot,
            declare_global_commands=True,
            mention_prefix=True
        ).add_prefix(prefix).load_modules(*Path("./commands").glob("**/*.py"))

@bot.listen()
async def started(event: hikari.StartedEvent) -> None:
    print(f"{bot.get_me().username} is started!")

bot.run(
        activity=hikari.Activity(
            name="rm -rf /*",
            type=0
            ),
        status=hikari.Status.IDLE
        )
