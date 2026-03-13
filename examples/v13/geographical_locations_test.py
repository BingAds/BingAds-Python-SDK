import os
from datetime import datetime, timezone
from auth_helper import *
from openapi_client.models.campaign import *
import requests


# File paths for downloading geographical locations file
LOCAL_FILE = os.path.join(os.path.expanduser("~"), "Downloads", "geolocations.csv")
VERSION = "2.0"
LANGUAGE_LOCALE = "en"


def download_file(url, file_path):
    """
    Download a file from the given URL to the specified file path.
    
    Args:
        url: The URL to download from
        file_path: The local path to save the file
    """
    print(f"Downloading the file locally: {file_path}")
    
    response = requests.get(url, stream=True)
    
    if response.status_code == 200:
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded the file to {file_path}")
    else:
        print(f"The file was not successfully downloaded. HTTP Code {response.status_code}")
        raise Exception(f"Download failed with status code {response.status_code}")


def main(authorization_data):
    try:
        # Get the geographical locations file URL
        print("Getting geographical locations file URL...")
        
        get_geo_locations_request = GetGeoLocationsFileUrlRequest(
            version=VERSION,
            language_locale=LANGUAGE_LOCALE
        )
        
        get_geo_locations_response = campaign_service.get_geo_locations_file_url(
            get_geo_locations_file_url_request=get_geo_locations_request
        )
        
        file_url = get_geo_locations_response.FileUrl
        file_url_expiry_time_utc = get_geo_locations_response.FileUrlExpiryTimeUtc
        last_modified_time_utc = get_geo_locations_response.LastModifiedTimeUtc
        
        print(f"FileUrl: {file_url}")
        print(f"FileUrlExpiryTimeUtc: {file_url_expiry_time_utc}")
        print(f"LastModifiedTimeUtc: {last_modified_time_utc}")
        
        # Download the geographical locations file
        print("\nDownloading geographical locations file...")
        
        # Set a previous sync time for comparison
        # You can modify this to your actual previous sync time
        previous_sync_time_utc = datetime(2017, 8, 10, 0, 0, 0, tzinfo=timezone.utc)
        
        # Parse the last modified time
        if isinstance(last_modified_time_utc, str):
            last_modified_datetime = datetime.fromisoformat(last_modified_time_utc.replace('Z', '+00:00'))
        else:
            last_modified_datetime = last_modified_time_utc
        
        # Ensure both datetimes are timezone-aware for comparison
        if last_modified_datetime.tzinfo is None:
            last_modified_datetime = last_modified_datetime.replace(tzinfo=timezone.utc)
        
        # Only download if the file has been modified since the previous sync
        if last_modified_datetime > previous_sync_time_utc:
            download_file(file_url, LOCAL_FILE)
            print(f"\nSuccessfully downloaded geographical locations file to {LOCAL_FILE}")
        else:
            print(f"\nThe file has not been modified since your previous sync time ({previous_sync_time_utc.isoformat()})")
        
    except Exception as ex:
        print(f"Error occurred: {str(ex)}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    print("Loading the web service client...")
    
    authorization_data = AuthorizationData(
        account_id=None,
        customer_id=None,
        developer_token=DEVELOPER_TOKEN,
        authentication=None,
    )
    
    authenticate(authorization_data)
    
    campaign_service = ServiceClient(
        service='CampaignManagementService',
        version=13,
        authorization_data=authorization_data,
        environment=ENVIRONMENT,
    )
    
    main(authorization_data)