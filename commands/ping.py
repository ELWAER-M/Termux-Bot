import hikari
import tanjun
import time

component = tanjun.Component()


@component.with_command
@tanjun.as_message_command("ping")
async def ping_msg(ctx: tanjun.abc.MessageContext, /) -> None:
    await ping(ctx)

@component.with_slash_command
@tanjun.as_slash_command("ping", "Ping test.")
async def ping_slash(ctx: tanjun.abc.SlashContext) -> None:
    await ping(ctx)

async def ping(ctx: tanjun.abc.Context, /) -> None:
    start_time = time.perf_counter()
    await ctx.respond(embed=hikari.Embed(
        description="Pong! 🏓",
        color="#ffff00"
        ))
    time_taken = (time.perf_counter() - start_time) * 1_000
    heartbeat_latency = ctx.shards.heartbeat_latency * 1_000 if ctx.shards else float("NAN")
    await ctx.edit_last_response(embed=hikari.Embed(
        description=f"Pong! 🏓\nREST: {time_taken:.0f}ms\nGateway: {heartbeat_latency:.0f}ms",
        color="#00ff00"
        ))

load_command = component.make_loader()
