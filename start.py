from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import START_PIC, START_TXT, HELP_TXT

def register_start_handlers(app: Client):
    @app.on_message(filters.command("start") & filters.private)
    async def start_private_handler(client: Client, message: Message):
        caption = START_TXT.format(user=message.from_user.mention)
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ Add Me To Your Group", url=f"https://t.me/{client.me.username}?startgroup=true")],
            [InlineKeyboardButton("❓ Help & Commands", callback_data="help_menu")]
        ])
        
        if START_PIC:
            try:
                await message.reply_photo(photo=START_PIC, caption=caption, reply_markup=reply_markup)
                return
            except Exception:
                pass
        
        await message.reply_text(caption, reply_markup=reply_markup)

    @app.on_callback_query(filters.regex("help_menu"))
    async def help_callback(client: Client, callback_query):
        await callback_query.message.edit_caption(
            caption=HELP_TXT,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back", callback_data="back_start")]
            ])
        )
        await callback_query.answer()

    @app.on_callback_query(filters.regex("back_start"))
    async def back_start_callback(client: Client, callback_query):
        caption = START_TXT.format(user=callback_query.from_user.mention)
        await callback_query.message.edit_caption(
            caption=caption,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("➕ Add Me To Your Group", url=f"https://t.me/{client.me.username}?startgroup=true")],
                [InlineKeyboardButton("❓ Help & Commands", callback_data="help_menu")]
            ])
        )
        await callback_query.answer()
