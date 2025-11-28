import requests
from PIL import Image
from pdf2image import convert_from_bytes
from io import BytesIO
from typing import List

def download_file(url: str) -> bytes:
    response = requests.get(url)
    response.raise_for_status()
    return response.content

def process_document(url: str) -> List[Image.Image]:
    content = download_file(url)
    
    # Try to open as image first
    try:
        image = Image.open(BytesIO(content))
        return [image]
    except IOError:
        # If not an image, try as PDF
        try:
            images = convert_from_bytes(content)
            return images
        except Exception as e:
            raise ValueError(f"Could not process document: {e}")
