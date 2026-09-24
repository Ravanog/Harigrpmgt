import os

# Telegram API Credentials (Replace values or use Koyeb Environment Variables)
API_ID = int(os.environ.get("API_ID", 12345678))
API_HASH = os.environ.get("API_HASH", "your_api_hash_here")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_bot_token_here")

# Start Message Picture (Direct Image URL)
START_PIC = "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=800"

# Required members count to unlock movie searches
REQUIRED_INVITES = 3
