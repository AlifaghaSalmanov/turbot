from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData


def get_filter_markup():
    markup = InlineKeyboardMarkup()
    buttons = []
    make_buttons = []
    for title in ["minimum qiymət", "maksimum qiymət"]:
        buttons.append(
            InlineKeyboardButton(
                title,
                callback_data=title,
            )
        )
    markup.row(*buttons)

    markup.row(
        InlineKeyboardButton(
            "Şəhər🏙️",
            callback_data="city",
        )
    )

    for cb_data, title in [("make", "Marka🚘"), ("model", "Model🛞")]:
        make_buttons.append(
            InlineKeyboardButton(
                title,
                callback_data=cb_data,
            )
        )

    markup.row(*make_buttons)

    markup.row(
        InlineKeyboardButton(
            "Filter bitir✅",
            callback_data="filter_bitir",
        )
    )

    return markup
