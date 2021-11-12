import hikari
import tanjun

component = tanjun.Component()


@component.with_command
@tanjun.as_message_command("playstore")
async def playstore_msg(ctx: tanjun.abc.MessageContext, /) -> None:
    await playstore(ctx)

@component.with_slash_command
@tanjun.as_slash_command("playstore", "Information about what happening with play store version of termux")
async def playstore_slash(ctx: tanjun.abc.SlashContext) -> None:
    await playstore(ctx)

async def playstore(ctx: tanjun.abc.Context, /) -> None:
    await ctx.respond(embed=hikari.Embed(
        title="Termux on playstore",
        description="""
**Google Play Store builds are deprecated!**

Termux and its plugins are no longer updated on Google Play Store due to android 10 issues and have been deprecated. The last version released for Android >= 7 was v0.101. **It is highly recommended to not install Termux apps from Play Store any more**.

There are plans for unpublishing the Termux app and all its plugins on Play Store soon so that new users cannot install it and for disabling the Termux apps with updates so that existing users **cannot continue using outdated versions**. You are encouraged to move to F-Droid or Github builds as soon as possible.

You can backup all your data under $HOME/ and $PREFIX/ before changing installation source, and then restore it afterwards, by following instructions at Backing up Termux before the uninstallation.

[Termux on F-Droid](https://f-droid.org/en/packages/com.termux/)

Before installing the fresh versions from F-Droid, open your Android OS settings —> Applications. Find all applications named Termux, Termux:API, Termux:Styling, Termux:Widget, Termux:Task, Termux:Float, Termux:Boot and uninstall all of them - yes, including paid ones.

In replacement for https://github.com/termux/termux-packages/issues/6726.
        """
        ))

@tanjun.as_loader
def load_examples(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())
