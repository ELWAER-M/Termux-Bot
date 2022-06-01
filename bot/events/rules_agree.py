import hikari
import tanjun
from hikari import Embed

component = tanjun.Component()

@component.with_listener(hikari.InteractionCreateEvent)
async def on_message_sent(event: hikari.PartialInteraction) -> None:
    print(event)

load_event = component.make_loader()
