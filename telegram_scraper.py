from telethon import TelegramClient
import csv
import os
from dotenv import load_dotenv

load_dotenv('.env')

api_id = os.getenv('TG_API_ID')
api_hash = os.getenv('TG_API_HASH')
phone = os.getenv('phone')

async def scrape_channel(client, channel_username, writer, media_dir):
    entity = await client.get_entity(channel_username)
    channel_title = entity.title
    async for message in client.iter_messages(entity, limit=1000):
        print(f"Processing message {message.id}")
        media_path = None
        if message.media and hasattr(message.media, 'photo'):
            filename = f"{channel_username}_{message.id}.jpg"
            media_path = os.path.join(media_dir, filename)
            await client.download_media(message.media, media_path)
        
        writer.writerow([channel_title, channel_username, message.id, message.message, message.date, media_path])

async def main():
    client = TelegramClient('session', api_id, api_hash)
    await client.start()

    os.makedirs('photos', exist_ok=True)

    with open('data/telegram_data.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Channel Title', 'Channel Username', 'ID', 'Message', 'Date', 'Media Path'])

        with open('data/channels_to_crawl.txt', 'r') as f:
            channels = [line.strip() for line in f.readlines()]

        for channel in channels:
            await scrape_channel(client, channel, writer, 'photos')
            print(f"Scraped data from {channel}")

    await client.disconnect()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
