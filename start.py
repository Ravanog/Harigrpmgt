from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import START_PIC
from script import Script

def register_start_handlers(app: Client):

    @app.on_message(filters.command("start"))
    async def start_handler(client: Client, message: Message):
        if message.chat.type.name == "PRIVATE":
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("➕ Add Bot To Your Group", url=f"https://t.me/{client.me.username}?startgroup=true")],
                [
                    InlineKeyboardButton("📖 Documentation", callback_data="docs_menu"),
                    InlineKeyboardButton("ℹ️ About", callback_data="about_menu")
                ]
            ])
            
            caption_text = Script.START_TEXT.format(first_name=message.from_user.first_name)
            
            await message.reply_photo(
                photo=START_PIC,
                caption=caption_text,
                reply_markup=keyboard
            )
        else:
            await message.reply_text("🟢 **Elite Guard Daemon is active.** Use `/settings` to manage group rules.")

    @app.on_callback_query(filters.regex("docs_menu"))
    async def docs_callback(client: Client, callback_query: CallbackQuery):
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("« Back", callback_data="main_menu")]])
        await callback_query.message.edit_caption(
            caption=Script.HELP_TEXT,
            reply_markup=kb
        )
        await callback_query.answer()

    @app.on_callback_query(filters.regex("about_menu"))
    async def about_callback(client: Client, callback_query: CallbackQuery):
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("« Back", callback_data="main_menu")]])
        await callback_query.message.edit_caption(
            caption=Script.ABOUT_TEXT,
            reply_markup=kb
        )
        await callback_query.answer()

    @app.on_callback_query(filters.regex("main_menu"))
    async def main_menu_callback(client: Client, callback_query: CallbackQuery):
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ Add Bot To Your Group", url=f"https://t.me/{client.me.username}?startgroup=true")],
            [
                InlineKeyboardButton("📖 Documentation", callback_data="docs_menu"),
                InlineKeyboardButton("ℹ️ About", callback_data="about_menu")
            ]
        ])
        
        await callback_query.message.edit_caption(
            caption=Script.MAIN_MENU_TEXT,
            reply_markup=keyboard
        )
        await callback_query.answer()
