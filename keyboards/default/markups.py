from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

pervious_message = "👈 geri"
next_message = "irəli 👉"


def get_reply_markup(*args):
    buttons = []
    for text in args:
        button = KeyboardButton(text)
        buttons.append(button)

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.add(*buttons)

    return keyboard


def get_move_buttons(pervious_callback_data="Next", next_callback_data="Previous"):
    pervious_button = InlineKeyboardButton(
        pervious_message, callback_data=pervious_callback_data
    )
    next_button = InlineKeyboardButton(next_message, callback_data=next_callback_data)

    return pervious_button, next_button


def get_previous_button(pervious_callback_data="Previous"):
    return InlineKeyboardButton(pervious_message, callback_data=pervious_callback_data)


def get_next_button(next_callback_data="Next"):
    return InlineKeyboardButton(next_message, callback_data=next_callback_data)
