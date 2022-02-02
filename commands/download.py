import hikari
import tanjun
# from modules import github_build

component = tanjun.Component()


@component.with_command
@tanjun.as_message_command("download")
async def download_msg(ctx: tanjun.abc.MessageContext, /) -> None:
    await download(ctx)

@component.with_slash_command
@tanjun.as_slash_command("download", "Termux download mirrors.")
async def download_slash(ctx: tanjun.abc.SlashContext) -> None:
    await download(ctx)

async def download(ctx: tanjun.abc.Context, /) -> None:
    # gh = github_build.last_build()

    embed = hikari.Embed(
            title="Download Termux",
            description=f"[F-Droid](https://f-droid.org/packages/com.termux/)\n[Github](https://github.com/termux/termux-app/releases)"
            )

    await ctx.respond(embed=embed)

load_command = component.make_loader()
