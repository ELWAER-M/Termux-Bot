import hikari
import tanjun
from modules import package_fetcher

component = tanjun.Component()

@component.with_command
@tanjun.with_argument("repo_n", default="main")
@tanjun.with_argument("arch_n", default="aarch64")
@tanjun.with_argument("pkg_n", default=None)
@tanjun.with_parser
@tanjun.as_message_command("pkg", "apt")
async def pkg(ctx: tanjun.abc.Context, pkg_n: str, arch_n: str, repo_n: str) -> None:
    if repo_n not in package_fetcher.all_repos or arch_n not in package_fetcher.archs:
        await ctx.respond(embed=hikari.Embed(
            description="the Arch or Repo name are Wrong!",
            color="#ff0000"
            ), reply=True)
        return

    if pkg_n:
        await ctx.respond(embed=hikari.Embed(
            description="Connecting to [packages.termux.org](https://packages.termux.org/)...",
            color="#ffff00"
            ), reply=True)

        p = package_fetcher.fetch(pkg_n, arch_n, getattr(package_fetcher, repo_n))

        if p:
            pkg_embed = hikari.Embed(color="#00ff00")
            pkg_embed.add_field(name="Package name:", value=p["Package"])
            pkg_embed.add_field(name="Description:", value=p["Description"])
            pkg_embed.add_field(name="Version:", value=p["Version"])
            pkg_embed.add_field(name="Size:", value=f'{"{:.2f}".format(int(p["Size"])/1024/1024)} MB')
            pkg_embed.add_field(name="Installation:", value=f"```\napt install {p['Package']}\n```")
            pkg_embed.add_field(name="Links:", value=f"[Homepage]({p['Homepage']}) | [Download .deb]({getattr(package_fetcher, repo_n)['repo_url']}/{p['Filename']})")
            await ctx.edit_last_response(embed=pkg_embed)
        else:
            await ctx.edit_last_response(embed=hikari.Embed(
                description=f"E: Unable to locate package {pkg_n}",
                color="#ff0000"
                ))
    else:
        await ctx.respond(embed=hikari.Embed(
            description="Please enter the package name!\n||hint: `$apt/pkg <Package name*> <Arch> <Repo>`||",
            color="#ff0000"
            ), reply=True)
        
@tanjun.as_loader
def load_examples(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())
