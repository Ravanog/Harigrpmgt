import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot import get_chat_config, update_chat_config, is_admin, update_channel_link

@Client.on_message(filters.new_chat_members & filters.group)
async def welcome_new_members(client: Client, message: Message):
    chat_id = message.chat.id
    config = await get_chat_config(chat_id)

    if not config.get("welcome_enabled", True):
        return

    for new_user in message.new_chat_members:
        if new_user.id == client.me.id:
            continue
        
        raw_welcome = config.get("welcome_text", "👋 Welcome {user} to **{group}**!")
        formatted_welcome = raw_welcome.format(
            user=new_user.mention,
            group=message.chat.title
        )
        
        buttons = []
        c1 = config.get("channel_1")
        c2 = config.get("channel_2")
        
        if c1:
            buttons.append([InlineKeyboardButton("📢 Join Channel 1", url=c1)])
        if c2:
            buttons.append([InlineKeyboardButton("📢 Join Channel 2", url=c2)])
            
        reply_markup = InlineKeyboardMarkup(buttons) if buttons else None
        
        try:
            sent_msg = await message.reply_text(
                formatted_welcome,
                reply_markup=reply_markup
            )
            asyncio.create_task(auto_delete_welcome(client, chat_id, sent_msg.id))
        except Exception as e:
            print(f"Error sending welcome message: {e}")

async def auto_delete_welcome(client: Client, chat_id: int, message_id: int):
    await asyncio.sleep(60)
    try:
        await client.delete_messages(chat_id, message_id)
    except Exception as e:
        print(f"Error auto-deleting welcome message: {e}")

@Client.on_message(filters.command("setwelcome") & filters.group)
async def set_welcome_command(client: Client, message: Message):
    chat_id = message.chat.id
    if not await is_admin(client, chat_id, message.from_user.id):
        await message.reply_text("❌ Only group admins can change the welcome message.")
        return

    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.reply_text(
            "⚠️ **Usage Error**\n"
            "Please provide the welcome message text after the command.\n\n"
            "**Example:**\n`/setwelcome Welcome {user} to {group}! Enjoy your stay.`"
        )
        return

    new_text = parts[1]
    await update_chat_config(chat_id, {"welcome_text": new_text})
    await message.reply_text("✅ Successfully updated the custom welcome message for this group!")

@Client.on_message(filters.command("setchannel1") & filters.group)
async def set_channel_1_command(client: Client, message: Message):
    chat_id = message.chat.id
    if not await is_admin(client, chat_id, message.from_user.id):
        return

    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await update_channel_link(chat_id, "channel_1", "")
        await message.reply_text("🗑️ Channel 1 button has been **deleted/removed**.")
        return

    link = parts[1].strip()
    await update_channel_link(chat_id, "channel_1", link)
    await message.reply_text(f"✅ Channel 1 button link updated to:\n`{link}`")

@Client.on_message(filters.command("setchannel2") & filters.group)
async def set_channel_2_command(client: Client, message: Message):
    chat_id = message.chat.id
    if not await is_admin(client, chat_id, message.from_user.id):
        return

    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await update_channel_link(chat_id, "channel_2", "")
        await message.reply_text("🗑️ Channel 2 button has been **deleted/removed**.")
        return

    link = parts[1].strip()
    await update_channel_link(chat_id, "channel_2", link)
    await message.reply_text(f"✅ Channel 2 button link updated to:\n`{link}`")
  
