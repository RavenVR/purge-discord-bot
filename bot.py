import hikari
from hikari import PermissionOverwrite, PermissionOverwriteType, Permissions, snowflakes
import lightbulb
import asyncio
import datetime

token = "bot token here"
guild_id = guild id here

mod = moderator-role-id

bot = lightbulb.BotApp(
    token=token, default_enabled_guilds=(guild_id), intents=hikari.Intents.ALL
)
bot.command()
@lightbulb.option(
    "count",
    "The amount of messages to purge.",
    type=int,
    max_value=1000000,
    min_value=1,
)
@lightbulb.command(
    "purge", "Purge a certain amount of messages from a channel.", pass_options=True
)
@lightbulb.implements(lightbulb.SlashCommand)
async def purge(ctx: lightbulb.SlashContext, count: int) -> None:
    member = ctx.get_guild().get_member(ctx.author.id)

    role = ctx.get_guild().get_role(mod)
    if role in await member.fetch_roles():
        """Purge a certain amount of messages from a channel."""
        if not guild_id:
            await ctx.respond("This command can only be used in a server.")
            return

        messages = (
            await ctx.app.rest.fetch_messages(ctx.channel_id)
            .take_until(
                lambda m: datetime.datetime.now(datetime.timezone.utc)
                - datetime.timedelta(days=14)
                > m.created_at
            )
            .limit(count)
        )
        if messages:
            await ctx.app.rest.delete_messages(ctx.channel_id, messages)
            await ctx.respond(f"Purged {len(messages)} messages.")
            asyncio.sleep(2)
            await ctx.delete_last_response()
        else:
            await ctx.respond("Could not find any messages younger than 14 days!")
    else:
        await ctx.respond("You do not have permission to run this command!")



bot.run(
    status=hikari.Status.ONLINE,
    activity=hikari.Activity(
        name="/purge",
        type=hikari.ActivityType.WATCHING,
    ),
)
