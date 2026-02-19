import logging
from extractors.logs import LogGenerator
from extractors.wikipedia import WikipediaExtractor
from extractors.unsplash import UnsplashExtractor

from transformers.log_transformer import LogTransformer
from transformers.text_transformer import TextTransformer
from transformers.image_transformer import ImageTransformer

from loaders.minio_loader import MinioLoader
from loaders.mongo_loader import MongoLoader

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_pipeline():
    logger.info("Starting the ETL Pipeline...")

    # 1. Initialize Loaders
    minio = MinioLoader()
    mongo = MongoLoader()

    # ==========================================
    # PIPELINE 1: Synthetic Logs
    # ==========================================
    logger.info("--- Processing Logs ---")
    log_ext = LogGenerator()
    log_trans = LogTransformer()
    
    raw_logs = log_ext.extract(count=10) # Extract 10 fake logs
    if raw_logs:
        # Save raw logs as a single text file
        minio.load_raw("logs/raw_logs.txt", "\n".join(raw_logs))
        
        for log_str in raw_logs:
            processed = log_trans.transform(log_str)
            if processed:
                mongo.load_metadata(processed)
                minio.load_processed(f"logs/{processed['file_id']}.json", processed)

    # ==========================================
    # PIPELINE 2: Wikipedia Text
    # ==========================================
    logger.info("--- Processing Wikipedia ---")
    wiki_ext = WikipediaExtractor()
    wiki_trans = TextTransformer()
    
    # Let's extract an article related to your major
    raw_wiki = wiki_ext.extract("Computer_security")
    if raw_wiki:
        # Save raw JSON
        minio.load_raw(f"wikipedia/{raw_wiki['title']}_raw.json", raw_wiki)
        
        processed = wiki_trans.transform(raw_wiki)
        if processed:
            mongo.load_metadata(processed)
            minio.load_processed(f"wikipedia/{processed['file_id']}.json", processed)

    # ==========================================
    # PIPELINE 3: Unsplash Images
    # ==========================================
    logger.info("--- Processing Unsplash ---")
    img_ext = UnsplashExtractor()
    img_trans = ImageTransformer()
    
    # Search for an image
    raw_images = img_ext.extract("data center", count=2)
    if raw_images:
        # Save raw metadata
        minio.load_raw("unsplash/raw_search_results.json", raw_images)
        
        for raw_img in raw_images:
            processed = img_trans.transform(raw_img)
            if processed:
                mongo.load_metadata(processed)
                minio.load_processed(f"unsplash/{processed['file_id']}.json", processed)

    logger.info("ETL Pipeline completed successfully!")

if __name__ == "__main__":
    run_pipeline()