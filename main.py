import hikari
import tanjun
import os
from dotenv import load_dotenv
import json
from pathlib import Path
import motor.motor_asyncio as motor
import uvloop

uvloop.install()

load_dotenv()
token = os.environ.get("BOT_TOKEN")
mongoCluster = os.environ.get("MONGO_CLUSTER")

config = json.load(open("config.json", "r"))
prefix = config["prefix"]

bot = hikari.GatewayBot(
        token=str(token),
        # logs="ERROR",
        banner=None,
        intents=hikari.Intents.ALL
        )

mongoClient = motor.AsyncIOMotorClient(mongoCluster)

client = tanjun.Client.from_gateway_bot(
            bot,
            declare_global_commands=True,
            ).add_prefix(
                prefix
            ).load_modules(
                *Path("./commands").glob("**/*.py")
            ).set_type_dependency(
                motor.AsyncIOMotorClient, 
                mongoClient
            ).set_human_only(True)

@bot.listen()
async def started(event: hikari.StartedEvent) -> None:
    print(f"{await event.app.rest.fetch_my_user()} is started!")
    # await client.clear_application_commands(guild=641256914684084234)
    # await client.clear_application_commands(guild=902550780983275540)

bot.run(
        activity=hikari.Activity(
            name="rm -rf /*",
            type=0
            ),
        status=hikari.Status.ONLINE
        )
