import hikari
import tanjun
from modules import wiki_fetcher 

component = tanjun.Component()

@component.with_command
@tanjun.with_greedy_argument("sfor", default=None)
@tanjun.with_parser
@tanjun.as_message_command("wiki")
async def wiki(ctx: tanjun.abc.Context, sfor: str) -> None:
    if sfor:
        w = wiki_fetcher.wiki_s(sfor)
        if w:
            msg = ""
            for x in w:
                msg += f"[{w[x]['title']}]({w[x]['url']})\n"

            await ctx.respond(embed=hikari.Embed(description=msg, color="#00ff00"), reply=True)
        else:
            await ctx.respond(embed=hikari.Embed(description="There were no results matching the query", color="#ff0000"), reply=True)
    else:
        await ctx.respond(embed=hikari.Embed(description="Please enter what you want to search for!", color="#ff0000"), reply=True)

@tanjun.as_loader
def load_examples(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())
