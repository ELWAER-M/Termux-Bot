import hikari
import tanjun

component = tanjun.Component()


@component.with_command
@tanjun.as_message_command("rules")
async def rules_msg(ctx: tanjun.abc.MessageContext, /) -> None:
    await rules(ctx)

@component.with_slash_command
@tanjun.as_slash_command("rules", "Termux discord server rules")
async def rules_slash(ctx: tanjun.abc.SlashContext) -> None:
    await rules(ctx)

async def rules(ctx: tanjun.abc.Context, /) -> None:
    await ctx.respond(embed=hikari.Embed(
        title="Termux discord server rules",
        description="""
- **Follow the Discord Terms of Service**
We'd recommend to follow the Discord ToS before starting conversation (https://discordapp.com/terms)

- **Be respectful to other people**
Respect other people around you. do not bully or be toxic to somebody, violation of this rule will lead to warn

- **Use Appropriate Topic Channels**
Please use appropriate topic channels, and keep in mind that the #general and #dev channels are bridged to [Gitter/IRC](https://gitter.im/termux/termux) channels and is solely for Termux only so avoid any kinds of topics that isn't relevant to Termux. Termux [General Community rules](https://wiki.termux.com/wiki/Community#rules) apply

- **Avoid Discussions regarding the use of Termux for Disruptive Activity**
Discussions about Termux as a Hacking/Phishing/DDoS activity is strongly discouraged! we do not tolerate any kinds of these topics and provide support for it, please see [Hacking](https://wiki.termux.com/wiki/Hacking) for more information

- **Avoid posting NSFW content and other sensitive topics**
Any kinds of discussion about NSFW and other sensitive topics such as Politics, Religion, Races and LGBTQ+ should be avoided

- **No Advertising and other self-promotion**
Any sorts of advertising and other promotions such as Invite links, advertising bots, nitro gifting are forbidden. you may DM a member only if a user are okay with it

- **Don't ask to ask**
Do not ask questions such as "is anyone there" or "can someone help me". instead, ask your actual question immediately. this saves time and we'll respond right away regarding your issue
(https://dontasktoask.net)

- **Do not randomly mention people for help**
When asking for help. do not randomly mention people for help, they may or may not know about your issue. just ask and let someone respond regarding your issue

- **Trolling, Flood, and other types of spam are not tolerated**
little trolling is fine but such behavior that disrupt the conversation aren't tolerated here. and will result in kick or permanent ban
        """
        ))

@tanjun.as_loader
def load_examples(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())
