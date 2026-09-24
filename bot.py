import os
import re
import json
import time
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ChatPermissions
from config import API_ID, API_HASH, BOT_TOKEN, REQUIRED_INVITES
from start import register_start_handlers

app = Client(
    "EliteGroupManagerBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Register start module handlers
register_start_handlers(app)

SETTINGS_FILE = "group_settings.json"

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

def save_settings(data):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=4)

group_settings = load_settings()

def get_chat_setting(chat_id: int, key: str, default=True):
    str_id = str(chat_id)
    if str_id not in group_settings:
        group_settings[str_id] = {"anti_link": True, "anti_forward": True, "anti_spam": True, "action": "restrict"}
        save_settings(group_settings)
    return group_settings[str_id].get(key, default)

URL_REGEX = r"(https?://\S+|www\.\S+|t\.me/\S+|telegram\.dog/\S+|bit\.ly/\S+|whatsapp\.com/\S+|chat\.whatsapp\.com/\S+|discord\.gg/\S+|instagram\.com/\S+)"
SPAM_KEYWORDS = [
    "xxx", "hardcore", "homemade", "cheating", "massage", 
    "daily leak", "nsfw", "18+", "hot video", "sex chat", "adult video", "onlyfans"
]

@app.on_message(filters.group & ~filters.service, group=1)
async def elite_security_pipeline(client: Client, message: Message):
    if not message.from_user:
        return

    chat_id = message.chat.id
    user_id = message.from_user.id

    # Exemption for Administrators and Creators
    try:
        member = await client.get_chat_member(chat_id, user_id)
        if member.status in ["administrator", "creator"]:
            return
    except Exception:
        pass

    raw_text = message.text or message.caption or ""
    text_content = raw_text.lower()

    anti_link = get_chat_setting(chat_id, "anti_link", True)
    anti_forward = get_chat_setting(chat_id, "anti_forward", True)
    anti_spam = get_chat_setting(chat_id, "anti_spam", True)
    punishment_action = get_chat_setting(chat_id, "action", "restrict")

    violations = []
    is_movie_search = False

    # 1. Anti-Link Check
    if anti_link:
        has_url = bool(re.search(URL_REGEX, raw_text, flags=re.IGNORECASE))
        if message.entities:
            for entity in message.entities:
                if entity.type in ["url", "text_link", "mention", "email"]:
                    has_url = True
        if has_url:
            violations.append("Unauthorized Web/Telegram Link")

    # 2. Anti-Forward Check
    if anti_forward:
        is_fwd = bool(message.forward_date or message.forward_from or message.forward_from_chat)
        if is_fwd:
            violations.append("Forwarded Promotional Post")

    # 3. Anti-Spam Keyword Check
    if anti_spam:
        matched_keywords = [kw for kw in SPAM_KEYWORDS if kw in text_content]
        if matched_keywords:
            violations.append(f"Forbidden Keywords Detected ({', '.join(matched_keywords)})")

    # 4. Movie Search / Plain Word Query Check
    if not violations and len(raw_text.split()) <= 4 and not raw_text.startswith("/"):
        is_movie_search = True

    # Handle Hard Violations (Links / Spam / Adult Leaks)
    if violations:
        try:
            await message.delete()
            if punishment_action == "ban":
                await client.ban_chat_member(chat_id, user_id)
                action_text = "Permanently Banned ❌"
            else:
                await client.restrict_chat_member(
                    chat_id=chat_id,
                    user_id=user_id,
                    permissions=ChatPermissions(can_send_messages=False)
                )
                action_text = "Muted / Restricted 🔒"

            reason_str = " + ".join(violations)
            await message.reply_text(
                f"🛡️ **SECURITY ENFORCEMENT TRIGGERED**\n\n"
                f"👤 **User:** {message.from_user.mention}\n"
                f"⚠️ **Violation:** {reason_str}\n"
                f"⚡ **Action:** Message deleted & {action_text}"
            )
        except Exception as e:
            print(f"Error executing security rule: {e}")

    # Handle Movie Search Queries (5-sec restriction + invite prompt)
    elif is_movie_search:
        try:
            await message.delete()

            # Temporarily restrict user for 5 seconds
            await client.restrict_chat_member(
                chat_id=chat_id,
                user_id=user_id,
                permissions=ChatPermissions(can_send_messages=False),
                until_date=int(time.time()) + 5
            )

            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton(f"➕ Add {REQUIRED_INVITES} Members to Search", url=f"https://t.me/{client.me.username}?startgroup=true")]
            ])

            warning_msg = await message.reply_text(
                f"⚠️ **Hey {message.from_user.mention}!**\n\n"
                f"To search for movies or post queries, you must first add **{REQUIRED_INVITES} members** to this group.\n"
                f"🔒 *Your messaging is temporarily restricted for 5 seconds.*",
                reply_markup=keyboard
            )

            await asyncio.sleep(8)
            await warning_msg.delete()

        except Exception as e:
            print(f"Error handling movie search restriction: {e}")

# Admin Settings Command Panel
@app.on_message(filters.command("settings") & filters.group)
async def settings_command(client: Client, message: Message):
    try:
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        if member.status not in ["administrator", "creator"]:
            await message.reply_text("❌ Only group administrators can access the security settings panel.")
            return
    except Exception:
        return

    chat_id = message.chat.id
    kb = get_settings_keyboard(chat_id)
    await message.reply_text(
        "⚙️ **Advanced Group Security Control Panel**\n\n"
        "Configure active filters and mitigation policies below:",
        reply_markup=kb
    )

def get_settings_keyboard(chat_id: int):
    str_id = str(chat_id)
    settings = group_settings.get(str_id, {"anti_link": True, "anti_forward": True, "anti_spam": True, "action": "restrict"})
    
    link_status = "✅ Enabled" if settings.get("anti_link", True) else "❌ Disabled"
    fwd_status = "✅ Enabled" if settings.get("anti_forward", True) else "❌ Disabled"
    spam_status = "✅ Enabled" if settings.get("anti_spam", True) else "❌ Disabled"
    action_status = "🔒 Mute" if settings.get("action", "restrict") == "restrict" else "🔨 Ban"

    return InlineKeyboardMarkup([
        [InlineKeyboardButton(f"Anti-Link: {link_status}", callback_data=f"toggle_link_{chat_id}")],
        [InlineKeyboardButton(f"Anti-Forward: {fwd_status}", callback_data=f"toggle_fwd_{chat_id}")],
        [InlineKeyboardButton(f"Anti-Spam Text: {spam_status}", callback_data=f"toggle_spam_{chat_id}")],
        [InlineKeyboardButton(f"Punishment: {action_status}", callback_data=f"toggle_action_{chat_id}")],
        [InlineKeyboardButton("🔄 Refresh Panel", callback_data=f"refresh_{chat_id}")]
    ])

@app.on_callback_query(filters.regex(r"^toggle_|^refresh_"))
async def callback_security_handler(client: Client, callback_query: CallbackQuery):
    data = callback_query.data
    parts = data.split("_")
    action_type = parts[0] + "_" + parts[1] if parts[0] == "toggle" else parts[0]
    chat_id = int(parts[-1])

    try:
        member = await client.get_chat_member(chat_id, callback_query.from_user.id)
        if member.status not in ["administrator", "creator"]:
            await callback_query.answer("❌ Admins only!", show_alert=True)
            return
    except Exception:
        return

    str_id = str(chat_id)
    if str_id not in group_settings:
        group_settings[str_id] = {"anti_link": True, "anti_forward": True, "anti_spam": True, "action": "restrict"}

    if action_type == "toggle_link":
        group_settings[str_id]["anti_link"] = not group_settings[str_id].get("anti_link", True)
    elif action_type == "toggle_fwd":
        group_settings[str_id]["anti_forward"] = not group_settings[str_id].get("anti_forward", True)
    elif action_type == "toggle_spam":
        group_settings[str_id]["anti_spam"] = not group_settings[str_id].get("anti_spam", True)
    elif action_type == "toggle_action":
        current = group_settings[str_id].get("action", "restrict")
        group_settings[str_id]["action"] = "ban" if current == "restrict" else "restrict"

    save_settings(group_settings)

    try:
        await callback_query.message.edit_reply_markup(reply_markup=get_settings_keyboard(chat_id))
        await callback_query.answer("Settings updated successfully!")
    except Exception:
        await callback_query.answer()

print("Elite Group Guard Bot initializing...")
app.run()
