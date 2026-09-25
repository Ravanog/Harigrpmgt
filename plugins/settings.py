from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from bot import get_chat_config, update_chat_config, toggle_welcome_status, groups_col
from config import RULES_TXT

@Client.on_message(filters.command("settings") & (filters.group | filters.private))
async def settings_command(client: Client, message: Message):
    user_id = message.from_user.id
    
    # If used in Private Chat, let the user choose a group
    if message.chat.type.name == "PRIVATE":
        cursor = groups_col.find({})
        groups = await cursor.to_list(length=None)
        
        if not groups:
            await message.reply_text("📂 My bot is not connected to any groups yet. Add me to a group first!")
            return
        
        buttons = []
        for g in groups:
            chat_id = g.get("chat_id")
            title = g.get("title", "Unnamed Group")
            buttons.append([InlineKeyboardButton(title, callback_data=f"cfg_select_{chat_id}")])
        
        await message.reply_text(
            "⚙️ **Group Settings Manager (PM)**\n\n"
            "Select the group you want to configure:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        return

    # If used in a Group
    chat_id = message.chat.id
    from bot import is_admin
    if not await is_admin(client, chat_id, user_id):
        await message.reply_text("❌ Only group administrators can open settings.")
        return

    config = await get_chat_config(chat_id)
    keyboard = get_settings_keyboard(chat_id, config)
    
    await message.reply_text(
        f"⚙️ **Group Security & Management Settings**\n"
        f"🏢 **Group:** `{message.chat.title}`\n\n"
        f"Configure your security filters and options below:",
        reply_markup=keyboard
    )

def get_settings_keyboard(chat_id, config):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(f"Welcome: {'🟢 ON' if config.get('welcome_enabled') else '🔴 OFF'}", callback_data=f"toggle_wel_{chat_id}"),
            InlineKeyboardButton(f"Auto-Delete: {'🟢 ON' if config.get('auto_delete_all') else '🔴 OFF'}", callback_data=f"toggle_del_{chat_id}")
        ],
        [
            InlineKeyboardButton(f"Anti-Link: {'🟢 ON' if config.get('anti_link') else '🔴 OFF'}", callback_data=f"toggle_link_{chat_id}"),
            InlineKeyboardButton(f"Anti-Forward: {'🟢 ON' if config.get('anti_forward') else '🔴 OFF'}", callback_data=f"toggle_fwd_{chat_id}")
        ],
        [
            InlineKeyboardButton(f"Anti-NSFW: {'🟢 ON' if config.get('anti_nsfw') else '🔴 OFF'}", callback_data=f"toggle_nsfw_{chat_id}"),
            InlineKeyboardButton(f"Action: {config.get('action', 'restrict').upper()}", callback_data=f"toggle_action_{chat_id}")
        ]
    ])

@Client.on_callback_query(filters.regex(r"^cfg_select_"))
async def select_group_settings(client: Client, callback_query: CallbackQuery):
    chat_id = int(callback_query.data.split("_")[2])
    config = await get_chat_config(chat_id)
    keyboard = get_settings_keyboard(chat_id, config)
    
    await callback_query.message.edit_text(
        f"⚙️ **Group Security & Management Settings**\n\n"
        f"Configure your security filters and options below:",
        reply_markup=keyboard
    )

@Client.on_message(filters.command("rules") & (filters.group | filters.private))
async def rules_command(client: Client, message: Message):
    if message.chat.type.name == "PRIVATE":
        await message.reply_text("⚠️ Please use `/rules` inside a specific group chat to view its guidelines.")
        return
        
    chat_id = message.chat.id
    config = await get_chat_config(chat_id)
    
    # Pulls the custom saved rules, or falls back to RULES_TXT from config.py
    rules_text = config.get("rules_text", RULES_TXT)
    
    await message.reply_text(rules_text)

@Client.on_message(filters.command("setrules") & filters.group)
async def set_rules_command(client: Client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    if not await is_admin(client, chat_id, user_id):
        await message.reply_text("❌ Only group administrators can update the rules.")
        return

    if len(message.command) < 2:
        await message.reply_text(
            "⚠️ **Invalid Usage:**\n"
            "Please provide the rules text after the command.\n\n"
            "**Example:**\n`/setrules 1. No spam\n2. Be nice`"
        )
        return

    new_rules = message.text.split(None, 1)[1]
    await update_chat_config(chat_id, {"rules_text": new_rules})
    await message.reply_text("✅ Group rules have been successfully updated!")

@Client.on_callback_query(filters.regex(r"^toggle_"))
async def toggle_setting_callback(client: Client, callback_query: CallbackQuery):
    data_parts = callback_query.data.split("_")
    action_type = data_parts[1]
    chat_id = int(data_parts[2])
    
    config = await get_chat_config(chat_id)
    
    if action_type == "wel":
        new_val = not config.get("welcome_enabled", True)
        await update_chat_config(chat_id, {"welcome_enabled": new_val})
    elif action_type == "del":
        new_val = not config.get("auto_delete_all", False)
        await update_chat_config(chat_id, {"auto_delete_all": new_val})
    elif action_type == "link":
        new_val = not config.get("anti_link", True)
        await update_chat_config(chat_id, {"anti_link": new_val})
    elif action_type == "fwd":
        new_val = not config.get("anti_forward", True)
        await update_chat_config(chat_id, {"anti_forward": True})
    elif action_type == "nsfw":
        new_val = not config.get("anti_nsfw", True)
        await update_chat_config(chat_id, {"anti_nsfw": new_val})
    elif action_type == "action":
        current = config.get("action", "restrict")
        new_val = "ban" if current == "restrict" else "restrict"
        await update_chat_config(chat_id, {"action": new_val})
        
    updated_config = await get_chat_config(chat_id)
    await callback_query.message.edit_reply_markup(reply_markup=get_settings_keyboard(chat_id, updated_config))
    await callback_query.answer("Settings updated successfully!")
