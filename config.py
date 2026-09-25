import re
import os
from os import environ


# Telegram API Credentials (Replace values or use Koyeb Environment Variables)
API_ID = int(os.environ.get("API_ID", 15671595))
API_HASH = os.environ.get("API_HASH", "bb8f36f9c39a24c7f8b2acbc7ea8c60a")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8932762816:AAHH4bYkyQ1a-Ujcbgsl5isu026GjIQ6wUI")

# Global Bot Admins / Owners (Put your Telegram User ID(s) here)
ADMINS = [int(x) for x in os.environ.get("ADMINS", "8363515444").split(",") if x.strip().isdigit()]

# --- Media & Customization Variables ---
START_PIC = os.environ.get("START_PIC", "https://files.catbox.moe/9oc9ai.jpg")
CHANNEL_1 = os.environ.get("CHANNEL_1", "https://t.me/+2dygCeQ4oGcwY2M9")  # Default channel 1 button link
CHANNEL_2 = os.environ.get("CHANNEL_2", "https://t.me/hari_moviez")  # Default channel 2 button link
REQUIRED_INVITES = int(os.environ.get("REQUIRED_INVITES", "3"))

# MongoDB Configuration
MONGO_URL = os.environ.get("MONGO_URL", "mongodb+srv://your_username:your_password@cluster.mongodb.net/?retryWrites=true&w=majority")
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

GROUP_RULES = os.environ.get(
    "GROUP_RULES",
    """📜 **Elite Group Rules & Guidelines**

1️⃣ Be respectful to all members. No hate speech or harassment.
2️⃣ No spamming, unauthorized advertising, or referral links.
3️⃣ No NSFW/sexual content or explicit media sharing.
4️⃣ Keep discussions relevant to the group's topic.

⚠️ *Failure to follow rules will result in mutes or permanent bans.*"""
)

HELP_TXT = os.environ.get(
    "HELP_TXT",
    "🛠️ **Elite Guard Bot - Help Menu**\n\n"
    "• `/settings` - Open interactive security & filter toggles (Admins only)\n"
    "• `/setwelcome [text]` - Set custom welcome message\n"
    "• `/setchannel1 [link]` - Set or update Channel 1 button link\n"
    "• `/setchannel2 [link]` - Set or update Channel 2 button link\n"
    "• `/rules` - View group guidelines\n"
    "• `/ban` / `/mute` / `/unrestrict` / `/pin` / `/purge` - Admin moderation tools"
)

