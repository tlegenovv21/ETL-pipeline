import argparse
import logging
from pythonjsonlogger import jsonlogger

from extractors.logs import LogGenerator
from extractors.wikipedia import WikipediaExtractor
from extractors.unsplash import UnsplashExtractor

from transformers.log_transformer import LogTransformer
from transformers.text_transformer import TextTransformer
from transformers.image_transformer import ImageTransformer

from loaders.minio_loader import MinioLoader
from loaders.mongo_loader import MongoLoader
from typing import Dict, Any, Optional

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# Configure strict JSON Logging
logger = logging.getLogger()
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(message)s')

def run_pipeline(source: str = "all") -> None:
    logger.info("Starting the ETL Pipeline...", extra={"source": source})

    # 1. Initialize Loaders
    minio = MinioLoader()
    mongo = MongoLoader()

    # ==========================================
    # PIPELINE 1: Synthetic Logs
    # ==========================================
    if source in ["all", "logs"]:
        logger.info("Processing Synthetic Logs")
        raw_logs = LogGenerator().extract(count=10)
        if raw_logs:
            minio.load_raw("logs/raw_logs.txt", "\n".join(raw_logs))
            for log_str in raw_logs:
                processed = LogTransformer().transform(log_str)
                if processed:
                    mongo.load_metadata(processed)
                    minio.load_processed(f"logs/{processed['file_id']}.json", processed)

    # ==========================================
    # PIPELINE 2: Wikipedia Text
    # ==========================================
    if source in ["all", "wikipedia"]:
        logger.info("Processing Wikipedia")
        raw_wiki = WikipediaExtractor().extract("DevOps") 
        if raw_wiki:
            minio.load_raw(f"wikipedia/{raw_wiki['title']}_raw.json", raw_wiki)
            processed = TextTransformer().transform(raw_wiki)
            if processed:
                mongo.load_metadata(processed)
                minio.load_processed(f"wikipedia/{processed['file_id']}.json", processed)

    # ==========================================
    # PIPELINE 3: Unsplash Images
    # ==========================================
    if source in ["all", "unsplash"]:
        logger.info("Processing Unsplash")
        raw_images = UnsplashExtractor().extract("data center", count=2)
        if raw_images:
            minio.load_raw("unsplash/raw_search_results.json", raw_images)
            for raw_img in raw_images:
                processed = ImageTransformer().transform(raw_img)
                if processed:
                    mongo.load_metadata(processed)
                    minio.load_processed(f"unsplash/{processed['file_id']}.json", processed)

    logger.info("ETL Pipeline completed successfully!")

if __name__ == "__main__":
    print("--- PIPELINE completed successfully! ---")
    parser = argparse.ArgumentParser(description="Run ETL Pipeline")
    parser.add_argument("--source", type=str, default="all", choices=["all", "logs", "wikipedia", "unsplash"], help="Data source to extract")
    args = parser.parse_args()
    run_pipeline(args.source)