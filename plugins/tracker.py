from pyrogram import Client, filters
from pyrogram.types import ChatMemberUpdated
from bot import db

groups_col = db["connected_groups"]

@Client.on_chat_member_updated()
async def track_connected_groups(client: Client, chat_member_updated: ChatMemberUpdated):
    chat = chat_member_updated.chat
    
    # Only track groups and supergroups
    if chat.type in ["group", "supergroup"]:
        new_member = chat_member_updated.new_chat_member
        
        # Check if the update is for the bot itself
        if new_member and new_member.user.id == client.me.id:
            status = new_member.status
            
            if status in ["member", "administrator"]:
                # Bot was added to the group
                await groups_col.update_one(
                    {"chat_id": chat.id},
                    {
                        "$set": {
                            "chat_id": chat.id,
                            "title": chat.title,
                            "username": chat.username or "Private"
                        }
                    },
                    upsert=True
                )
            elif status in ["left", "kicked"]:
                # Bot was removed or kicked from the group
                await groups_col.delete_one({"chat_id": chat.id})
