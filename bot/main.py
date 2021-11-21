import logging
import os
from typing import Union, List

from telegram.ext import Updater, Filters, MessageHandler, CommandHandler

from telegram.ext import CommandHandler, MessageHandler, MessageFilter, CallbackQueryHandler
from telegram import InlineKeyboardButton, KeyboardButton
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup
from telegram import KeyboardButton, InlineKeyboardMarkup

import requests
from PIL import Image
from io import BytesIO

import pdb

BASE_URL = "http://localhost:8000"

def build_menu(
    buttons: List[InlineKeyboardButton],
    n_cols: int,
    header_buttons: Union[InlineKeyboardButton, List[InlineKeyboardButton]]=None,
    footer_buttons: Union[InlineKeyboardButton, List[InlineKeyboardButton]]=None
) -> List[List[InlineKeyboardButton]]:
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons if isinstance(header_buttons, list) else [header_buttons])
    if footer_buttons:
        menu.append(footer_buttons if isinstance(footer_buttons, list) else [footer_buttons])
    return menu

def start(update, context):

    context.bot.send_message(chat_id=update.effective_chat.id, 
    text="Добрый день, вас приветствует бот пекарни Династия"
         "Чтобы посмотреть ассортимент, нажмите 'Продукты'")


def get_products(update, context):

    data = requests.get(f"{BASE_URL}/api/products/")
    response = data.json()

    # button_list = [
    #     InlineKeyboardButton("В корзину", callback_data="xyz")
    # ]
    
    # reply_markup = InlineKeyboardMarkup([button_list])

    for product in response:
        caption = f"""
        {product["name"]}\nЦена:
        """

        url = f"{BASE_URL}{product['image']}"
        img = get_image(url, (350, 300))
        button = InlineKeyboardButton("В корзину", callback_data=str(product))
        reply_markup = InlineKeyboardMarkup([[button]])

        context.bot.send_photo(chat_id=update.effective_chat.id, photo=img, caption=caption, reply_markup=reply_markup)




def get_image(image_url: str, size: tuple):

    data = requests.get(image_url).content
    img = Image.open(BytesIO(data))
    resized = img.resize(size)
    bio = BytesIO()
    resized.save(bio, "jpeg")
    bio.seek(0)
    return bio


def handle_product_id(update, context):
    print("handled")
    pass

class InCaseFilter(MessageFilter):
    def filter(self, message):
        pdb.set_trace()
        return 'Case:' in message.text

token = "2123147983:AAHvxdD1J0TX1yuxxfe3Xx-LefmEfGWLYns"

start_handler = CommandHandler('start', start)
products_hanlder = CommandHandler('products', get_products)
product_in_case = CallbackQueryHandler(handle_product_id)

updater = Updater(token=token, workers=8)
dispatcher = updater.dispatcher
dispatcher.add_handler(start_handler)
dispatcher.add_handler(products_hanlder)
dispatcher.add_handler(product_in_case)
updater.start_polling()