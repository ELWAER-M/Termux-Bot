import hikari
import tanjun
from modules import wiki_fetcher 
import typing

component = tanjun.Component()

@component.with_command
@tanjun.with_greedy_argument("sfor", default=None)
@tanjun.with_parser
@tanjun.as_message_command("wiki")
async def wiki_msg(ctx: tanjun.abc.MessageContext, sfor: str) -> None:
    await wiki(ctx, sfor)

@component.with_slash_command
@tanjun.with_str_slash_option("query", "What you want to search", default=None)
@tanjun.as_slash_command("wiki", "Search in termux wiki")
async def wiki_slash(ctx: tanjun.abc.SlashContext, query: typing.Optional[str]) -> None:
    await wiki(ctx, query)

async def wiki(ctx: tanjun.abc.Context, sfor) -> None:
    if sfor:
        w = wiki_fetcher.wiki_s(sfor)
        if w:
            msg = ""
            for x in w:
                msg += f"[{w[x]['title']}]({w[x]['url']})\n"

            await ctx.respond(embed=hikari.Embed(description=msg, color="#00ff00"))
        else:
            await ctx.respond(embed=hikari.Embed(description="There were no results matching the query", color="#ff0000"))
    else:
        await ctx.respond(embed=hikari.Embed(description="Please enter what you want to search for!", color="#ff0000"))

load_command = component.make_loader()
