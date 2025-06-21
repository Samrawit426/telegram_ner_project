# Telegram Product NER

This project scrapes Telegram marketplace channels and extracts product, price, and location info using NER.

## Setup

1. Clone the repo and install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. Create a `.env` file with your Telegram credentials.

3. Add your target channels to `data/channels_to_crawl.txt`.

4. Run the scraper:
    ```bash
    python telegram_scraper.py
    ```

5. Process or label data in `data/labeled_telegram_data.txt`.

6. (Optional) Run `ner_inference.py` to simulate predictions.
