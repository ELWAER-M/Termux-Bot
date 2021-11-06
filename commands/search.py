import hikari
import tanjun
import typing
from modules import package_fetcher

component = tanjun.Component()

@component.with_command
@tanjun.with_argument("repo_n", default="main")
@tanjun.with_argument("arch_n", default="aarch64")
@tanjun.with_argument("query", default=None)
@tanjun.with_parser
@tanjun.as_message_command("search")
async def seach_msg(ctx: tanjun.abc.MessageContext, query: str, arch_n: str, repo_n: str) -> None:
    if repo_n not in ["main", "root", "science", "game", "x11"] or arch_n not in ["aarch64", "arm", "i686", "x86_64"]:
        await ctx.respond(embed=hikari.Embed(
            description="the Arch or Repo name are Wrong!",
            color="#ff0000"
            ))
        return
    await search(ctx, query, arch_n, repo_n)

@component.with_slash_command
@tanjun.with_str_slash_option("repo_name", "The repo name", choices={"main", "root", "science", "game", "x11"}, default="main")
@tanjun.with_str_slash_option("arch", "The arch name", choices={"aarch64", "arm", "i686", "x86_64"}, default="aarch64")
@tanjun.with_str_slash_option("query", "What you want to search", default=None)
@tanjun.as_slash_command("search", "Search in package descriptions")
async def search_slash(ctx: tanjun.abc.SlashContext, query: typing.Optional[str], arch: typing.Optional[str], repo_name: typing.Optional[str]) -> None:
    await search(ctx, query, arch, repo_name)

async def search(ctx: tanjun.abc.Context, sfor, arch_n, repo_n) -> None:
    if sfor:
        await ctx.respond(embed=hikari.Embed(
            description="Connecting to [packages.termux.org](https://packages.termux.org/)...",
            color="#ffff00"
            ))

        r = package_fetcher.search(sfor, arch_n, getattr(package_fetcher, repo_n))

        if r == "err1":
            await ctx.edit_last_response(embed=hikari.Embed(
                description="Failed to connect to the repo",
                color="#ff0000"
                ))
        elif r == "err2":
            await ctx.edit_last_response(embed=hikari.Embed(
                description="Disconnected from the repo",
                color="#ff0000"
                ))
        elif r == "err3":
            await ctx.edit_last_response(embed=hikari.Embed(
                description=f"There were no results matching the query",
                color="#ff0000"
                ))
        else:
            msg = ""
            for x in r:
                msg += f"{x}/{r[x]['Version']}\n  {r[x]['Description']}\n\n"
            await ctx.edit_last_response(embed=hikari.Embed(
                title="Search Results",
                description=msg,
                color="#00ff00"
                ))
    else:
        await ctx.respond(embed=hikari.Embed(
            description="Please enter the package name!",
            color="#ff0000"
            ))
@tanjun.as_loader
def load_examples(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())
