import asyncio
import os
import re

import requests
from bs4 import BeautifulSoup

from database.managers import ProductManager
from loader import BOT_KEY, bot, storage

from .send_message import send_product_to_users
from .utils.formatter import get_product_make_and_model


class WebScrapping:
    def __init__(self):
        self.new_products = []
        pass

    async def run(self):

        url = "https://turbo.az/autos"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
        }

        # Fetch the webpage content using requests
        response = requests.get(url, headers=headers)
        html_content = response.text

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")

        # Get all elements with class "product-price"
        product_prices = soup.select(".product-price")
        product_links = soup.select(".products-i__link")
        product_images = soup.select(".products-i__top img")
        product_names = soup.select(".products-i__name")
        product_datetimes = soup.select(".products-i__datetime")

        print("Elements found")

        for price_data, link_data, image_data, name_data, datetime_data in zip(
            product_prices,
            product_links,
            product_images,
            product_names,
            product_datetimes,
        ):
            # Extract data from each element
            price_data = price_data.get_text().strip().replace(" ", "")
            currency = re.findall(r"\D+", price_data)[0]
            price = int(re.findall(r"\d+", price_data)[0])

            href = link_data.get("href")
            link_href = "https://turbo.az" + href

            image_src = image_data.get("src")

            product_id = re.findall(r"/autos/(\d+)-", href)[0]
            product_name = name_data.get_text().strip()
            product_make, product_model = get_product_make_and_model(product_name)

            datetime = datetime_data.get_text().strip()
            product_region = datetime.split(",")[0]

            product = {
                "product_id": product_id,
                "make": product_make,
                "model": product_model,
                "region": product_region,
                "price": price,
                "currency": currency,
                "link": link_href,
                "image": image_src,
            }

            # check if the product exists in the database (simulated with cached_data)
            cached_data = {}  # Simulated cached data
            if product_id in cached_data.get("products_id", []):
                continue

            # Assuming ProductManager().product_exists is a function checking existence
            if not ProductManager().product_exists(product["product_id"]):
                self.new_products.append(product)

        await storage.set_data(
            chat=BOT_KEY,
            user=BOT_KEY,
            data={
                "products_id": [product["product_id"] for product in self.new_products]
            },
        )

        if self.new_products:
            await send_product_to_users(self.new_products)

        self.new_products = []

    async def job(self):
        await self.run()

    async def start(self):
        while True:
            print("Running the job")
            # Run pending jobs
            await self.job()

            await asyncio.sleep(os.getenv("SCRAPPER_INTERVAL", 60))
