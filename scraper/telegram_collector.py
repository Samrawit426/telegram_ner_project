import os
import csv
import asyncio
from datetime import datetime
from telethon import TelegramClient
from telethon.errors import FloodWaitError, ChannelPrivateError
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

class TelegramCollector:
    def __init__(self):
        self.api_id = os.getenv('TG_API_ID')
        self.api_hash = os.getenv('TG_API_HASH')
        self.phone = os.getenv('phone')
        self.client = None
        self.output_dir = 'data/raw_data'
        os.makedirs(self.output_dir, exist_ok=True)
        
    async def connect(self):
        """Initialize and connect Telegram client."""
        self.client = TelegramClient('session', self.api_id, self.api_hash)
        await self.client.start(phone=self.phone)
        
    async def collect_channel_data(self, channel_username: str, limit: int = 1000) -> List[Dict]:
        """Collect messages from a specific channel.
        
        Args:
            channel_username: Username of the Telegram channel
            limit: Maximum number of messages to collect
            
        Returns:
            List of message dictionaries
        """
        messages = []
        try:
            entity = await self.client.get_entity(channel_username)
            channel_title = entity.title
            
            async for message in self.client.iter_messages(entity, limit=limit):
                # Skip empty messages
                if not message.text and not message.media:
                    continue
                    
                media_path = None
                if message.media and hasattr(message.media, 'photo'):
                    # Save media with timestamp to avoid conflicts
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename = f"{channel_username}_{message.id}_{timestamp}.jpg"
                    media_path = os.path.join(self.output_dir, 'media', filename)
                    os.makedirs(os.path.dirname(media_path), exist_ok=True)
                    await self.client.download_media(message.media, media_path)
                
                messages.append({
                    'channel_title': channel_title,
                    'channel_username': channel_username,
                    'message_id': message.id,
                    'text': message.text,
                    'date': message.date.isoformat(),
                    'media_path': media_path,
                    'views': message.views,
                    'forwards': message.forwards
                })
                
        except FloodWaitError as e:
            print(f"Rate limit hit for {channel_username}. Waiting {e.seconds} seconds")
            await asyncio.sleep(e.seconds)
        except ChannelPrivateError:
            print(f"Cannot access private channel {channel_username}")
        except Exception as e:
            print(f"Error collecting from {channel_username}: {e}")
            
        return messages
    
    async def collect_multiple_channels(self, channel_list_path: str):
        """Collect data from multiple channels listed in a file.
        
        Args:
            channel_list_path: Path to file containing channel usernames
        """
        # Read channel list
        with open(channel_list_path, 'r') as f:
            channels = [line.strip() for line in f if line.strip()]
            
        # Prepare CSV output
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        csv_path = os.path.join(self.output_dir, f'telegram_data_{timestamp}.csv')
        
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'channel_title', 'channel_username', 'message_id',
                'text', 'date', 'media_path', 'views', 'forwards'
            ])
            writer.writeheader()
            
            for channel in channels:
                print(f"Collecting data from {channel}...")
                messages = await self.collect_channel_data(channel)
                for msg in messages:
                    writer.writerow(msg)
                print(f"Collected {len(messages)} messages from {channel}")
                
        print(f"Data collection complete. Output saved to {csv_path}")
        
    async def close(self):
        """Close the Telegram client connection."""
        if self.client:
            await self.client.disconnect()
            
def main():
    collector = TelegramCollector()
    
    async def run():
        await collector.connect()
        await collector.collect_multiple_channels('data/channels_to_crawl.txt')
        await collector.close()
        
    asyncio.run(run())
    
if __name__ == '__main__':
    main()