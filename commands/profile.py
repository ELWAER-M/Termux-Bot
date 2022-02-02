import hikari
import tanjun
from datetime import datetime
import motor.motor_asyncio as motor
import typing

component = tanjun.Component()

@component.with_command
@tanjun.with_greedy_argument("arg3", default=None)
@tanjun.with_argument("arg2", default=None)
@tanjun.with_argument("arg", default=None)
@tanjun.as_message_command("profile")
async def profile_msg(ctx: tanjun.abc.MessageContext, arg: str, arg2: str, arg3: str, bot: hikari.GatewayBot = tanjun.inject(type=hikari.GatewayBot), mongo: motor.AsyncIOMotorClient = tanjun.inject(type=motor.AsyncIOMotorClient)) -> None:
    if arg and arg != "setup" and arg != "edit":
        try:
            member = await tanjun.to_member(arg, ctx=ctx)
        except:
            await ctx.respond(embed=hikari.Embed(
                                description=f"Can't find this user **{arg}**",
                                color="#ff0000"))
            return
    else:
        member = ctx.member

    if member == None:
        assert ctx.guild_id
        member = await ctx.rest.fetch_member(ctx.guild_id, ctx.author.id)

    if member.is_bot:
        await ctx.respond(embed=hikari.Embed(
                            description="This command only for users not bots!",
                            color="#ff0000"))
        return

    if arg == "setup":
        await setup_profile(ctx, member, bot, mongo)
        return

    if arg == "edit":
        edit_args = ["des", "description", "android", "build", "lang", "language", "device"]
        if arg2 and arg2 in edit_args:
            if not arg3:
                await ctx.respond(embed=hikari.Embed(
                                    description="You need to add a value for it",
                                    color="#ff0000"))
                return

            await edit_profile(ctx, member, mongo, arg2, arg3)
            return
        else:
            await ctx.respond(embed=hikari.Embed(
                                title="Profile editing arguments",
                                description="`des/description`\n`android`\n`build`\n`lang/language`\n`device`",
                                color="#ffe500"))
            return

    await profile(ctx, member, mongo)

@component.with_slash_command
@tanjun.with_member_slash_option("member", "member", default=None)
@tanjun.as_slash_command("profile", "Show user profile")
async def profile_slash(ctx: tanjun.abc.SlashContext, member: hikari.Member, mongo: motor.AsyncIOMotorClient = tanjun.inject(type=motor.AsyncIOMotorClient)) -> None:
    if member:
        user_ = member
    else:
        user_ = ctx.member

    if user_ == None:
        assert ctx.guild_id
        user_ = await ctx.rest.fetch_member(ctx.guild_id, ctx.author.id)

    if user_.is_bot:
        await ctx.respond(embed=hikari.Embed(
                            description="This command only for users not bots!",
                            color="#ff0000"))
        return

    await profile(ctx, user_, mongo)

@component.with_slash_command
@tanjun.as_slash_command("profile-setup", "Setup Your profile")
async def profile_setup_slash(ctx: tanjun.abc.SlashContext, bot: hikari.GatewayBot = tanjun.inject(type=hikari.GatewayBot), mongo: motor.AsyncIOMotorClient = tanjun.inject(type=motor.AsyncIOMotorClient)) -> None:
    user_ = ctx.member

    if user_ == None:
        assert ctx.guild_id
        user_ = await ctx.rest.fetch_member(ctx.guild_id, ctx.author.id)

    await setup_profile(ctx, user_, bot, mongo)

@component.with_slash_command
@tanjun.with_str_slash_option("new_value", "The new value you want to set", default=None)
@tanjun.with_str_slash_option("part", "What part of your profile you want to edit.", choices=["description", "android", "build", "language", "device"], default=None)
@tanjun.as_slash_command("profile-edit", "Editing Your profile")
async def profile_edit_slash(ctx: tanjun.abc.SlashContext, part: typing.Optional[str], new_value: typing.Optional[str], mongo: motor.AsyncIOMotorClient = tanjun.inject(type=motor.AsyncIOMotorClient)) -> None:
    user_ = ctx.member

    if user_ == None:
        assert ctx.guild_id
        user_ = await ctx.rest.fetch_member(ctx.guild_id, ctx.author.id)

    if part == None or new_value == None:
        await ctx.respond(embed=hikari.Embed(
                        description="Missed arguments",
                        color="#ff0000"))
        return

    await edit_profile(ctx, user_, mongo, part, new_value)


async def profile(ctx: tanjun.abc.Context, member: hikari.Member, mongo: motor.AsyncIOMotorClient) -> None:
    db = mongo.profiles.main
    find = await db.find_one({"user_id": member.id})
    if not find:
        if member.id == ctx.author.id:
            await ctx.respond(embed=hikari.Embed(
                                description="You don't have a profile yet!, use `$profile setup` to make one.",
                                color="#ff0000"))
            return
        else:
            await ctx.respond(embed=hikari.Embed(
                                description=f"**{member.username}** don't have a profile yet!",
                                color="#ff0000"))
            return
    data = find
    persence = member.get_presence()
    top_role = member.get_top_role()

    embed = hikari.Embed(color=(top_role.color if top_role else None))
    embed.set_author(name=member.username, icon=member.avatar_url)
    embed.set_thumbnail(member.avatar_url)

    profile_info_msg = ""

    if data["des"] != "None":
        profile_info_msg += f"**Description:** {data['des']}"
    if data["an_ver"] != "None":
        profile_info_msg +=f"\n**Android Version:** {data['an_ver']}"
    if data["t_b"] != "None":
        profile_info_msg += f"\n**Termux Build:** {data['t_b']}"
    if data["lang"] != "None":
        profile_info_msg += f"\n**Language:** {data['lang']}"
    if data["dev"] != "None":
        profile_info_msg += f"\n**Device:** {data['dev']}"

    if profile_info_msg != "":
        embed.add_field("About:", value=profile_info_msg)

    account_info = ""

    account_info += f"**Username:** {member.user}"
    account_info += f"\n**ID:** {member.id}"
    account_info += f"\n**Status:** {persence.visible_status if persence else 'offline'}"
    account_info += f"\n**Created at:** {member.created_at.date().strftime('%Y/%m/%d')} ({(datetime.now().date() - member.created_at.date()).days} Days ago)"
    account_info += f"\n**Joined at:** {member.joined_at.date().strftime('%Y/%m/%d')} ({(datetime.now().date() - member.joined_at.date()).days} Days ago)"
    account_info += f"\n**Highest Role:** {(top_role.name if top_role else 'None')}"

    embed.add_field("Account:", account_info)

    await ctx.respond(embed=embed)

async def setup_profile(ctx: tanjun.abc.Context, member: hikari.Member, bot: hikari.GatewayBot, mongo: motor.AsyncIOMotorClient) -> None:
    await ctx.respond(content="wait a min...")

    db = mongo.profiles.main

    data = {}
    data["user_id"] = member.id

    try:
        with bot.stream(hikari.GuildMessageCreateEvent, timeout=60).filter(('author', ctx.author)) as stream:
            await ctx.edit_last_response(content="What android version you use? (if you using a custom rom you can pass that too)")
            async for event in stream:
                data["an_ver"] = str(event.content)[:30]
                await event.message.delete()
                break
            else:
                raise TimeoutError
            await ctx.edit_last_response(content="What termux build you use? (ex: F-Droid, Github)")
            async for event in stream:
                data["t_b"] = str(event.content)[:30]
                await event.message.delete()
                break
            else:
                raise TimeoutError
            await ctx.edit_last_response(content="What device you have? (ex: Galaxy S21, Redmi Note 11)")
            async for event in stream:
                data["dev"] = str(event.content)[:50]
                await event.message.delete()
                break
            else:
                raise TimeoutError
            await ctx.edit_last_response(content="What language/s you speak? (ex: English, Russian or if you don't like that pass `None`)") 
            async for event in stream:
                data["lang"] = str(event.content)[:100]
                await event.message.delete()
                break
            else:
                raise TimeoutError
            await ctx.edit_last_response(content="Add a description to your profile (pass `None` if you don't want that)")
            async for event in stream:
                data["des"] = str(event.content)[:200]
                await event.message.delete()
                break
            else:
                raise TimeoutError
    except TimeoutError:
        await ctx.edit_last_response("Timeout! please try again...")
        return
    find = await db.find_one({"user_id": member.id})
    if find:
        await db.replace_one({"user_id": member.id}, data)
    else:
        await db.insert_one(data)
    await ctx.edit_last_response(content="Alright!! use `$profile` to see your profile")

async def edit_profile(ctx: tanjun.abc.Context, member: hikari.Member, mongo: motor.AsyncIOMotorClient, w: str, new: str):
    db = mongo.profiles.main
    find = await db.find_one({"user_id": member.id})
    if not find:
        if member.id == ctx.author.id:
            await ctx.respond(embed=hikari.Embed(
                                description="You don't have a profile yet!, use `$profile setup` to make one.",
                                color="#ff0000"))
            return
        else:
            await ctx.respond(embed=hikari.Embed(
                                description=f"**{member.username}** don't have a profile yet!",
                                color="#ff0000"))
            return

    if w == "description":w = "des"
    if w == "language": w = "lang"
    if w == "device": w = "dev"
    if w == "android": w = "an_ver"
    if w == "build": w = "t_b"

    max_len = {
            "des": 200,
            "an_ver": 30,
            "dev": 50,
            "lang": 100,
            "t_b": 30
            }

    await db.update_one({"user_id": member.id}, {"$set": {w: new[:max_len[w]]}})

    await ctx.respond(embed=hikari.Embed(
                        description="Edits saved!, do `$profile` to see them",
                        color="#00ff00"))

load_command = component.make_loader()
