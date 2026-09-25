from pyrogram import Client, filters
from pyrogram.types import Message, ChatPermissions
from config import GROUP_RULES
from bot import is_admin, add_banned_user, add_muted_user, remove_muted_user

@Client.on_message(filters.command("rules") & filters.group)
async def rules_command(client: Client, message: Message):
    try:
        await message.reply_text(GROUP_RULES)
    except Exception as e:
        print(f"Error sending rules: {e}")

@Client.on_message(filters.command("ban") & filters.group)
async def ban_command(client: Client, message: Message):
    chat_id = message.chat.id
    if not await is_admin(client, chat_id, message.from_user.id):
        await message.reply_text("❌ Admins only!")
        return
    if not message.reply_to_message or not message.reply_to_message.from_user:
        await message.reply_text("⚠️ Reply to a user's message with `/ban` to ban them.")
        return
    
    target = message.reply_to_message.from_user
    try:
        await client.ban_chat_member(chat_id, target.id)
        await add_banned_user(target.id)
        await message.reply_text(f"🔨 Banned {target.mention} successfully!")
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")

@Client.on_message(filters.command("mute") & filters.group)
async def mute_command(client: Client, message: Message):
    chat_id = message.chat.id
    if not await is_admin(client, chat_id, message.from_user.id):
        await message.reply_text("❌ Admins only!")
        return
    if not message.reply_to_message or not message.reply_to_message.from_user:
        await message.reply_text("⚠️ Reply to a user's message with `/mute` to mute them.")
        return
    
    target = message.reply_to_message.from_user
    try:
        await client.restrict_chat_member(
            chat_id=chat_id,
            user_id=target.id,
            permissions=ChatPermissions(can_send_messages=False)
        )
        await add_muted_user(target.id)
        await message.reply_text(f"🔒 Muted {target.mention} successfully!")
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")

@Client.on_message(filters.command("unrestrict") & filters.group)
async def unrestrict_command(client: Client, message: Message):
    chat_id = message.chat.id
    if not await is_admin(client, chat_id, message.from_user.id):
        await message.reply_text("❌ Only group administrators can use this command.")
        return
    if not message.reply_to_message or not message.reply_to_message.from_user:
        await message.reply_text("⚠️ Please reply to the user's message whom you want to unrestrict using `/unrestrict`.")
        return

    target_user = message.reply_to_message.from_user
    try:
        await client.restrict_chat_member(
            chat_id=chat_id,
            user_id=target_user.id,
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True
            )
        )
        await remove_muted_user(target_user.id)
        await message.reply_text(f"✅ Successfully unrestricted {target_user.mention}!")
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")

@Client.on_message(filters.command("pin") & filters.group)
async def pin_command(client: Client, message: Message):
    chat_id = message.chat.id
    if not await is_admin(client, chat_id, message.from_user.id):
        await message.reply_text("❌ Admins only!")
        return
    if not message.reply_to_message:
        await message.reply_text("⚠️ Reply to the message you want to pin with `/pin`.")
        return
    
    try:
        await message.reply_to_message.pin(disable_notification=False)
        await message.reply_text("📌 Message pinned successfully!")
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")

@Client.on_message(filters.command("purge") & filters.group)
async def purge_command(client: Client, message: Message):
    chat_id = message.chat.id
    if not await is_admin(client, chat_id, message.from_user.id):
        await message.reply_text("❌ Admins only!")
        return
    if not message.reply_to_message:
        await message.reply_text("⚠️ Reply to the starting message you want to purge from.")
        return

    start_msg_id = message.reply_to_message.id
    current_msg_id = message.id
    
    message_ids = []
    for msg_id in range(start_msg_id, current_msg_id + 1):
        message_ids.append(msg_id)
        if len(message_ids) == 100:
            try:
                await client.delete_messages(chat_id, message_ids)
            except Exception:
                pass
            message_ids = []
            
    if message_ids:
        try:
            await client.delete_messages(chat_id, message_ids)
        except Exception:
            pass
            
    await message.delete()
