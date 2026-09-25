from pyrogram import Client, filters
from pyrogram.types import Message
from bot import is_admin, get_stats_counts

@Client.on_message(filters.command("users") & filters.group)
async def total_users_command(client: Client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if not await is_admin(client, chat_id, user_id):
        await message.reply_text("❌ Only group administrators can check bot statistics.")
        return

    total_count, muted_count, banned_count = await get_stats_counts()

    await message.reply_text(
        f"📊 **Bot Analytics & Moderation Statistics**\n\n"
        f"👥 **Total Unique Users Tracked:** `{total_count}`\n"
        f"🔒 **Currently Muted Users:** `{muted_count}`\n"
        f"🔨 **Total Banned Users:** `{banned_count}`"
    )
