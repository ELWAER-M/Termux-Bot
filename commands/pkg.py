import hikari
import tanjun
from modules import package_fetcher
import typing

component = tanjun.Component()

@component.with_command
@tanjun.with_argument("repo_n", default="main")
@tanjun.with_argument("arch_n", default="aarch64")
@tanjun.with_argument("pkg_n", default=None)
@tanjun.with_parser
@tanjun.as_message_command("pkg", "apt")
async def pkg_msg(ctx: tanjun.abc.MessageContext, pkg_n: str, arch_n: str, repo_n: str) -> None:
    if repo_n not in ["main", "root", "science", "game", "x11"] or arch_n not in ["aarch64", "arm", "i686", "x86_64"]:
        await ctx.respond(embed=hikari.Embed(
            description="the Arch or Repo name are Wrong!",
            color="#ff0000"
            ))
        return
    await pkg(ctx, pkg_n, arch_n, repo_n)

@component.with_slash_command
@tanjun.with_str_slash_option("repo_name", "The repo name", choices={"main", "root", "science", "game", "x11"}, default="main")
@tanjun.with_str_slash_option("arch", "The arch name", choices={"aarch64", "arm", "i686", "x86_64"}, default="aarch64")
@tanjun.with_str_slash_option("package_name", "The package name", default=None)
@tanjun.as_slash_command("pkg", "Gives you information about packages")
async def pkg_slash(ctx: tanjun.abc.SlashContext, package_name: typing.Optional[str], arch: typing.Optional[str], repo_name: typing.Optional[str]) -> None:
    await pkg(ctx, package_name, arch, repo_name)

async def pkg(ctx: tanjun.abc.Context, pkg_n, arch_n, repo_n) -> None:
    if pkg_n:
        await ctx.respond(embed=hikari.Embed(
            description="Connecting to [packages.termux.org](https://packages.termux.org/)...",
            color="#ffff00"
            ))

        p = package_fetcher.fetch(pkg_n, arch_n, getattr(package_fetcher, repo_n))

        if p == "err1":
            await ctx.edit_last_response(embed=hikari.Embed(
                description="Failed to connect to the repo",
                color="#ff0000"
                ))
        elif p == "err2":
            await ctx.edit_last_response(embed=hikari.Embed(
                description="Disconnected from the repo",
                color="#ff0000"
                ))
        elif p == "err3":
            await ctx.edit_last_response(embed=hikari.Embed(
                description=f"Unable to locate package {pkg_n}",
                color="#ff0000"
                ))
        else:
            pkg_embed = hikari.Embed(color="#00ff00")
            pkg_embed.add_field(name="Package name:", value=p["Package"])
            pkg_embed.add_field(name="Description:", value=p["Description"])
            pkg_embed.add_field(name="Version:", value=p["Version"])
            # pkg_embed.add_field(name="Dependencies:", value=p["Depends"])
            pkg_embed.add_field(name="Size:", value=f'{"{:.2f}".format(int(p["Size"])/1024/1024)} MB')
            pkg_embed.add_field(name="Maintainer:", value=p["Maintainer"])
            pkg_embed.add_field(name="Installation:", value=f"```\napt install {p['Package']}\n```")
            pkg_embed.add_field(name="Links:", value=f"[Homepage]({p['Homepage']}) | [Download .deb]({getattr(package_fetcher, repo_n)['repo_url']}/{p['Filename']})")
            await ctx.edit_last_response(embed=pkg_embed)
    else:
        await ctx.respond(embed=hikari.Embed(
            description="Please enter the package name!",
            color="#ff0000"
            ))
        
@tanjun.as_loader
def load_examples(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())
