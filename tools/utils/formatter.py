from typing import List

from database.filter_managers import MakeManager


def format_product_detail(product_detail: dict):
    text = ""
    text += f"Marka: {product_detail['make']}\n"
    text += f"Model: {product_detail['model']}\n"
    text += f"Şəhər: {product_detail['region']}\n"
    text += (
        f"Qiymət: {str(product_detail['price']) + ' ' + product_detail['currency']}\n"
    )
    text += f"Link: {product_detail['link']}"

    return text


def get_product_make_and_model(product_name: str) -> str:
    name_list = product_name.split(" ")

    old_make = name_list[0]

    var = False

    for i in range(0, len(name_list)):
        make = " ".join(name_list[: i + 1])

        if MakeManager().check_make_exists(make):
            var = True

        if not MakeManager().check_make_exists(make) and var:
            return old_make, " ".join(name_list[i:])
        old_make = make
    return product_name.split(" ")[0], " ".join(product_name.split(" ")[1:])
