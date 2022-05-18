import hikari
import tanjun

component = tanjun.Component()

@component.with_command
@tanjun.as_message_command("help")
async def help_msg(ctx: tanjun.abc.MessageContext) -> None:
    await help(ctx)

@component.with_slash_command
@tanjun.as_slash_command("help", "Show commands help list")
async def help_slash(ctx: tanjun.abc.SlashContext) -> None:
    await help(ctx)

async def help(ctx: tanjun.abc.Context) -> None:
    bot = await ctx.rest.fetch_my_user()

    embed = hikari.Embed()
    embed.set_author(name=bot.username, icon=bot.avatar_url)
    embed.add_field(name="Prefix:", value=", ".join(f"`{x}`" for x in ctx.client.prefixes))
    embed.add_field(name="Commands:", value=", ".join(filter(None, (f"`{'/'.join(x.names)}`" for x in ctx.client.iter_message_commands()))))
    embed.add_field(name="Links:", value="[Github Repository](https://github.com/ELWAER-M/Termux-Bot)\n[Termux Discord Server](https://discord.gg/HXpF69X)")
    
    await ctx.respond(embed=embed)

load_command = component.make_loader()
