from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from database.filter_managers import ModelManager
from keyboards.default.markups import (
    get_move_buttons,
    get_next_button,
    get_previous_button,
)

"""
region_cb = CallbackData("region", "id", "name", "offset", "limit")


def get_regions_markup(
    offset: int = 0,
    limit: int = 16,
):
    markup = InlineKeyboardMarkup()
    all_regions = RegionManager().get_all_regions()
    # Apply offset and limit
    regions = all_regions[offset : offset + limit]

    # Create pairs of regions
    region_pairs = zip(regions[::2], regions[1::2])

    if offset == 0:
        markup.row(
            InlineKeyboardButton(
                "🌀Hamısı🌀",
                callback_data=region_cb.new(
                    id="None", name="Hamısı", offset=offset, limit=limit
                ),
            )
        )

    for region1, region2 in region_pairs:
        button1 = InlineKeyboardButton(
            region1[1],
            callback_data=region_cb.new(
                id=region1[0], name=region1[1], offset=offset, limit=limit
            ),
        )
        button2 = InlineKeyboardButton(
            region2[1],
            callback_data=region_cb.new(
                id=region2[0], name=region2[1], offset=offset, limit=limit
            ),
        )
        markup.row(button1, button2)

    # If there is an odd number of regions, add the last one in a separate row
    if len(regions) % 2 != 0:
        markup.add(
            InlineKeyboardButton(
                regions[-1][1],
                callback_data=region_cb.new(
                    id=regions[-1][0], name=regions[-1][1], offset=offset, limit=limit
                ),
            )
        )

    # Add move buttons only if there are more regions to show
    if offset == 0:
        markup.row(
            get_next_button(
                next_callback_data=region_cb.new(
                    id="None", name="next", offset=offset + limit, limit=limit
                ),
            )
        )

    elif offset + limit < len(all_regions):
        markup.row(
            *get_move_buttons(
                pervious_callback_data=region_cb.new(
                    id="None",
                    name="previous",
                    offset=max(0, offset - limit),
                    limit=limit,
                ),
                next_callback_data=region_cb.new(
                    id="None", name="next", offset=offset + limit, limit=limit
                ),
            )
        )
    else:
        markup.row(
            get_previous_button(
                region_cb.new(
                    id="None", name="previous", offset=offset - limit, limit=limit
                )
            )
        )

    return markup

"""


model_cb = CallbackData("model", "id", "make_id", "name", "offset", "limit")


def get_models_markup(
    make_id: int,
    offset: int = 0,
    limit: int = 16,
):
    markup = InlineKeyboardMarkup()
    all_models = ModelManager().get_all_models_by_make_id(make_id=make_id)
    # Apply offset and limit
    models = all_models[offset : offset + limit]

    # Create pairs of models
    model_pairs = zip(models[::2], models[1::2])

    if offset == 0:
        markup.row(
            InlineKeyboardButton(
                "🌀Hamısı🌀",
                callback_data=model_cb.new(
                    id="None", make_id="None", name="Hamısı", offset=offset, limit=limit
                ),
            )
        )

    for model1, model2 in model_pairs:
        button1 = InlineKeyboardButton(
            model1[1],
            callback_data=model_cb.new(
                id=model1[0],
                make_id=make_id,
                name=model1[1],
                offset=offset,
                limit=limit,
            ),
        )
        button2 = InlineKeyboardButton(
            model2[1],
            callback_data=model_cb.new(
                id=model2[0],
                make_id=make_id,
                name=model2[1],
                offset=offset,
                limit=limit,
            ),
        )
        markup.row(button1, button2)

    # If there is an odd number of models, add the last one in a separate row
    if len(models) % 2 != 0:
        markup.add(
            InlineKeyboardButton(
                models[-1][1],
                callback_data=model_cb.new(
                    id=models[-1][0],
                    make_id=make_id,
                    name=models[-1][1],
                    offset=offset,
                    limit=limit,
                ),
            )
        )

    # Add move buttons only if there are more models to show
    if offset == 0:
        markup.row(
            get_next_button(
                next_callback_data=model_cb.new(
                    id="None",
                    make_id=make_id,
                    name="next",
                    offset=offset + limit,
                    limit=limit,
                ),
            )
        )

    elif offset + limit < len(all_models):
        markup.row(
            *get_move_buttons(
                pervious_callback_data=model_cb.new(
                    id="None",
                    name="previous",
                    make_id=make_id,
                    offset=max(0, offset - limit),
                    limit=limit,
                ),
                next_callback_data=model_cb.new(
                    id="None",
                    make_id=make_id,
                    name="next",
                    offset=offset + limit,
                    limit=limit,
                ),
            )
        )
    else:
        markup.row(
            get_previous_button(
                model_cb.new(
                    id="None",
                    make_id=make_id,
                    name="previous",
                    offset=offset - limit,
                    limit=limit,
                )
            )
        )

    return markup
