from pyrogram import Client, filters
from pyrogram.types import Message
from bot import is_admin

# --- Fallback Handlers for PM (Private Chat) ---
@Client.on_message(filters.command(["ban", "mute", "purge", "pin", "unrestrict"]) & filters.private)
async def admin_pm_fallback(client: Client, message: Message):
    cmd = message.command[0]
    await message.reply_text(
        f"⚠️ **Invalid Usage:** The `/{cmd}` command is designed for group moderation.\n\n"
        f"Please use this command **inside your Telegram group chat** by replying to a user's message!"
    )

# --- Group Moderation Commands ---
@Client.on_message(filters.command("ban") & filters.group)
async def ban_command(client: Client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if not await is_admin(client, chat_id, user_id):
        await message.reply_text("❌ Only group administrators can use the ban command.")
        return

    if not message.reply_to_message:
        await message.reply_text("⚠️ Please reply to the user's message you want to ban.")
        return

    target_user = message.reply_to_message.from_user
    if not target_user:
        await message.reply_text("❌ Could not identify the user to ban.")
        return

    try:
        await client.ban_chat_member(chat_id, target_user.id)
        await message.reply_text(f"🔨 Successfully banned **{target_user.first_name}** from this group.")
    except Exception as e:
        await message.reply_text(f"❌ Failed to ban user. Make sure I am an admin with ban permissions.\nError: {e}")

@Client.on_message(filters.command("mute") & filters.group)
async def mute_command(client: Client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if not await is_admin(client, chat_id, user_id):
        await message.reply_text("❌ Only group administrators can use the mute command.")
        return

    if not message.reply_to_message:
        await message.reply_text("⚠️ Please reply to the user's message you want to mute.")
        return

    target_user = message.reply_to_message.from_user
    if not target_user:
        await message.reply_text("❌ Could not identify the user to mute.")
        return

    from pyrogram.types import ChatPermissions
    try:
        await client.restrict_chat_member(
            chat_id, 
            target_user.id, 
            ChatPermissions(can_send_messages=False)
        )
        await message.reply_text(f"🔒 Successfully muted **{target_user.first_name}**.")
    except Exception as e:
        await message.reply_text(f"❌ Failed to mute user. Check my admin permissions.\nError: {e}")

@Client.on_message(filters.command("unrestrict") & filters.group)
async def unrestrict_command(client: Client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if not await is_admin(client, chat_id, user_id):
        await message.reply_text("❌ Only group administrators can use this command.")
        return

    if not message.reply_to_message:
        await message.reply_text("⚠️ Please reply to the user's message you want to unrestrict.")
        return

    target_user = message.reply_to_message.from_user
    if not target_user:
        await message.reply_text("❌ Could not identify the user.")
        return

    from pyrogram.types import ChatPermissions
    try:
        await client.restrict_chat_member(
            chat_id, 
            target_user.id, 
            ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True
            )
        )
        await message.reply_text(f"🔓 Successfully restored permissions for **{target_user.first_name}**.")
    except Exception as e:
        await message.reply_text(f"❌ Failed to unrestrict user.\nError: {e}")

@Client.on_message(filters.command("pin") & filters.group)
async def pin_command(client: Client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if not await is_admin(client, chat_id, user_id):
        await message.reply_text("❌ Only group administrators can pin messages.")
        return

    if not message.reply_to_message:
        await message.reply_text("⚠️ Please reply to the message you want to pin.")
        return

    try:
        await client.pin_chat_message(chat_id, message.reply_to_message.id)
        await message.reply_text("📌 Message pinned successfully!")
    except Exception as e:
        await message.reply_text(f"❌ Failed to pin message. Make sure I have pin permissions.\nError: {e}")

@Client.on_message(filters.command("purge") & filters.group)
async def purge_command(client: Client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if not await is_admin(client, chat_id, user_id):
        await message.reply_text("❌ Only group administrators can purge messages.")
        return

    if not message.reply_to_message:
        await message.reply_text("⚠️ Please reply to the starting message you want to purge from.")
        return

    message_ids = []
    start_id = message.reply_to_message.id
    end_id = message.id

    for i in range(start_id, end_id + 1):
        message_ids.append(i)
        if len(message_ids) >= 100:  # Telegram batch delete limit
            break

    try:
        await client.delete_messages(chat_id, message_ids)
        ack = await message.reply_text(f"🗑️ Purged {len(message_ids)} messages successfully.")
        await asyncio.sleep(3)
        await ack.delete()
    except Exception as e:
        await message.reply_text(f"❌ Failed to purge messages.\nError: {e}")
