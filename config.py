import re
import os
from os import environ


# Telegram API Credentials (Replace values or use Koyeb Environment Variables)
API_ID = int(os.environ.get("API_ID", 15671595))
API_HASH = os.environ.get("API_HASH", "bb8f36f9c39a24c7f8b2acbc7ea8c60a")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8916131861:AAHx8KQVvcUrXJkicyWSIlxmxRfX3StHgqQ")

# Global Bot Admins / Owners (Put your Telegram User ID(s) here)
ADMINS = [int(x) for x in os.environ.get("ADMINS", "8363515444").split(",") if x.strip().isdigit()]

# --- Media & Customization Variables ---
START_PIC = os.environ.get("START_PIC", "https://files.catbox.moe/9oc9ai.jpg")
CHANNEL_1 = os.environ.get("CHANNEL_1", "https://t.me/+2dygCeQ4oGcwY2M9")  # Default channel 1 button link
CHANNEL_2 = os.environ.get("CHANNEL_2", "https://t.me/hari_moviez")  # Default channel 2 button link
REQUIRED_INVITES = int(os.environ.get("REQUIRED_INVITES", "3"))

# MongoDB Configuration
MONGO_URL = os.environ.get("MONGO_URL", "mongodb+srv://anikush8310_db_user:YLhManFE9BAMvdyV@cluster0.0aqtvqw.mongodb.net/?appName=Cluster0")
DB_NAME = "hari_elite_bot"


# ==========================================
# --- CENTRALIZED TEXT TEMPLATES & STRINGS ---
# ==========================================

START_TXT = os.environ.get(
    "START_TXT",
    "👋 Hello {user}!\n\n"
    "I am your **Elite Group Guard Bot**, equipped with toggleable security filters, anti-link, "
    "anti-forward, anti-NSFW, 3-second global message auto-delete, and custom welcome management."
)

WELCOME_TXT = os.environ.get(
    "WELCOME_TXT",
    "👋 Welcome {user} to **{group}**!\n\n📜 Please read the group rules and enjoy your stay!"
)

RULES_TXT = (
    "📜 **Official Group Rules:**\n\n"
    "1. Be respectful to all members.\n"
    "2. No spam, unauthorized links, or advertisements.\n"
    "3. No NSFW, abusive, or hate speech content.\n"
    "4. Listen to and respect administrators."
)

HELP_TXT = os.environ.get(
    "HELP_TXT",
    "🛠️ **Elite Guard Bot — Help Menu**\n\n"
    "⚙️ **Security & Configuration:**\n"
    "• `/settings` — Open interactive security & filter toggles *(Admins)*\n"
    "• `/rules` — View group guidelines & rules\n\n"
    "👋 **Welcome & Channels:**\n"
    "• `/setwelcome [text]` — Set custom welcome message\n"
    "• `/setchannel1 [link]` — Set or update Channel 1 button\n"
    "• `/setchannel2 [link]` — Set or update Channel 2 button\n\n"
    "⚡ **Admin Moderation Tools:**\n"
    "• `/ban` — Permanently ban replied user\n"
    "• `/mute` — Restrict replied user from chatting\n"
    "• `/unrestrict` — Restore user permissions\n"
    "• `/pin` — Pin replied message with alert\n"
    "• `/purge` — Bulk delete messages\n"
    "• `/users` — View group stats & analytics\n"
    "• `/groups` — List all connected groups *(Owner only)*"
)
