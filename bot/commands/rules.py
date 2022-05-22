import tanjun
import typing

from hikari import Embed

component = tanjun.Component()

@component.with_command
@tanjun.with_argument("rule", default=None)
@tanjun.as_message_command("rules")
async def rules_msg(ctx: tanjun.abc.MessageContext, rule: str) -> None:
    await rules(ctx, rule)

@component.with_slash_command
@tanjun.with_str_slash_option("rule", "Rule number", default=None)
@tanjun.as_slash_command("rules", "Termux discord server rules.")
async def rules_slash(ctx: tanjun.abc.SlashContext, rule: typing.Optional[str]) -> None:
    await rules(ctx, rule)

async def rules(ctx: tanjun.abc.Context, rule) -> None:
    guild = ctx.get_guild()
    if guild is None:
        guild = await ctx.rest.fetch_guild(641256914684084234)
    color = "#5865F2"
    rules = [
            ["Be respectful and kind to people", "That includes: no bullying, no slurs of any kind, no encouraging suicide or any other form of self harm *(Swearing is allowed but at a level that doesn't hurt anyone, don't take it too far!)*"],
            ["No NSFW content at all", "No porn/suggestive/sensitive media/messages allowed"],
            ["Follow Discord ToS", "Selfbots and other things are banned"],
            ["No Hacking", "We don't support or encourage hacking in any forms, and we don't offer help with any illegal activities"],
            ["No Advertising", "Advertising other servers and DM advertising is not allowed. You may only DM a link if the other user agreed to it"],
            ["Please avoid talking about sensitive topics", "Such topics include but is not limited to: politics, war, religion, race, LGBTQ+ and other social issues"],
            ["Exploiting rules is bannable offense", "Please don't do anything bad just because it's not explicitly written here!"]
            ]
    if rule:
        try:
            rule = int(rule)
            if rule > len(rules) or rule < 1:
                raise ValueError
            await ctx.respond(embed=Embed(title=rules[rule-1][0], description=rules[rule-1][1], color=color))
            return
        except ValueError:
                await ctx.respond(embed=Embed(color="#ff0000", description="Please enter a rational number"))
                return

    welcome = Embed(color=color, description="Welcome to the official Termux Discord community, we hope you have fun.")
    welcome.set_author(name=guild.name, icon=guild.icon_url)

    rules_embed = Embed(title="Rules", color=color, description="We recommend you to follow a few rules to keep the community friendly, breaking them may cause a warning/mute/kick/ban depending on the action.")
    for x in rules:
        rules_embed.add_field(name=f"{rules.index(x)+1}. {x[0]}", value=x[1])

    more = Embed(title="For more community rules", color=color, description="Please check our wiki:\nhttps://wiki.termux.com/wiki/Community#Rules")

    faq = Embed(title="For more termux questions", color=color, description="Be sure to read the FAQ before asking any questions:\nhttps://wiki.termux.com/wiki/FAQ")

    bridge = Embed(color=color, description="The __channels__ <#641256914684084237>/<#847704138711171084> are **relayed** to Termux's Gitter**/**IRC - users with `BOT` in their names are being relayed to Discord for us!\n**Keep in mind default Discord replies are not visible to bridged users, so please quote messages and usernames when reffering to bridged users!**")

    links = Embed(title="Links", color=color, description="""
Termux Wiki:
https://wiki.termux.com/wiki/Main_Page
Termux Organization:
https://github.com/termux
Termux App Repository:
https://github.com/termux/termux-app
Termux Packages Repository:
https://github.com/termux/termux-packages
Permanent Invite Link to this server:
https://discord.gg/HXpF69X
    """)

    await ctx.respond(embeds=[welcome, rules_embed, more, faq, bridge, links])

load_command = component.make_loader()
