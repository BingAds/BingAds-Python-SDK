import os
import base64
from auth_helper import *
from openapi_client.models.campaign import *

# Media file paths - update with your own images
MEDIA_FILE_PATH = "c:\\dev\\media\\"
RESPONSIVE_AD_MEDIA_FILE_NAME = "imageresponsivead703x368.png"
IMAGE_AD_EXTENSION_MEDIA_FILE_NAME = "imageadextension300x200.png"

def get_base64_image_data(image_file_path):
    """
    Read an image file and return its base64 encoded data.
    
    Args:
        image_file_path: Path to the image file
        
    Returns:
        Base64 encoded string of the image data
    """
    with open(image_file_path, 'rb') as image_file:
        image_data = image_file.read()
        return base64.b64encode(image_data).decode('utf-8')

def get_image_media(media_type, image_file_name):
    """
    Create an Image media object with the specified type and file.
    
    Args:
        media_type: The media type (e.g., "Image191x100", "Image15x10")
        image_file_name: Path to the image file
        
    Returns:
        Image object ready to be added to the account
    """
    image = Image(
        data=get_base64_image_data(image_file_name),
        media_type=media_type,
        type="Image"
    )
    return image

def main(authorization_data):
    try:
        # Prepare the image media objects
        print("Preparing image media...")
        
        responsive_ad_image_path = os.path.join(MEDIA_FILE_PATH, RESPONSIVE_AD_MEDIA_FILE_NAME)
        image_ad_extension_path = os.path.join(MEDIA_FILE_PATH, IMAGE_AD_EXTENSION_MEDIA_FILE_NAME)
        
        # Check if files exist
        if not os.path.exists(responsive_ad_image_path):
            print(f"Warning: File not found: {responsive_ad_image_path}")
            print("Please update MEDIA_FILE_PATH and file names with your actual image files.")
            return
        
        if not os.path.exists(image_ad_extension_path):
            print(f"Warning: File not found: {image_ad_extension_path}")
            print("Please update MEDIA_FILE_PATH and file names with your actual image files.")
            return
        
        responsive_ad_image_media = get_image_media(
            "Image191x100",
            responsive_ad_image_path
        )
        
        image_ad_extension_media = get_image_media(
            "Image15x10",
            image_ad_extension_path
        )
        
        add_media = [responsive_ad_image_media, image_ad_extension_media]
        
        # Add media to the account
        print("\nAdding media to account...")
        
        add_media_request = AddMediaRequest(
            account_id=authorization_data.account_id,
            media=add_media
        )
        
        add_media_response = campaign_service.add_media(
            add_media_request=add_media_request
        )
        
        media_ids = add_media_response.MediaIds
        print(f"Added Media IDs: {media_ids}")
        
        # Get media metadata
        print("\nGetting media metadata...")
        
        get_metadata_request = GetMediaMetaDataByIdsRequest(
            media_ids=media_ids
        )
        
        get_metadata_response = campaign_service.get_media_meta_data_by_ids(
            get_media_meta_data_by_ids_request=get_metadata_request
        )
        
        media_meta_data = get_metadata_response.MediaMetaData
        print(f"Media Metadata:")
        for metadata in media_meta_data:
            if metadata:
                print(f"  Media ID: {metadata.Id}")
                print(f"  Media Type: {metadata.MediaType}")
                if hasattr(metadata, 'Dimensions') and metadata.Dimensions:
                    print(f"  Dimensions: {metadata.Dimensions}")
                if hasattr(metadata, 'Urls') and metadata.Urls:
                    print(f"  URLs: {metadata.Urls}")
        
        if get_metadata_response.PartialErrors:
            print(f"Partial Errors: {get_metadata_response.PartialErrors}")
        
        # Delete the media
        print("\nDeleting media...")
        
        delete_media_request = DeleteMediaRequest(
            account_id=authorization_data.account_id,
            media_ids=media_ids
        )
        
        delete_media_response = campaign_service.delete_media(
            delete_media_request=delete_media_request
        )
        
        if delete_media_response.PartialErrors:
            print(f"Partial Errors: {delete_media_response.PartialErrors}")
        else:
            print(f"Deleted Media IDs: {media_ids}")
        
    except FileNotFoundError as ex:
        print(f"File not found: {str(ex)}")
        print("Please update MEDIA_FILE_PATH and file names with your actual image files.")
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