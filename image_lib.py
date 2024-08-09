import requests
from PIL import Image
import io
import ctypes
from tkinter import *
from tkinter import filedialog
from datetime import date
import os

# Function to download an image from a URL
def download_image(image_url):
    try:
        response = requests.get(image_url, allow_redirects=True)
        response.raise_for_status()  # Raise HTTPError for bad responses (e.g., 404)
        
        # Check if the response contains image data
        if 'image' not in response.headers.get('content-type', ''):
            print("Error: The response does not contain image data.")
            return None
        
        return response.content
    except requests.HTTPError as e:
        print("HTTP Error:", e)
    except Exception as e:
        print("Error downloading image:", e)
    return None

# Function to save image data to a file
def save_image_file(image_data, image_path):
    try:
        with open(image_path, 'wb') as f:
            f.write(image_data)
        return True
    except Exception as e:
        print("Error saving image:", e)
    return False

# Function to set desktop background
def set_desktop_background(image_path):
    try:
        SPI_SETDESKWALLPAPER = 20
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 3)
        return True
    except Exception as e:
        print("Error setting desktop background image:", e)
    return False

# Function to download and set desktop background
def download_and_set_background(image_url):
    image_data = download_image(image_url)
    if image_data:
        image_path = "temp_image.png"
        saved = save_image_file(image_data, image_path)
        if saved:
            set_desktop_background(image_path)
        else:
            print("Failed to save image.")

# Function to open a file dialog to select an image file
def select_image():
    root = Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        set_desktop_background(file_path)

# Function to create the GUI
def create_gui():
    root = Tk()
    root.title("Desktop Image Viewer")
    root.geometry("400x200")

    # Button to select an image file
    select_image_button = Button(root, text="Select Image File", command=select_image)
    select_image_button.pack(pady=10)

    # Entry to input image URL
    url_entry = Entry(root, width=50)
    url_entry.pack()

    # Button to download and set desktop background from URL
    set_from_url_button = Button(root, text="Set Desktop Background from URL", command=lambda: download_and_set_background(url_entry.get()))
    set_from_url_button.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    create_gui()