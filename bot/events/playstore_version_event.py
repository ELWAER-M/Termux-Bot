import hikari
import tanjun
from hikari import Embed
import os

import io
import requests
from PIL import Image
import pytesseract

if "DYNO" in os.environ:
    pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'

config = r"--psm 6"
filtered = ["N: Metadata integrity can't be verified", "N: Possible cause: repository is under maintenance", "(wrong sources.list URL?)"]
warn_embed = Embed(
        title="Termux on playstore",
        description="""
**Google Play Store builds are deprecated!**

Termux and its plugins are no longer updated on Google Play Store due to android 10 issues and have been deprecated. The last version released for Android >= 7 was v0.101. **It is highly recommended to not install Termux apps from Play Store any more**.

There are plans for unpublishing the Termux app and all its plugins on Play Store soon so that new users cannot install it and for disabling the Termux apps with updates so that existing users **cannot continue using outdated versions**. You are encouraged to move to F-Droid or Github builds as soon as possible.

You can backup all your data under $HOME/ and $PREFIX/ before changing installation source, and then restore it afterwards, by following instructions at Backing up Termux before the uninstallation.

[Termux on F-Droid](https://f-droid.org/en/packages/com.termux/)

Before installing the fresh versions from F-Droid, open your Android OS settings —> Applications. Find all applications named Termux, Termux:API, Termux:Styling, Termux:Widget, Termux:Task, Termux:Float, Termux:Boot and uninstall all of them - yes, including paid ones.

In replacement for https://github.com/termux/termux-packages/issues/6726.
        """)

component = tanjun.Component()

@component.with_listener(hikari.GuildMessageCreateEvent)
async def on_message_sent(event: hikari.GuildMessageCreateEvent) -> None:
    message = event.message
    if message.author.is_bot: return

    if att := message.attachments:
        for x in att:
            if "image" not in str(x.media_type): break

            img_url = x.url
            res = requests.get(img_url)
            img = Image.open(io.BytesIO(res.content))
            text = pytesseract.image_to_string(img, config=config)

            if all(x in text for x in filtered):
                await message.respond(embed=warn_embed, reply=True, mentions_reply=True)
                return

    if cnt := message.content:
        if all(x in cnt for x in filtered):
            await message.respond(embed=warn_embed, reply=True, mentions_reply=True)
                                                        

load_event = component.make_loader()
