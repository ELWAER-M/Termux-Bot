import hikari
import tanjun
import platform

component = tanjun.Component()


@component.with_command
@tanjun.as_message_command("stat")
async def info_msg(ctx: tanjun.abc.MessageContext, /) -> None:
    await info(ctx)

@component.with_slash_command
@tanjun.as_slash_command("stat", "Some info about the bot host")
async def info_slash(ctx: tanjun.abc.SlashContext) -> None:
    await info(ctx)

async def info(ctx: tanjun.abc.Context, /) -> None:
    total_mem = int("".join(list(filter(lambda x: "MemTotal:" in x, open("/proc/meminfo", "r").read().splitlines()))).replace("MemTotal:        ", "").replace(" kB", ""))
    av_mem = int("".join(list(filter(lambda x: "MemAvailable:" in x, open("/proc/meminfo", "r").read().splitlines()))).replace("MemAvailable:     ", "").replace(" kB", ""))
    system = platform.system()
    arch = platform.machine()
    py_ver = platform.python_version()
    hikari_ver = hikari.__version__
    tanjun_ver = tanjun.__version__

    await ctx.respond(embed=hikari.Embed(
        description=f"**Used Memory:** `{(total_mem-av_mem)/1024/1024:.2f}Gb / {total_mem/1024/1024:.2F}Gb ({100.0*(total_mem-av_mem)/total_mem:.0f}%)`\n**System:** `{system}`\n**Architecture:** `{arch}`\n**Python**: `{py_ver}`\n**Hikari:** `{hikari_ver}`\n**Tanjun:** `{tanjun_ver}`",
                        color="#ffe500"))

load_command = component.make_loader()
