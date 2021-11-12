import hikari
import tanjun

component = tanjun.Component()

fucking_commands_are_not_supposed_to_show = ["rules"]

@component.with_command
@tanjun.as_message_command("help")
async def help_msg(ctx: tanjun.abc.MessageContext, bot: hikari.GatewayBotAware = tanjun.injected(type=hikari.GatewayBotAware)) -> None:
    await help(ctx, bot)

@component.with_slash_command
@tanjun.as_slash_command("help", "Show commands help list")
async def help_slash(ctx: tanjun.abc.SlashContext, bot: hikari.GatewayBotAware = tanjun.injected(type=hikari.GatewayBotAware)) -> None:
    await help(ctx, bot)

async def help(ctx: tanjun.abc.Context, bot) -> None:
    embed = hikari.Embed()
    embed.set_author(name=bot.get_me().username, icon=bot.get_me().avatar_url)
    embed.add_field(name="Prefix:", value=", ".join(f"`{x}`" for x in ctx.client.prefixes))
    embed.add_field(name="Commands:", value=", ".join(filter(None, (f"`{'/'.join(x.names)}`" if any(cmd in no for no in x.names for cmd in fucking_commands_are_not_supposed_to_show) != True else "" for x in ctx.client.iter_message_commands()))))
    embed.add_field(name="Links:", value="[Github Repository](https://github.com/ELWAER-M/Termux-Bot)\n[Termux Discord Server](https://discord.gg/HXpF69X)")
    
    await ctx.respond(embed=embed)

@tanjun.as_loader
def load_examples(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())
