from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from bot import get_chat_config, update_chat_config, is_admin, toggle_welcome_status

@Client.on_message(filters.command("settings") & filters.group)
async def settings_command(client: Client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if not await is_admin(client, chat_id, user_id):
        await message.reply_text("❌ Only group administrators can access the security settings panel.")
        return

    kb = await get_settings_keyboard(chat_id)
    await message.reply_text(
        "⚙️ **Advanced Group Security & Control Panel**\n\n"
        "Tap any option below to toggle it **On** or **Off** instantly:",
        reply_markup=kb
    )

async def get_settings_keyboard(chat_id: int):
    config = await get_chat_config(chat_id)
    
    welcome_status = "✅ On" if config.get("welcome_enabled", True) else "❌ Off"
    link_status = "✅ On" if config.get("anti_link", True) else "❌ Off"
    fwd_status = "✅ On" if config.get("anti_forward", True) else "❌ Off"
    nsfw_status = "✅ On" if config.get("anti_nsfw", True) else "❌ Off"
    autodelete_status = "✅ On (3s)" if config.get("auto_delete_all", False) else "❌ Off"
    action_status = "🔒 Mute" if config.get("action", "restrict") == "restrict" else "🔨 Ban"

    return InlineKeyboardMarkup([
        [InlineKeyboardButton(f"Welcome Message: {welcome_status}", callback_data=f"toggle_welcome_{chat_id}")],
        [InlineKeyboardButton(f"Anti-Link Filter: {link_status}", callback_data=f"toggle_link_{chat_id}")],
        [InlineKeyboardButton(f"Anti-Forward Filter: {fwd_status}", callback_data=f"toggle_fwd_{chat_id}")],
        [InlineKeyboardButton(f"Anti-NSFW Filter: {nsfw_status}", callback_data=f"toggle_nsfw_{chat_id}")],
        [InlineKeyboardButton(f"Auto-Delete All (3s): {autodelete_status}", callback_data=f"toggle_autodelete_{chat_id}")],
        [InlineKeyboardButton("🔗 Edit Channel 1 Button", callback_data=f"edit_chan1_{chat_id}")],
        [InlineKeyboardButton("🔗 Edit Channel 2 Button", callback_data=f"edit_chan2_{chat_id}")],
        [InlineKeyboardButton(f"Punishment Type: {action_status}", callback_data=f"toggle_action_{chat_id}")],
        [InlineKeyboardButton("🔄 Refresh Panel", callback_data=f"refresh_{chat_id}")]
    ])

@Client.on_callback_query(filters.regex(r"^toggle_|^refresh_|^edit_chan"))
async def callback_security_handler(client: Client, callback_query: CallbackQuery):
    data = callback_query.data
    parts = data.split("_")
    chat_id = int(parts[-1])
    user_id = callback_query.from_user.id

    if not await is_admin(client, chat_id, user_id):
        await callback_query.answer("❌ Admins only!", show_alert=True)
        return

    if data.startswith("edit_chan1") or data.startswith("edit_chan2"):
        chan_num = "1" if "chan1" in data else "2"
        await callback_query.message.reply_text(
            f"💡 **How to update Channel {chan_num} link:**\n\n"
            f"Send command in group: `/setchannel{chan_num} https://t.me/your_channel`\n"
            f"*(Send `/setchannel{chan_num}` alone to delete the button).* "
        )
        await callback_query.answer()
        return

    action_type = "_".join(parts[:-1])
    config = await get_chat_config(chat_id)

    updates = {}
    if action_type == "toggle_welcome":
        await toggle_welcome_status(chat_id)
    elif action_type == "toggle_link":
        updates["anti_link"] = not config.get("anti_link", True)
    elif action_type == "toggle_fwd":
        updates["anti_forward"] = not config.get("anti_forward", True)
    elif action_type == "toggle_nsfw":
        updates["anti_nsfw"] = not config.get("anti_nsfw", True)
    elif action_type == "toggle_autodelete":
        updates["auto_delete_all"] = not config.get("auto_delete_all", False)
    elif action_type == "toggle_action":
        current = config.get("action", "restrict")
        updates["action"] = "ban" if current == "restrict" else "restrict"

    if updates:
        await update_chat_config(chat_id, updates)

    try:
        kb = await get_settings_keyboard(chat_id)
        await callback_query.message.edit_reply_markup(reply_markup=kb)
        await callback_query.answer("Settings updated successfully!")
    except Exception:
        await callback_query.answer()
