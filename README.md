# Turbo.az Scraper Telegram Bot

![turbot-ezgif com-resize](https://github.com/user-attachments/assets/231528df-3a55-4f46-b1b8-941dd9e3ec36)




## Description

This Telegram bot scrapes the turbo.az website for car listings and sends notifications to users based on their specified filter criteria. The bot allows users to set filters such as car make, model, price range, and other attributes to receive updates when new listings match their preferences. The bot supports multiple users, each with their own filter settings and notifications.
## Features

- Scrape turbo.az for car listings
- Send notifications via Telegram
- Set filters based on car attributes (make, model, price range, etc.)
- Support for multiple users
- Easy to use and configure

## Installation

### Prerequisites

- Python 3.9
- A Telegram account
- A Telegram bot token (you can get one from [BotFather](https://core.telegram.org/bots#botfather))

### Steps

1. Clone the repository:

    ```bash
    git clone https://github.com/AlifaghaSalmanov/turbot.git
    cd turbot
    ```

2. Create a virtual environment and activate it:

    ```bash
    python -m venv .venv
    source .venv/bin/activate   # On Windows, use `.venv\Scripts\activate`
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file and add your Telegram bot token and database configuration:

    ```bash
    echo "BOT_TOKEN=your_bot_token" > .env
    ```

5. Run the Alembic migrations to set up the database:

    ```bash
    alembic revision --autogenerate -m "create tables"
    alembic upgrade head
    ```

6. Populate the database with initial data:

    ```bash
    python add_data.py
    ```

7. Run the bot:

    ```bash
    python main.py
    ```

## Usage

Once the bot is running, users can interact with it on Telegram. The bot provides commands to set filters and start receiving notifications. Below are some common commands:

- `/start` - Start the bot and get a welcome message
- `/filter` - Set your filter criteria (e.g., make, model, price range)
- `/filter_bitir` - End the filtering process
- `/bildirim` - Enable or disable notifications

## Contributing

We welcome contributions! If you have suggestions for new features or improvements, feel free to open an issue or submit a pull request. Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a new Pull Request

