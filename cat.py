import os
import requests
from PIL import Image
import numpy as np

# Function to retrieve the cat image from the Cat API
def get_cat_image(api_key):
    url = "https://api.thecatapi.com/v1/images/search"
    headers = {"x-api-key": api_key}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        image_url = response.json()[0]["url"]
        image_response = requests.get(image_url, stream=True)
        image_response.raw.decode_content = True
        return Image.open(image_response.raw)
    else:
        raise Exception("Failed to retrieve cat image")

# Function to convert the image to ASCII characters
def image_to_ascii(image, width=100):
    # Resize image while maintaining aspect ratio
    aspect_ratio = image.height / image.width
    new_height = int(aspect_ratio * width)
    resized_image = image.resize((width, new_height))

    # Convert image to grayscale
    grayscale_image = resized_image.convert("L")

    # Define ASCII characters
    ascii_chars = "@%#*+=-:. "

    # Convert pixels to ASCII characters
    pixels = np.array(grayscale_image)
    ascii_image = []
    for row in pixels:
        ascii_row = "".join([ascii_chars[pixel // 32] for pixel in row])
        ascii_image.append(ascii_row)
    
    return "\n".join(ascii_image)

# Function to print the ASCII representation of the cat image
def print_ascii_image(ascii_image):
    print(ascii_image)

# Main function to execute the steps
def main():
    api_key = os.getenv("CATKEY")
    if not api_key:
        raise Exception("API key not found in CATKEY environment variable")
    
    cat_image = get_cat_image(api_key)
    ascii_image = image_to_ascii(cat_image)
    print_ascii_image(ascii_image)

if __name__ == "__main__":
    main()
