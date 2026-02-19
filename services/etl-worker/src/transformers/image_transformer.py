from .base import BaseTransformer
import requests
from PIL import Image
import imagehash
from io import BytesIO

class ImageTransformer(BaseTransformer):
    def transform(self, data):
        if not data or 'url' not in data:
            return None

        image_url = data['url']
        
        try:
            # Download image into memory
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()
            img_bytes = BytesIO(response.content)
            
            # Open with Pillow for processing
            with Image.open(img_bytes) as img:
                width, height = img.size
                img_format = img.format or "JPEG"
                img_hash = str(imagehash.phash(img))

            specific_metadata = {
                "width": width,
                "height": height,
                "format": img_format,
                "image_hash": img_hash,
                "description": data.get("description"),
                "photographer": data.get("photographer")
            }
            # Return using the unified schema
            return self.unify_metadata(
                raw_id=data.get("id"),
                source_type="unsplash",
                data_type="image",
                content=image_url, 
                metadata=specific_metadata
            )

        except Exception as e:
            # The typo was likely here! It should be 'e', not 'earr'
            print(f"Failed to transform image {image_url}: {e}")
            return None