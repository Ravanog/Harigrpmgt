import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from pyrogram import Client
from motor.motor_asyncio import AsyncIOMotorClient
from config import (
    API_ID, API_HASH, BOT_TOKEN, MONGO_URL, DB_NAME, 
    WELCOME_TXT, CHANNEL_1, CHANNEL_2, REQUIRED_INVITES, RULES_TXT
)
from start import register_start_handlers

# --- Health Check Server for Cloud Hosting (Port 8080) ---
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Elite Group Guard Bot is alive and running!")
    
    def log_message(self, format, *args):
        return

class ReusableHTTPServer(HTTPServer):
    allow_reuse_address = True

def run_health_server():
    port = int(os.environ.get("PORT", 8080))
    server_address = ('0.0.0.0', port)
    try:
        httpd = ReusableHTTPServer(server_address, HealthCheckHandler)
        print(f"Health-check server listening on port {port}...")
        httpd.serve_forever()
    except Exception as e:
        print(f"Health server error: {e}")

threading.Thread(target=run_health_server, daemon=True).start()
# --------------------------------------------------------

app = Client(
    "EliteGroupManagerBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="plugins")
)

register_start_handlers(app)

# --- MongoDB Database Setup ---
mongo_client = AsyncIOMotorClient(MONGO_URL)
db = mongo_client[DB_NAME]

settings_col = db["group_settings"]
violations_col = db["user_violations"]
stats_col = db["bot_stats"]
groups_col = db["connected_groups"]

# --- Database Helper Functions ---
async def get_chat_config(chat_id: int):
    str_id = str(chat_id)
    config = await settings_col.find_one({"chat_id": str_id})
    if not config:
        default_config = {
            "chat_id": str_id,
            "welcome_enabled": True,
            "welcome_text": WELCOME_TXT,
            "rules_text": RULES_TXT,
            "channel_1": CHANNEL_1,
            "channel_2": CHANNEL_2,
            "required_invites": REQUIRED_INVITES,
            "anti_link": True,
            "anti_forward": True,
            "anti_nsfw": True,
            "auto_delete_all": False,
            "action": "restrict"
        }
        await settings_col.insert_one(default_config)
        return default_config
    return config

async def update_chat_config(chat_id: int, new_values: dict):
    str_id = str(chat_id)
    await settings_col.update_one(
        {"chat_id": str_id},
        {"$set": new_values},
        upsert=True
    )

async def toggle_welcome_status(chat_id: int):
    str_id = str(chat_id)
    config = await get_chat_config(chat_id)
    new_status = not config.get("welcome_enabled", True)
    await settings_col.update_one({"chat_id": str_id}, {"$set": {"welcome_enabled": new_status}}, upsert=True)
    return new_status

async def update_channel_link(chat_id: int, channel_key: str, link: str):
    str_id = str(chat_id)
    await settings_col.update_one({"chat_id": str_id}, {"$set": {channel_key: link}}, upsert=True)

async def increment_violation_count(chat_id: int, user_id: int):
    key = f"{chat_id}_{user_id}"
    doc = await violations_col.find_one_and_update(
        {"key": key},
        {"$inc": {"count": 1}},
        upsert=True,
        return_document=True
    )
    return doc.get("count", 1)

async def reset_violation_count(chat_id: int, user_id: int):
    key = f"{chat_id}_{user_id}"
    await violations_col.update_one({"key": key}, {"$set": {"count": 0}}, upsert=True)

async def add_tracked_user(user_id: int):
    await stats_col.update_one({"type": "global_stats"}, {"$addToSet": {"users": user_id}}, upsert=True)

async def add_banned_user(user_id: int):
    await stats_col.update_one({"type": "global_stats"}, {"$addToSet": {"banned_users": user_id}, "$pull": {"muted_users": user_id}}, upsert=True)

async def add_muted_user(user_id: int):
    await stats_col.update_one({"type": "global_stats"}, {"$addToSet": {"muted_users": user_id}}, upsert=True)

async def remove_muted_user(user_id: int):
    await stats_col.update_one({"type": "global_stats"}, {"$pull": {"muted_users": user_id}}, upsert=True)

async def get_stats_counts():
    doc = await stats_col.find_one({"type": "global_stats"})
    total_groups = await groups_col.count_documents({})
    if not doc:
        return 0, 0, 0, total_groups
    return len(doc.get("users", [])), len(doc.get("muted_users", [])), len(doc.get("banned_users", [])), total_groups

async def is_admin(client: Client, chat_id: int, user_id: int):
    from config import ADMINS
    if user_id in ADMINS:
        return True
    try:
        member = await client.get_chat_member(chat_id, user_id)
        return member.status in ["administrator", "creator"]
    except Exception:
        return False

if __name__ == "__main__":
    app.run()
