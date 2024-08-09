from datetime import date
import os
import image_lib
import tkinter as tk
from tkinter import ttk, messagebox
import apod_desktop

# Full paths of the image cache folder and database
script_dir = os.path.dirname(os.path.abspath(__file__))
image_cache_dir = os.path.join(script_dir, 'images')
image_cache_db = os.path.join(image_cache_dir, 'image_cache.db')

class AstronomyDesktopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("APOD Desktop")
        self.root.geometry("400x200")
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.root, text="Enter APOD Date (YYYY-MM-DD):").grid(row=0, column=0, padx=10, pady=10)
        self.date_entry = ttk.Entry(self.root)
        self.date_entry.grid(row=0, column=1, padx=10, pady=10)
        
        self.download_button = ttk.Button(self.root, text="Download and Set as Desktop", command=self.download_and_set)
        self.download_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.titles_listbox = tk.Listbox(self.root)
        self.titles_listbox.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.load_titles_button = ttk.Button(self.root, text="Load Titles", command=self.load_titles)
        self.load_titles_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def download_and_set(self):
        apod_date_str = self.date_entry.get()
        try:
            apod_date = date.fromisoformat(apod_date_str)
        except ValueError:
            messagebox.showerror("Invalid date format. Please use YYYY-MM-DD.")
            return

        status = apod_desktop.add_apod_to_cache(apod_date)
        if status:
            apod_info = apod_desktop.get_apod_info(status)
            image_lib.set_desktop_background_image(apod_info['file_path'])
            messagebox.showinfo("Successful", "Desktop background set successfully.")
        else:
            messagebox.showerror("Failed to download APOD image.")

    def load_titles(self):
        ttl = apod_desktop.get_all_apod_titles()
        self.titles_listbox.delete(0, tk.END)
        for title in ttl:
            self.titles_listbox.insert(tk.END, title)

def main():
    root = tk.Tk()
    app = AstronomyDesktopApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()