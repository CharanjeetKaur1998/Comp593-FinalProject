'''
Library for interacting with NASA's Astronomy Picture of the Day API.
'''
import requests

def main():
    # TODO: Add code to test the functions in this module
    apod_info_dict = get_apod_info('2024-08-09')
    print(apod_info_dict)
    #print(get_apod_image_url(apod_info_dict))
    return

def get_apod_info(apod_date):
    """Gets information from the NASA API for the Astronomy 
    Picture of the Day (APOD) from a specified date.

    Args:
        apod_date (date): APOD date (Can also be a string formatted as YYYY-MM-DD)

    Returns:
        dict: Dictionary of APOD info, if successful. None if unsuccessful
    """
    # TODO: Complete the function body
    # Hint: The APOD API uses query string parameters: https://requests.readthedocs.io/en/latest/user/quickstart/#passing-parameters-in-urls
    # Hint: Set the 'thumbs' parameter to True so the info returned for video APODs will include URL of the video thumbnail image 
    payload = {'api_key':'uZv1QMecDUR1qduWdXLEgAgRQdIhCHRjqXs7xuHQ','date':apod_date,'thumbs':True}
    resp_msg = requests.get('https://api.nasa.gov/planetary/apod',params=payload)
    info_json=resp_msg.json()
    return info_json

def get_apod_image_url(apod_info_dict):
    """Gets the URL of the APOD image from the dictionary of APOD information.

    If the APOD is an image, gets the URL of the high definition image.
    If the APOD is a video, gets the URL of the video thumbnail.

    Args:
        apod_info_dict (dict): Dictionary of APOD info from API

    Returns:
        str: APOD image URL
    """
    # Extract media type from APOD info dictionary
    media_type = apod_info_dict.get("media_type")
    if media_type == "image":
        return apod_info_dict.get("hdurl")
    elif media_type == "video":
        return apod_info_dict.get("url")
    else:
        print("Error: Unknown media type.")
        return None

if __name__ == '__main__':
    main()