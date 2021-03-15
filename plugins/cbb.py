import pyrogram
import asyncio
from pyrogram import Client as FayasNoushad
from plugins.commands import force_name, start, help

@FayasNoushad.on_callback_query()
async def cb_handler(bot, update):
        
    if update.data == "rename":
        await update.message.delete()
        await force_name(bot, update.message)
        
    if update.data == "home":
        await update.message.delete()
        await start(bot, update.message)

    if update.data == "help":
        await update.message.delete()
        await help(bot, update.message)

    if update.data == "close":
        await update.message.delete()
    
    if update.data == "cancel":
        await update.message.edit_text(text="<code>Process Cancelled</code>")
