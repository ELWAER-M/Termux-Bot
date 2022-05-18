import tanjun
import typing

from hikari import Embed
from modules import package_fetcher

component = tanjun.Component()

@component.with_command
@tanjun.with_argument("repo_n", default="main")
@tanjun.with_argument("arch_n", default="aarch64")
@tanjun.with_argument("pkg_n", default=None)
@tanjun.with_parser
@tanjun.as_message_command("pkg", "apt")
async def pkg_msg(ctx: tanjun.abc.MessageContext, pkg_n: str, arch_n: str, repo_n: str) -> None:
    if repo_n not in ["main", "root", "x11"] or arch_n not in ["aarch64", "arm", "i686", "x86_64"]:
        await ctx.respond(embed=Embed(
            description="the Arch or Repo name are Wrong!",
            color="#ff0000"
            ))
        return
    await pkg(ctx, pkg_n, arch_n, repo_n)

@component.with_slash_command
@tanjun.with_str_slash_option("repo_name", "The repo name", choices=["main", "root", "x11"], default="main")
@tanjun.with_str_slash_option("arch", "The arch name", choices=["aarch64", "arm", "i686", "x86_64"], default="aarch64")
@tanjun.with_str_slash_option("package_name", "The package name", default=None)
@tanjun.as_slash_command("pkg", "show package details")
async def pkg_slash(ctx: tanjun.abc.SlashContext, package_name: typing.Optional[str], arch: typing.Optional[str], repo_name: typing.Optional[str]) -> None:
    await pkg(ctx, package_name, arch, repo_name)

async def pkg(ctx: tanjun.abc.Context, pkg_n, arch_n, repo_n) -> None:
    if pkg_n:
        await ctx.respond(embed=Embed(
            description="Connecting to the repository...",
            color="#ffff00"
            ))

        r = package_fetcher.fetch(arch_n, repo_n)
        ct = lambda x, y: x[y-3] + "..." if len(x) > y else x

        if not r:
            await ctx.edit_last_response(embed=Embed(
                description="Failed to connect to the repository!",
                color="#ff0000"
                ))
        elif pkg_n in r and pkg_n != "_host":
            pkg_embed = Embed(color="#00ff00")
            pkg_embed.add_field(name="Package name:", value=r[pkg_n]["Package"])
            pkg_embed.add_field(name="Description:", value=ct(r[pkg_n]["Description"], 500))
            pkg_embed.add_field(name="Version:", value=ct(r[pkg_n]["Version"], 200))
            if "Depends" in r[pkg_n]:
                pkg_embed.add_field(name="Dependencies:", value=ct(", ".join(f"`{x}`" for x in r[pkg_n]["Depends"].split(", ")), 2500))
            pkg_embed.add_field(name="Size:", value=f"{int(r[pkg_n]['Size'])/1024/1024:.2f} MB")
            pkg_embed.add_field(name="Maintainer:", value=ct(r[pkg_n]["Maintainer"], 300))
            pkg_embed.add_field(name="Installation:", value=f"```\napt install {r[pkg_n]['Package']}\n```")
            pkg_embed.add_field(name="Links:", value=f"[Homepage]({r[pkg_n]['Homepage']}) | [Download .deb]({r['_host']['url']}/{r[pkg_n]['Filename']})")
            pkg_embed.set_footer(text=f"Connected to {r['_host']['host_name']}")
            await ctx.edit_last_response(embed=pkg_embed)
        else:
            await ctx.edit_last_response(embed=Embed(
                description=f"Unable to locate package `{pkg_n}`",
                color="#ff0000"
                ))
    else:
        await ctx.respond(embed=Embed(
            description="Please enter the package name!",
            color="#ff0000"
            ))

load_command = component.make_loader()
