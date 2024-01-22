#! /usr/bin/env python3

from PIL import Image
from PIL.ExifTags import TAGS
import sys
import os
from datetime import datetime

def octal_to_symbolic(octal):
    symbols = ['---', '--x', '-w-', '-wx', 'r--', 'r-x', 'rw-', 'rwx']
    mode = int(octal, 8)
    return ''.join(symbols[(mode >> shift) & 0b111] for shift in (6, 3, 0))

def extract_metadata(image_path):
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(f"Error opening {image_path}: {e}")
        return

    # Vérifier si l'extension est autorisée
    allowed_extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]
    if not any(image_path.lower().endswith(ext) for ext in allowed_extensions):
        print(f"Ignoring {image_path}: Unsupported image format.")
        return

    info_dict = {
        "Filename": image.filename,
        "Image Size": image.size,
        "Image Height": image.height,
        "Image Width": image.width,
        "Image Format": image.format,
        "Image Mode": image.mode,
        "Image is Animated": getattr(image, "is_animated", False),
        "Frames in Image": getattr(image, "n_frames", 1),
        "Time Original" : None,
        "File Permissions": None,
    }

    # Obtenir les informations sur les autorisations du fichier
    try:
        permissions = oct(os.stat(image_path).st_mode)[-3:]
        info_dict["File Permissions"] = octal_to_symbolic(permissions)
    except Exception as e:
        print(f"Error getting file permissions: {e}")

    exifdata = image.getexif()
    possible_tags = [36867, 36868, 306, 36881, 36882, 37520, 37521, 37522]  # Some common tags that might contain date information

    for tag_id in possible_tags:
        date_info = exifdata.get(tag_id)
        if date_info:
            info_dict["Time Original"] = date_info
            break

    for tag_id, value in exifdata.items():
        tag = TAGS.get(tag_id, tag_id)
        if isinstance(value, bytes):
            value = value.decode()
        print(f"{tag:15}: {value}")

    print("\nFull metadata:")
    for label, value in info_dict.items():
        print(f"{label:15}: {value}")

    print("\n" + "=" * 50 + "\n")  # Separator between images

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scorpion.py image1.jpg image2.png ...")
        sys.exit(1)

    for image_path in sys.argv[1:]:
        extract_metadata(image_path)