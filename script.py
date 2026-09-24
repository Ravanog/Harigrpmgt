class Script:
    START_TEXT = (
        "🤖 **Elite Group Guard System Active**\n\n"
        "Welcome, {first_name}! I am an enterprise-grade group security and movie search management utility.\n\n"
        "• Auto-blocks URLs and invite links.\n"
        "• Enforces 5-sec restriction & invite prompt on movie queries.\n"
        "• Configurable punishments (Mute vs. Ban).\n\n"
        "Add me to your target group and grant **Admin Privileges** (Delete & Restrict permissions)."
    )

    HELP_TEXT = (
        "📖 **Configuration Guidelines:**\n\n"
        "1. Promote bot to **Admin** with *Delete Messages* and *Ban/Restrict Users* rights.\n"
        "2. Type `/settings` inside the group to toggle anti-link, anti-forward, or switch punishment behaviors dynamically."
    )

    ABOUT_TEXT = (
        "ℹ️ **About Elite Group Guard Bot:**\n\n"
        "• **Developer:** Secure Group Utilities\n"
        "• **Framework:** Pyrogram (Python Async)\n"
        "• **Core Features:**\n"
        "  - Anti-Link & Anti-Forward filters\n"
        "  - Keyword spam detection\n"
        "  - 5-second movie query restriction with member invite requirement\n"
        "  - Interactive group settings dashboard (`/settings`)\n\n"
        "Designed to keep your groups clean and active!"
    )

    MAIN_MENU_TEXT = (
        "🤖 **Elite Group Guard System Active**\n\nChoose an option below:"
    )
