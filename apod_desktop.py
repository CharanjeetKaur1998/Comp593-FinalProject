import hashlib
import sys
from datetime import date
import image_lib
import apod_api
import os 
import sqlite3
""" 
COMP 593 - Final Project

Description: 
  Downloads NASA's Astronomy Picture of the Day (APOD) from a specified date
  and sets it as the desktop background image.

Usage:
  python apod_desktop.py [apod_date]

Parameters:
  apod_date = APOD date (format: YYYY-MM-DD)
"""

# Full paths of the image cache folder and database
# - The image cache directory is a subdirectory of the specified parent directory.
# - The image cache database is a sqlite database located in the image cache directory.
script_dir = os.path.dirname(os.path.abspath(__file__))
image_cache_dir = os.path.join(script_dir, 'images')
image_cache_db = os.path.join(image_cache_dir, 'image_cache.db')

 ## DO NOT CHANGE THIS FUNCTION ##
  # Get the APOD date from the command line
def main(apod_date=None): 
    if apod_date is None:
        apod_date = date.today()

    # Initialize the image cache
    init_apod_cache()

    # Add the APOD for the specified date to the cache
    apod_id = add_apod_to_cache(apod_date)

    # Get the information for the APOD from the DB
    apod_info = get_apod_info(apod_id)
   
    # Set the APOD as the desktop background image
    if apod_id != 0:
        image_lib.set_desktop_background(apod_info['file_path'])


def get_apod_date():
    """Gets the APOD date
     
    The APOD date is taken from the first command line parameter.
    Validates that the command line parameter specifies a valid APOD date.
    Prints an error message and exits script if the date is invalid.
    Uses today's date if no date is provided on the command line.

    Returns:
        date: APOD date
    """
    # TODO: Complete function body
    # Hint: The following line of code shows how to convert and ISO-formatted date string to a date object

    apod_date = date.today()
    if len(sys.argv) > 1 and sys.argv[1].count('-') == 2 and len(sys.argv[1]) == 10:
        apod_date = date.fromisoformat(sys.argv[1])
    else:
        print("this is Invalid date format. Follow this format YYYY-MM-DD.")
        sys.exit(1)

    return apod_date

def init_apod_cache():
    """Initializes the image cache by:
    - Creating the image cache directory if it does not already exist,
    - Creating the image cache database if it does not already exist.
    """
    # TODO: Create the image cache directory if it does not already exist
    # TODO: Create the DB if it does not already exist

    if not os.path.exists(image_cache_dir):
        os.mkdir(image_cache_dir)
        print(f"cache directory has been created successfully: {image_cache_dir}")

    if not os.path.exists(image_cache_db):
        print(f"cache database has been successfully created: {image_cache_db}")
        create_db()

def create_db():
    conn = sqlite3.connect(image_cache_db)
    c = conn.cursor()
    c.execute('''CREATE TABLE apod_images
                 (id INTEGER PRIMARY KEY,
                 title TEXT,
                 explanation TEXT,
                 file_path TEXT,
                 sha256 TEXT)''')
    conn.commit()
    conn.close()
    return

def add_apod_to_cache(apod_date):
    """Adds the APOD image from a specified date to the image cache.
     
    The APOD information and image file is downloaded from the NASA API.
    If the APOD is not already in the DB, the image file is saved to the 
    image cache and the APOD information is added to the image cache DB.

    Args:
        apod_date (date): Date of the APOD image

    Returns:
        int: Record ID of the APOD in the image cache DB, if a new APOD is added to the
        cache successfully or if the APOD already exists in the cache. Zero, if unsuccessful.
    """
    print("APOD date:", apod_date.isoformat())

    # TODO: Download the APOD information from the NASA API
    # Hint: Use a function from apod_api.py 
    apod_info = apod_api.get_apod_info(apod_date)

    # TODO: Download the APOD image
    # Hint: Use a function from image_lib.py 
    image_content = image_lib.download_image(apod_info['url'])
    sha256 = hashlib.sha256(image_content).hexdigest()

    # TODO: Check whether the APOD already exists in the image cache
    # Hint: Use the get_apod_id_from_db() function below
    existing_id = get_apod_id_from_db(sha256)
    
    # TODO: Save the APOD file to the image cache directory
    # Hint: Use the determine_apod_file_path() function below to determine the image file path
    # Hint: Use a function from image_lib.py to save the image file
    image_file_path = determine_apod_file_path(apod_info['title'], apod_info['url'])
    if not os.path.exists(image_file_path):
     image_lib.save_image_file(image_content, image_file_path)
      

    # TODO: Add the APOD information to the DB
    # Hint: Use the add_apod_to_db() function below
    if existing_id != 0:
        return existing_id
    add_apod_to_db(apod_info['title'], apod_info['explanation'], image_file_path, sha256)
    return 0

def add_apod_to_db(title, explanation, file_path, sha256):
    """Adds specified APOD information to the image cache DB.
     
    Args:
        title (str): Title of the APOD image
        explanation (str): Explanation of the APOD image
        file_path (str): Full path of the APOD image file
        sha256 (str): SHA-256 hash value of APOD image

    Returns:
        int: The ID of the newly inserted APOD record, if successful. Zero, if unsuccessful       
    """
    # TODO: Complete function body

    import sqlite3
    connection = sqlite3.connect(image_cache_db)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO apod_images (title, explanation, file_path, sha256) VALUES (?, ?, ?, ?)", 
              (title, 
               explanation, 
               file_path, 
               sha256
               )
            )
    connection.commit()
    connection.close()
    return 0

def get_apod_id_from_db(image_sha256):
    """Gets the record ID of the APOD in the cache having a specified SHA-256 hash value
    
    This function can be used to determine whether a specific image exists in the cache.

    Args:
        image_sha256 (str): SHA-256 hash value of APOD image

    Returns:
        int: Record ID of the APOD in the image cache DB, if it exists. Zero, if it does not.
    """
    # TODO: Complete function body

    import sqlite3
    connection = sqlite3.connect(image_cache_db)
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM apod_images WHERE sha256=?", (image_sha256,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return 0

def determine_apod_file_path(image_title, image_url):
    """Determines the path at which a newly downloaded APOD image must be 
    saved in the image cache. 
    
    The image file name is constructed as follows:
    - The file extension is taken from the image URL
    - The file name is taken from the image title, where:
        - Leading and trailing spaces are removed
        - Inner spaces are replaced with underscores
        - Characters other than letters, numbers, and underscores are removed

    For example, suppose:
    - The image cache directory path is 'C:\\temp\\APOD'
    - The image URL is 'https://apod.nasa.gov/apod/image/2205/NGC3521LRGBHaAPOD-20.jpg'
    - The image title is ' NGC #3521: Galaxy in a Bubble '

    The image path will be 'C:\\temp\\APOD\\NGC_3521_Galaxy_in_a_Bubble.jpg'

    Args:
        image_title (str): APOD title
        image_url (str): APOD image URL
    
    Returns:
        str: Full path at which the APOD image file must be saved in the image cache directory
    """
    # TODO: Complete function body
    # Hint: Use regex and/or str class methods to determine the filename.

    fil_extension = image_url.split('.')[-1]
    clean_title = '_'.join(char for char in image_title if char.isalnum() or char == ' ')
    file_path = os.path.join(image_cache_dir, f"{clean_title}.{fil_extension}")
    return file_path

def get_apod_info(image_id):
    """Gets the title, explanation, and full path of the APOD having a specified
    ID from the DB.

    Args:
        image_id (int): ID of APOD in the DB

    Returns:
        dict: Dictionary of APOD information
    """
    # TODO: Query DB for image info
    # TODO: Put information into a dictionary

    import sqlite3
    connection = sqlite3.connect(image_cache_db)
    cursor = connection.cursor()
    cursor.execute("SELECT title, explanation, file_path FROM apod_images WHERE id=?", (image_id,))
    result = cursor.fetchone()
    if result:
        apod_information = {
            'title': result[0],
            'explanation': result[1],
            'file_path': result[2]
        }
        return apod_information
    else:
        return None
    
def get_all_apod_titles():
    """Gets a list of the titles of all APODs in the image cache

    Returns:
        list: Titles of all images in the cache
    """
    # TODO: Complete function body
    # NOTE: This function is only needed to support the APOD viewer GUI
    import sqlite3
    connection = sqlite3.connect(image_cache_db)
    cursor = connection.cursor()
    cursor.execute("SELECT image_title FROM apod_images")
    results = cursor.fetchall()
    titles = [result[0] for result in results]
    connection.close()
    return titles  

if __name__ == '__main__':
    main()