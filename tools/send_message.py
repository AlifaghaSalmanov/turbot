import asyncio
from typing import List

from database.managers import ProductManager, UserManager
from database.models import User
from keyboards.default.markups import get_reply_markup
from loader import bot, dp

from .utils.calculations import get_price_currency
from .utils.formatter import format_product_detail
from .validators import Validator


async def send_product_to_users(products: list):
    users = UserManager().get_all_active_users()

    for product in products:
        user: User
        for user in users:
            user_filter = UserManager().get_user_filter(user.tg_id)
            validator = Validator(user_filter)
            if user_filter:
                price = get_price_currency(
                    product.get("price", 0), product.get("currency", "AZN"), "AZN"
                )

                if not validator.validate_min_price(price):
                    continue

                if not validator.validate_max_price(price):
                    continue

                if not validator.validate_region_name(product.get("region", "")):
                    continue

                if not validator.validate_make_name(product.get("make", "")):
                    continue

                if not validator.validate_model_name(product.get("model", "")):
                    continue

                if not UserManager().check_user_is_active(user.tg_id):
                    continue

                try:

                    await bot.send_photo(
                        user.tg_id,
                        caption=format_product_detail(product),
                        photo=product["image"],
                        disable_notification=not UserManager().check_user_notification(
                            user.tg_id
                        ),
                        reply_markup=get_reply_markup("/bildirim", "/filter"),
                    )
                except Exception as e:
                    print(e)

        ProductManager().insert_product(product_id=product["product_id"])
        await asyncio.sleep(3.5)
