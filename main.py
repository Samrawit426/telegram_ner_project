import os
import asyncio
from datetime import datetime
from scraper.telegram_collector import TelegramCollector
from utils.data_processor import process_telegram_data

def setup_directories():
    """Create necessary directories if they don't exist."""
    dirs = ['data/raw_data', 'data/processed', 'models']
    for d in dirs:
        os.makedirs(d, exist_ok=True)

def get_latest_csv(directory: str) -> str:
    """Get the path of the most recent CSV file in the directory."""
    csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
    if not csv_files:
        raise FileNotFoundError("No CSV files found in the directory")
        
    latest = max(csv_files, key=lambda x: os.path.getctime(os.path.join(directory, x)))
    return os.path.join(directory, latest)

async def collect_telegram_data():
    """Collect data from Telegram channels."""
    collector = TelegramCollector()
    try:
        await collector.connect()
        await collector.collect_multiple_channels('data/channels_to_crawl.txt')
    finally:
        await collector.close()

def process_data():
    """Process the collected data and convert to CoNLL format."""
    try:
        # Get the latest collected data
        latest_csv = get_latest_csv('data/raw_data')
        
        # Generate output path with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = f'data/processed/telegram_ner_data_{timestamp}.conll'
        
        # Process the data
        process_telegram_data(latest_csv, output_path)
        print(f"Data processed and saved to {output_path}")
        
        return output_path
    except Exception as e:
        print(f"Error processing data: {e}")
        return None

def main():
    # Create necessary directories
    setup_directories()
    
    # Collect data from Telegram
    print("Starting data collection from Telegram channels...")
    asyncio.run(collect_telegram_data())
    
    # Process the collected data
    print("\nProcessing collected data...")
    processed_file = process_data()
    
    if processed_file:
        print("\nWorkflow completed successfully!")
        print(f"Processed data saved to: {processed_file}")
        print("\nNext steps:")
        print("1. Review and manually correct the NER labels in the processed file")
        print("2. Use the labeled data to train the NER model using train_ner_model.ipynb")
    else:
        print("\nWorkflow completed with errors. Please check the logs above.")

if __name__ == '__main__':
    main()