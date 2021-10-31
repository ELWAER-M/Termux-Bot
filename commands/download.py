import hikari
import tanjun
from modules import github_build

component = tanjun.Component()

@component.with_command
@tanjun.as_message_command("download")
async def download(ctx: tanjun.abc.Context, /) -> None:
    embed = hikari.Embed(
            title="Download Termux",
            description=f"[F-Droid](https://f-droid.org/packages/com.termux/) (Recommended)\n[Last Github Builds]({github_build.last_build()})"
            )

    await ctx.respond(embed=embed, reply=True)

@tanjun.as_loader
def load_examples(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())
