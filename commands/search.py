import hikari
import tanjun
from modules import package_fetcher
import typing

from hikari.messages import ButtonStyle
from hikari import InteractionCreateEvent

component = tanjun.Component()

@component.with_command
@tanjun.with_argument("repo_n", default="main")
@tanjun.with_argument("arch_n", default="aarch64")
@tanjun.with_argument("query", default=None)
@tanjun.with_parser
@tanjun.as_message_command("search")
async def search_msg(ctx: tanjun.abc.MessageContext, query: str, arch_n: str, repo_n: str, bot: hikari.GatewayBot = tanjun.injected(type=hikari.GatewayBot)) -> None:
    if repo_n not in ["main", "root", "x11"] or arch_n not in ["aarch64", "arm", "i686", "x86_64"]:
        await ctx.respond(embed=hikari.Embed(
            description="the Arch or Repo name are Wrong!",
            color="#ff0000"
            ))
        return
    await search(ctx, bot, query, arch_n, repo_n)

@component.with_slash_command
@tanjun.with_str_slash_option("repo_name", "The repo name", choices=["main", "root", "x11"], default="main")
@tanjun.with_str_slash_option("arch", "The arch name", choices=["aarch64", "arm", "i686", "x86_64"], default="aarch64")
@tanjun.with_str_slash_option("query", "The package name", default=None)
@tanjun.as_slash_command("search", "Search in package descriptions")
async def search_slash(ctx: tanjun.abc.SlashContext, query: typing.Optional[str], arch: typing.Optional[str], repo_name: typing.Optional[str], bot: hikari.GatewayBot = tanjun.injected(type=hikari.GatewayBot)) -> None:
    await search(ctx, bot, query, arch, repo_name)

async def search(ctx: tanjun.abc.Context, bot: hikari.GatewayBot, query, arch_n, repo_n) -> None:
    if query:
        await ctx.respond(embed=hikari.Embed(
            description="Connecting to the repo...",
            color="#ffff00"
            ))

        r = package_fetcher.fetch(arch_n, getattr(package_fetcher, repo_n))

        if not r:
            await ctx.edit_last_response(embed=hikari.Embed(
                description="Failed to connect to the repo",
                color="#ff0000"
                ))
        else:
            msg = [""]
            page = 0
            msg_id = (await ctx.fetch_last_response()).id 

            for x in r:
                if x != "_host" and query != "_host" and query.lower() in r[x]["Package"].lower() or x != "_host" and query != "_host" and query.lower() in r[x]["Description"].lower():
                    if (len(msg[-1]) + len(r[x]["Package"]) + len(r[x]['Version']) + len(r[x]["Description"]) + 10) >= 4096:
                        msg.append("")
                    msg[-1] += f"{r[x]['Package']}/{r[x]['Version']}\n{r[x]['Description']}\n\n"

            if msg == [""]:
                await ctx.edit_last_response(embed=hikari.Embed(
                    description="There were no results matching the query",
                    color="#ff0000"))
                return

            btn = ctx.rest.build_action_row()
            (
                btn.add_button(ButtonStyle.PRIMARY, f"left_{msg_id}")
                .set_emoji("◀")
                .add_to_container()
            )
            (
                btn.add_button(ButtonStyle.PRIMARY, f"right_{msg_id}")
                .set_emoji("▶")
                .add_to_container()
            )
            
            right_btn = ctx.rest.build_action_row()
            (
                right_btn.add_button(ButtonStyle.PRIMARY, f"left_{msg_id}")
                .set_emoji("◀")
                .set_is_disabled(True)
                .add_to_container()
            )
            (
                right_btn.add_button(ButtonStyle.PRIMARY, f"right_{msg_id}")
                .set_emoji("▶")
                .add_to_container()
            )


            left_btn = ctx.rest.build_action_row()
            (
                left_btn.add_button(ButtonStyle.PRIMARY, f"left_{msg_id}")
                .set_emoji("◀")
                .add_to_container()
            )
            (
                left_btn.add_button(ButtonStyle.PRIMARY, f"right_{msg_id}")
                .set_emoji("▶")
                .set_is_disabled(True)
                .add_to_container()
            )

            def get_row():
                if len(msg) == 1:
                    row = []
                elif page == 0:
                    row = [right_btn]
                elif page == msg.index(msg[-1]):
                    row = [left_btn]
                else: 
                    row = [btn]
                return row

            def get_page():
                if len(msg) == 1:
                    _page = None
                else:
                    _page = f"Page {(page+1)} of {len(msg)}"
                return _page

            await ctx.edit_last_response(embed=hikari.Embed(
                description=msg[page],
                color="#00ff00"
                ).set_footer(get_page()),
                components=get_row())

            # don't fucking ask me how this working
            with bot.stream(InteractionCreateEvent, timeout=60) as stream:
                async for event in stream:
                    click = event.interaction.custom_id
                    if click == f"right_{msg_id}":
                        page += 1            
                        await ctx.edit_last_response(embed=hikari.Embed(
                            description=msg[page],
                            color="#00ff00"
                            ).set_footer(get_page()),
                            components=get_row())
                    elif click == f"left_{msg_id}":
                        page -= 1            
                        await ctx.edit_last_response(embed=hikari.Embed(
                            description=msg[page],
                            color="#00ff00"
                            ).set_footer(get_page()),
                            components=get_row())

            await ctx.edit_last_response(components=[])
    else:
        await ctx.respond(embed=hikari.Embed(
            description="Please enter what you want to search for!",
            color="#ff0000"
            ))

load_command = component.make_loader()
