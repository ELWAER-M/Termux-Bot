import hikari
import tanjun

component = tanjun.Component()

@component.with_command
@tanjun.as_message_command("help")
async def help(ctx: tanjun.abc.Context, bot: hikari.traits.GatewayBotAware = tanjun.injected(type=hikari.traits.GatewayBotAware)) -> None:
    cl = []

    for x in ctx.client.iter_message_commands():
        if len(x.names) > 1:
            cl.append(f"`{'/'.join(x.names)}`")
        else:
            cl.append(f"`{''.join(x.names)}`")
    msg = ', '.join(cl)

    embed = hikari.Embed()
    embed.set_author(name=bot.get_me().username, icon=bot.get_me().avatar_url)
    embed.add_field(name="Prefix:", value=f"`{''.join(ctx.client.prefixes)}`")
    embed.add_field(name="Commands:", value=msg)
    embed.add_field(name="Links:", value="[Github Repository](https://github.com/ELWAER-M/Termux-Bot)\n[Termux Discord Server](https://discord.gg/HXpF69X)")
    
    await ctx.respond(embed=embed, reply=True)

@tanjun.as_loader
def load_examples(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())
