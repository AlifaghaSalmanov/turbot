from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup

from database.managers import FilterManager, UserManager
from database.models import User
from database.utils.formatter import format_user_filter
from keyboards.default.markups import get_reply_markup
from keyboards.inline.filters import get_filter_markup
from keyboards.inline.makes import get_makes_markup, make_cb
from keyboards.inline.models import get_models_markup, model_cb
from keyboards.inline.regions import get_regions_markup, region_cb
from loader import BOT_KEY, bot, dp, storage

from .utils.state import finish_state


class PriceFilter(StatesGroup):
    waiting_for_min_price = State()
    waiting_for_max_price = State()
    waiting_for_start_max_price = State()


class FilterHandler:

    @dp.message_handler(state=PriceFilter.waiting_for_min_price)
    async def set_min_price(message: types.Message, state: FSMContext):
        min_price = message.text

        if await finish_state(message.text, state):
            await FilterHandler.cancel_filter(message, state)
            return None

        if not min_price.isdigit():
            await message.answer("Qiyməti sadəcə rəqəmlə daxil edin.")
            return

        FilterManager().update_filter(tg_id=message.from_user.id, min_price=min_price)
        await message.answer(
            f"🟢Minimum qiymət *{min_price} AZN* olaraq təyin edildi.",
            parse_mode="Markdown",
            reply_markup=get_reply_markup("/filter"),
        )

        await state.finish()

        await FilterHandler.filter(message)

    @dp.message_handler(
        state=[
            PriceFilter.waiting_for_max_price,
            PriceFilter.waiting_for_start_max_price,
        ]
    )
    async def set_max_price(message: types.Message, state: FSMContext):
        max_price = message.text

        if await finish_state(message.text, state):
            await FilterHandler.cancel_filter(message, state)
            return None

        if not max_price.isdigit():
            await message.answer("Qiyməti sadəcə rəqəmlə daxil edin.")
            return

        FilterManager().update_filter(tg_id=message.from_user.id, max_price=max_price)
        await message.answer(
            f"🟢Maksimum qiymət *{max_price} AZN* olaraq təyin edildi.",
            parse_mode="Markdown",
        )

        # write if state = waiting_for_max_price then call filter
        if await state.get_state() == "PriceFilter:waiting_for_max_price":
            await FilterHandler.filter(message)
        else:
            UserManager().update_user(tg_id=message.from_user.id, is_active=True)

        await state.finish()

    # write call back for Imtina
    @dp.message_handler(commands=["Imtina"])
    async def cancel_filter(message: types.Message, state: FSMContext):
        current_state = await state.get_state()
        text = "🟢Filter etməyə son verildi."
        if current_state is None:
            await message.answer(text, reply_markup=get_reply_markup("/filter"))
            return
        await state.finish()
        await message.answer(text, reply_markup=get_reply_markup("/filter"))

    @dp.message_handler(commands=["filter"])
    async def filter(message: types.Message):

        UserManager().update_user(tg_id=message.from_user.id, is_active=False)

        await message.answer(
            "Nəyə əsasən filter etmək istəyirsiniz seçin.\nFilter bitdikdən sonra təkrar avtomobil axtarışına başlamaq üçün _Filter bitir_ ✅-ə basın.",
            reply_markup=get_reply_markup("/filter_bitir"),
            parse_mode="Markdown",
        )
        await message.answer(
            format_user_filter(
                tg_id=(
                    message.chat.id
                    if isinstance(message, types.Message)
                    else message.chat.id
                )
            ),
            parse_mode="Markdown",
            reply_markup=get_filter_markup(),
        )
        pass

    @dp.callback_query_handler(
        lambda callback_query: callback_query.data == "minimum qiymət"
    )
    async def set_min_price(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        await callback_query.message.answer(
            "🟡Minimum qiyməti AZN valyutasına əsasən yazın.\nÖrnək:\n2000",
            reply_markup=get_reply_markup("/filter_bitir"),
        )

        await PriceFilter.waiting_for_min_price.set()

    @dp.callback_query_handler(
        lambda callback_query: callback_query.data == "maksimum qiymət"
    )
    async def set_max_price(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        await callback_query.message.answer(
            "🟡Maksimum qiyməti AZN valyutasına əsasən yazın.\nÖrnək:\n9000",
            reply_markup=get_reply_markup("/filter_bitir"),
        )

        await PriceFilter.waiting_for_max_price.set()

    @dp.callback_query_handler(text=["city"])
    async def set_city(call: types.CallbackQuery):

        await call.message.answer(
            "Şəhəri Seçin. Səhifə: 1", reply_markup=get_regions_markup()
        )

    @dp.callback_query_handler(region_cb.filter())
    async def handle_region_callback(
        query: types.CallbackQuery, callback_data: dict, state: FSMContext
    ):
        if await finish_state(query.message.text, state):
            await FilterHandler.cancel_filter(query.message, state)

        region_id = int(callback_data["id"]) if callback_data["id"] != "None" else None
        name = callback_data["name"]
        offset = int(callback_data["offset"])
        limit = int(callback_data["limit"])

        if name in ["next", "previous"]:
            # If the user clicked the next or previous button, edit the message with the new markup
            await query.message.edit_text(
                f"Şəhəri Seçin. Səhifə: {offset//limit + 1}",
                reply_markup=get_regions_markup(offset, limit),
            )
        else:

            await query.message.answer(
                f"🟢Şəhər *{name}* olaraq təyin edildi.",
                parse_mode="Markdown",
                reply_markup=get_reply_markup("/filter"),
            )

            FilterManager().update_filter(
                tg_id=query.from_user.id, region_id=region_id, region_name=name
            )

            # Call the filter function
            await FilterHandler.filter(query.message)
            pass

    @dp.callback_query_handler(text="make")
    async def set_make(call: types.CallbackQuery):
        await call.message.answer(
            "Markanı Seçin. Səhifə: 1", reply_markup=get_makes_markup()
        )

    @dp.callback_query_handler(make_cb.filter())
    async def handle_make_callback(
        query: types.CallbackQuery, callback_data: dict, state: FSMContext
    ):
        if await finish_state(query.message.text, state):
            await FilterHandler.cancel_filter(query.message, state)

        make_id = int(callback_data["id"]) if callback_data["id"] != "None" else None
        name = callback_data["name"]
        offset = int(callback_data["offset"])
        limit = int(callback_data["limit"])

        if name in ["next", "previous"]:
            # If the user clicked the next or previous button, edit the message with the new markup
            await query.message.edit_text(
                f"Markanı Seçin. Səhifə: {offset//limit+1}",
                reply_markup=get_makes_markup(offset, limit),
            )

        else:

            await query.message.answer(
                f"🟢Marka *{name}* olaraq təyin edildi.",
                parse_mode="Markdown",
                reply_markup=get_reply_markup("/filter"),
            )

            FilterManager().update_filter(
                tg_id=query.from_user.id, make_id=make_id, make_name=name
            )

            # Call the filter function
            await FilterHandler.filter(query.message)
            pass

    @dp.callback_query_handler(text="model")
    async def set_model(call: types.CallbackQuery):
        user = UserManager().get_user(call.from_user.id)
        if not user or not user.filter or not user.filter.make_id:
            await call.message.answer("Marka seçilməyib.")
            return

        await call.message.answer(
            "Modeli Seçin. Səhifə: 1",
            reply_markup=get_models_markup(make_id=user.filter.make_id),
        )

    @dp.callback_query_handler(model_cb.filter())
    async def handle_model_callback(
        query: types.CallbackQuery, callback_data: dict, state: FSMContext
    ):
        if await finish_state(query.message.text, state):
            await FilterHandler.cancel_filter(query.message, state)

        model_id = int(callback_data["id"]) if callback_data["id"] != "None" else None
        make_id = (
            int(callback_data["make_id"])
            if callback_data["make_id"] != "None"
            else None
        )
        name = callback_data["name"]
        offset = int(callback_data["offset"])
        limit = int(callback_data["limit"])

        if name in ["next", "previous"]:
            # If the user clicked the next or previous button, edit the message with the new markup
            await query.message.edit_text(
                f"Modeli Seçin. Səhifə: {offset//limit+1}",
                reply_markup=get_models_markup(make_id, offset, limit),
            )

        else:

            await query.message.answer(
                f"🟢Model *{name}* olaraq təyin edildi.",
                parse_mode="Markdown",
                reply_markup=get_reply_markup("/filter"),
            )

            FilterManager().update_filter(
                tg_id=query.from_user.id, model_id=model_id, model_name=name
            )

            # Call the filter function
            await FilterHandler.filter(query.message)
            pass

    @dp.callback_query_handler(text="filter_bitir")
    @dp.message_handler(commands=["filter_bitir"])
    async def filter_done(
        call: Union[types.CallbackQuery, types.Message], state: FSMContext
    ):
        text = "🟢Filter etməyə son verildi."
        current_state = await state.get_state()
        if current_state:
            await state.finish()

        if isinstance(call, types.CallbackQuery):
            await call.message.answer(
                text, reply_markup=get_reply_markup("/bildirim", "/filter")
            )
        else:
            await call.answer(
                text, reply_markup=get_reply_markup("/bildirim", "/filter")
            )
        UserManager().update_user(tg_id=call.from_user.id, is_active=True)
