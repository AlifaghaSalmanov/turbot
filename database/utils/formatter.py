from aiogram import types

from ..managers import UserManager


def format_user_filter(tg_id: int):
    user = UserManager().get_user(tg_id)

    if not user or (not user.filter):
        return "Filter tapılmadı."
    text = "Filterlər:\n"
    text += f"Minimum qiymət: *{user.filter.min_price}* AZN\n"
    text += f"Maksimum qiymət: *{user.filter.max_price}* AZN\n"
    text += f"🏙️Şəhər: *{user.filter.region_name}* \n"
    text += f"🚘Marka: *{user.filter.make_name}* \n"
    text += f"🛞Model: *{user.filter.model_name}* \n"

    return text
