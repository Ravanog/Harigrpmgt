import re
import os
from os import environ


# Telegram API Credentials (Replace values or use Koyeb Environment Variables)
API_ID = int(os.environ.get("API_ID", 15671595))
API_HASH = os.environ.get("API_HASH", "bb8f36f9c39a24c7f8b2acbc7ea8c60a")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8932762816:AAHH4bYkyQ1a-Ujcbgsl5isu026GjIQ6wUI")

# Start Message Picture (Direct Image URL)
START_PIC = "https://files.catbox.moe/9oc9ai.jpg"

# Required members count to unlock movie searches
REQUIRED_INVITES = 3
