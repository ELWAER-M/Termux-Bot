import hikari
from hikari.embeds import Embed
import tanjun
import platform

component = tanjun.Component()


@component.with_command
@tanjun.as_message_command("info")
async def info_msg(ctx: tanjun.abc.MessageContext, /) -> None:
    await info(ctx)

@component.with_slash_command
@tanjun.as_slash_command("info", "Some info about the bot host")
async def info_slash(ctx: tanjun.abc.SlashContext) -> None:
    await info(ctx)

async def info(ctx: tanjun.abc.Context, /) -> None:
    system = platform.system()
    arch = platform.machine()
    py_ver = platform.python_version()
    hikari_ver = hikari.__version__
    tanjun_ver = tanjun.__version__

    await ctx.respond(embed=hikari.Embed(
                        description=f"**System:** `{system}`\n**Architecture:** `{arch}`\n**Python**: `{py_ver}`\n**Hikari:** `{hikari_ver}`\n**Tanjun:** `{tanjun_ver}`",
                        color="#ffe500"))

load_command = component.make_loader()
