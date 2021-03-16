import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

import os
import time
import asyncio
import pyrogram

if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

from script import script
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant, UserBannedInChannel 

from progress import progress_for_pyrogram

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser

from PIL import Image
from database.database import *

    
async def rename(bot, message):
    
    mssg = await bot.get_messages(
        message.chat.id,
        message.reply_to_message.message_id
    )    
    
    media = mssg.reply_to_message

    
    if media.empty:
        await message.reply_text('Why did you delete that 😕', True)
        return
    await bot.delete_messages(chat_id=message.chat.id, message_ids=message.reply_to_message.message_id, revoke=True)
    if (" | " in message.text) and (message.reply_to_message is not None):
        file_name, file_type = message.text.split(" | ", 1)
        if len(file_name) > 64:
            await message.reply_text(script.IFLONG_FILE_NAME.format(alimit="64", num=len(file_name)))
            return
        description = script.CUSTOM_CAPTION_UL_FILE
        download_location = Config.DOWNLOAD_LOCATION + "/"
        thumb_image_path = download_location + "FayasNoushad " + str(message.from_user.id) + ".jpg"
        if not os.path.exists(thumb_image_path):
            mes = await thumb(message.from_user.id)
            if mes != None:
                m = await bot.get_messages(message.chat.id, mes.msg_id)
                await m.download(file_name=thumb_image_path)
                thumb_image_path = thumb_image_path

        a = await bot.send_message(chat_id=message.chat.id, text=script.DOWNLOAD_START, reply_to_message_id=message.message_id)
        c_time = time.time()
        the_real_download_location = await bot.download_media(
            message=media,
            file_name=download_location,
            progress=progress_for_pyrogram,
            progress_args=(script.DOWNLOAD_START, a, c_time)
        )
        if the_real_download_location is not None:
            await bot.edit_message_text(text=script.SAVED_RECVD_DOC_FILE, chat_id=message.chat.id, message_id=a.message_id)
            new_file_name = download_location + file_name
            os.rename(the_real_download_location, new_file_name)
            # logger.info(the_real_download_location)
            try:
                await bot.edit_message_text(text=script.UPLOAD_START, chat_id=message.chat.id, message_id=a.message_id)
            except:
                pass
            if os.path.exists(thumb_image_path):
                width = 0
                height = 0
                metadata = extractMetadata(createParser(thumb_image_path))
                if metadata.has("width"):
                    width = metadata.get("width")
                if metadata.has("height"):
                    height = metadata.get("height")
                Image.open(thumb_image_path).convert("RGB").save(thumb_image_path)
                img = Image.open(thumb_image_path)
                img.resize((320, height))
                img.save(thumb_image_path, "JPEG")
            else:
                thumb_image_path = None
            c_time = time.time()
            if "media" in file_type:
                await bot.send_video(
                    chat_id=message.chat.id,
                    video=new_file_name,
                    thumb=thumb_image_path,
                    caption="<b>" + file_name + "</b>",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('⚙ Join Updates Channel ⚙', url='https://telegram.me/VKPROJECTS')]]),
                    reply_to_message_id=message.reply_to_message.message_id,
                    progress=progress_for_pyrogram,
                    progress_args=(script.UPLOAD_START, a, c_time)
                )
                try:
                    os.remove(new_file_name)
                except:
                    pass
                try:
                    os.remove(thumb_image_path)
                except:
                    pass
                await bot.edit_message_text(text=script.AFTER_SUCCESSFUL_UPLOAD_MSG, chat_id=message.chat.id, message_id=a.message_id, disable_web_page_preview=True)
                return
            if "file" in file_type:
                await bot.send_document(
                    chat_id=message.chat.id,
                    document=new_file_name,
                    thumb=thumb_image_path,
                    caption="<b>" + file_name + "</b>",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('⚙ Join Updates Channel ⚙', url='https://telegram.me/VKPROJECTS')]]),
                    reply_to_message_id=message.reply_to_message.message_id,
                    progress=progress_for_pyrogram,
                    progress_args=(script.UPLOAD_START, a, c_time)
                )
                try:
                    os.remove(new_file_name)
                except:
                    pass                 
                try:
                    os.remove(thumb_image_path)
                except:
                    pass
                await bot.edit_message_text(text=script.AFTER_SUCCESSFUL_UPLOAD_MSG, chat_id=message.chat.id, message_id=a.message_id, disable_web_page_preview=True)
                return
        else:
            await bot.send_message(chat_id=message.chat.id, text="You're not Authorized to do that!", reply_to_message_id=message.message_id)
