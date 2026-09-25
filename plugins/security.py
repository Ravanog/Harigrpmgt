import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, ChatPermissions
from bot import (
    get_chat_config, is_admin, add_tracked_user, add_banned_user, 
    add_muted_user, remove_muted_user, 
    increment_violation_count, reset_violation_count
)

NSFW_KEYWORDS = [
    "sex", "porn", "xxx", "nude", "nudes", "adult", "hot video", 
    "xnxx", "xvideos", "nsfw", "bhabhi", "desisex", "fuck", "dick", "pussy"
]

@Client.on_message(filters.group & ~filters.service, group=1)
async def security_pipeline(client: Client, message: Message):
    if not message.from_user:
        return

    chat_id = message.chat.id
    user_id = message.from_user.id

    await add_tracked_user(user_id)

    # Admins bypass security rules
    if await is_admin(client, chat_id, user_id):
        return

    config = await get_chat_config(chat_id)
    raw_text = message.text or message.caption or ""
    text_content = raw_text.lower()

    # 1. 3-Second Auto-Delete All Messages Feature (Toggleable)
    if config.get("auto_delete_all", False):
        asyncio.create_task(auto_delete_any_message(client, chat_id, message.id, 3))

    violation_reason = None

    # 2. Check Anti-Forward (Toggleable)
    if config.get("anti_forward", True) and (message.forward_date or message.forward_from or message.forward_from_chat):
        violation_reason = "Forwarding messages from channels/users is not allowed."

    # 3. Check Anti-Link (Toggleable)
    elif config.get("anti_link", True):
        has_url_entity = any(entity.type in ["url", "text_link"] for entity in (message.entities or message.caption_entities or []))
        has_link_text = any(domain in text_content for domain in ["http://", "https://", "www.", "t.me/", ".com", ".me/", "bit.ly"])
        if has_url_entity or has_link_text:
            violation_reason = "Sending external links or URLs is not allowed."

    # 4. Check Anti-NSFW / Sexual Content (Toggleable)
    elif config.get("anti_nsfw", True):
        if any(kw in text_content for kw in NSFW_KEYWORDS):
            violation_reason = "Sending NSFW or sexual content keywords is strictly prohibited."

    # If a violation was triggered
    if violation_reason:
        try:
            await message.delete()
            now_count = await increment_violation_count(chat_id, user_id)

            action = config.get("action", "restrict")

            if now_count >= 2 or action == "ban":
                await client.ban_chat_member(chat_id, user_id)
                await reset_violation_count(chat_id, user_id)
                await add_banned_user(user_id)

                await message.reply_text(
                    f"🛡️ **AUTO-BAN ENFORCEMENT**\n\n"
                    f"👤 **User:** {message.from_user.mention}\n"
                    f"⚠️ **Reason:** {violation_reason}\n"
                    f"⚡ **Action:** Permanently Banned ❌"
                )
            else:
                await client.restrict_chat_member(
                    chat_id=chat_id,
                    user_id=user_id,
                    permissions=ChatPermissions(can_send_messages=False)
                )
                await add_muted_user(user_id)

                warning_msg = await message.reply_text(
                    f"🛡️ **SECURITY WARNING**\n\n"
                    f"👤 **User:** {message.from_user.mention}\n"
                    f"⚠️ **Reason:** {violation_reason}\n"
                    f"⚡ **Action:** Muted for **1 minute** 🔒\n"
                    f"📌 *Note: Repeating this will result in a permanent ban.*"
                )
                asyncio.create_task(auto_unmute_user(client, chat_id, user_id, warning_msg.id))

        except Exception as e:
            print(f"Error handling security action: {e}")

async def auto_delete_any_message(client: Client, chat_id: int, message_id: int, delay: int):
    await asyncio.sleep(delay)
    try:
        await client.delete_messages(chat_id, message_id)
    except Exception:
        pass

async def auto_unmute_user(client: Client, chat_id: int, user_id: int, warning_msg_id: int):
    await asyncio.sleep(60)
    try:
        await client.restrict_chat_member(
            chat_id=chat_id,
            user_id=user_id,
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True
            )
        )
        await remove_muted_user(user_id)
        await client.delete_messages(chat_id, warning_msg_id)
    except Exception as e:
        print(f"Error unmuting user: {e}")
