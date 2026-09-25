import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from bot import db
from config import ADMINS

groups_col = db["connected_groups"]

@Client.on_message(filters.command("broadcast") & filters.private)
async def broadcast_groups_command(client: Client, message: Message):
    # Check if the user is a global bot admin
    if message.from_user.id not in ADMINS:
        await message.reply_text("❌ This command is restricted to bot administrators only.")
        return

    # Check if the admin replied to a message to broadcast
    if not message.reply_to_message:
        await message.reply_text(
            "⚠️ **Broadcast Usage:**\n\n"
            "1. Go to your private chat with the bot.\n"
            "2. Send or forward the message you want to broadcast.\n"
            "3. **Reply** to that message with `/broadcast`."
        )
        return

    broadcast_msg = message.reply_to_message
    
    # Fetch all connected groups from MongoDB
    cursor = groups_col.find({})
    groups = await cursor.to_list(length=None)
    
    total_groups = len(groups)
    if total_groups == 0:
        await message.reply_text("📂 There are no connected groups found in the database.")
        return

    status_msg = await message.reply_text(f"🚀 Starting broadcast to **{total_groups}** connected groups...")
    
    success = 0
    failed = 0

    for group in groups:
        chat_id = group.get("chat_id")
        try:
            # Copy the replied message directly to the group chat
            await broadcast_msg.copy(chat_id=chat_id)
            success += 1
            # Small delay to prevent Telegram FloodWait limits
            await asyncio.sleep(0.3)
        except Exception as e:
            failed += 1
            # Clean up database if bot was kicked, blocked, or chat is invalid
            error_str = str(e).lower()
            if any(err in error_str for err in ["peer_id_invalid", "bot_kicked", "chat_admin_required", "user_is_blocked"]):
                await groups_col.delete_one({"chat_id": chat_id})

    # Final analytics report
    await status_msg.edit_text(
        f"✅ **Broadcast Completed!**\n\n"
        f"📤 **Successful Deliveries:** `{success}`\n"
        f"❌ **Failed Deliveries:** `{failed}`\n"
        f"🏢 **Total Groups Processed:** `{total_groups}`"
    )
