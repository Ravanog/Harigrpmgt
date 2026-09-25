from pyrogram import Client, filters
from pyrogram.types import Message
from bot import is_admin, get_stats_counts, db

groups_col = db["connected_groups"]

@Client.on_message(filters.command("users") & filters.group)
async def total_users_command(client: Client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if not await is_admin(client, chat_id, user_id):
        await message.reply_text("❌ Only group administrators can check bot statistics.")
        return

    # Unpack all 4 values returned by get_stats_counts()
    total_count, muted_count, banned_count, group_count = await get_stats_counts()

    await message.reply_text(
        f"📊 **Bot Analytics & Moderation Statistics**\n\n"
        f"🏢 **Connected Groups:** `{group_count}`\n"
        f"👥 **Total Unique Users Tracked:** `{total_count}`\n"
        f"🔒 **Currently Muted Users:** `{muted_count}`\n"
        f"🔨 **Total Banned Users:** `{banned_count}`"
    )

@Client.on_message(filters.command("groups") & (filters.group | filters.private))
async def connected_groups_list_command(client: Client, message: Message):
    from config import ADMINS
    if message.from_user.id not in ADMINS:
        await message.reply_text("❌ This command is restricted to bot administrators only.")
        return

    cursor = groups_col.find({})
    groups = await cursor.to_list(length=None)
    
    total_groups = len(groups)
    
    if total_groups == 0:
        await message.reply_text("📂 My bot is currently not connected to any groups.")
        return

    group_lines = []
    for idx, g in enumerate(groups[:30], 1):
        title = g.get("title", "Unknown Group")
        chat_id = g.get("chat_id")
        group_lines.append(f"{idx}. **{title}** (`{chat_id}`)")

    text = (
        f"📋 **Connected Groups List**\n\n"
        f"📊 **Total Active Groups:** `{total_groups}`\n\n"
        f"👇 **Recent Groups:**\n" + "\n".join(group_lines)
    )
    
    if total_groups > 30:
        text += f"\n\n*(Showing first 30 out of {total_groups} groups)*"

    await message.reply_text(text)
