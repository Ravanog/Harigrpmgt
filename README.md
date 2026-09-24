
# 🛡️ Elite Telegram Group Guard & Movie Search Bot

An advanced, production-grade **Telegram Group Management Bot** built using Python and the **Pyrogram** asynchronous framework. Designed to automatically secure groups against unauthorized links, forwarded promotional spam, and adult content, while featuring an interactive movie search query restriction system.

---

## ✨ Key Features

- **🛡️ Multi-Layer Security Pipeline**: Automatically detects and strips unauthorized web URLs, Telegram links, and invite redirects.
- **🚫 Adult & Spam Protection**: Scans messages for explicit keywords and spam fragments (e.g., adult leaks, promotional terms).
- **⏱️ Smart Movie Search Restriction**: Automatically intercepts short word or movie title queries, applies a **5-second temporary mute**, and prompts users with an interactive button to invite 3 members.
- **⚙️ Interactive Admin Control Panel (`/settings`)**: Group administrators can toggle features (anti-link, anti-spam, anti-forward) and switch punishment modes (Mute vs. Ban) directly inside the group via inline buttons.
- **💾 Persistent Settings Layer**: Saves group configurations dynamically using a lightweight JSON backend.
- **🖼️ Rich Start Menu**: Sends an interactive welcome card featuring a custom photo, direct add-to-group buttons, and documentation links.

---

## 📂 Project Structure

```text
├── bot.py             # Main asynchronous bot logic & event filters
├── config.py          # Centralized configuration variables (API keys, pics, limits)
├── requirements.txt   # Python dependencies
├── Procfile           # Koyeb / Heroku process execution file
└── README.md          # Project documentation
