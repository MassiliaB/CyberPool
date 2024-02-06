# Arachnida

## Spider
The spider program allow you to extract all the images from a website, recursively, by providing a url as a parameter.

Usage:

```bash
./spider [-rlp] URL
```

• Option -r : recursively downloads the images in a URL received as a parameter.
• Option -r -l [N] : indicates the maximum depth level of the recursive download.
If not indicated, it will be 5.
• Option -p [PATH] : indicates the path where the downloaded files will be saved.
If not specified, ./data/ will be used.

The program will download the following extensions by default:
• .jpg/jpeg
• .png
• .gif
• .bmp

## Scorpion
The scorpion program receive image files as parameters and parse them for EXIF and other metadata. It handles the same extensions that spider handles.

```bash
./scorpion FILE1 [FILE2 ...]
```
