from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from database.filter_managers import MakeManager
from keyboards.default.markups import (
    get_move_buttons,
    get_next_button,
    get_previous_button,
)

make_cb = CallbackData("make", "id", "name", "offset", "limit")


def get_makes_markup(
    offset: int = 0,
    limit: int = 16,
):
    markup = InlineKeyboardMarkup()
    all_makes = MakeManager().get_all_makes()
    # Apply offset and limit
    makes = all_makes[offset : offset + limit]

    # Create pairs of makes
    make_pairs = zip(makes[::2], makes[1::2])

    if offset == 0:
        markup.row(
            InlineKeyboardButton(
                "🌀Hamısı🌀",
                callback_data=make_cb.new(
                    id="None", name="Hamısı", offset=offset, limit=limit
                ),
            )
        )

    for make1, make2 in make_pairs:
        button1 = InlineKeyboardButton(
            make1[1],
            callback_data=make_cb.new(
                id=make1[0], name=make1[1], offset=offset, limit=limit
            ),
        )
        button2 = InlineKeyboardButton(
            make2[1],
            callback_data=make_cb.new(
                id=make2[0], name=make2[1], offset=offset, limit=limit
            ),
        )
        markup.row(button1, button2)

    # If there is an odd number of makes, add the last one in a separate row
    if len(makes) % 2 != 0:
        markup.add(
            InlineKeyboardButton(
                makes[-1][1],
                callback_data=make_cb.new(
                    id=makes[-1][0], name=makes[-1][1], offset=offset, limit=limit
                ),
            )
        )

    # Add move buttons only if there are more makes to show
    if offset == 0:
        markup.row(
            get_next_button(
                next_callback_data=make_cb.new(
                    id="None", name="next", offset=offset + limit, limit=limit
                ),
            )
        )

    elif offset + limit < len(all_makes):
        markup.row(
            *get_move_buttons(
                pervious_callback_data=make_cb.new(
                    id="None",
                    name="previous",
                    offset=max(0, offset - limit),
                    limit=limit,
                ),
                next_callback_data=make_cb.new(
                    id="None", name="next", offset=offset + limit, limit=limit
                ),
            )
        )

    else:
        markup.row(
            get_previous_button(
                make_cb.new(
                    id="None", name="previous", offset=offset - limit, limit=limit
                )
            )
        )

    return markup
