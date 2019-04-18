import base64

from auth_helper import *
from campaignmanagement_example_helper import *

# You must provide credentials in auth_helper.py.

# To run this example you'll need to provide your own images.  
# For required aspect ratios and recommended dimensions please see 
# Image remarks at https://go.microsoft.com/fwlink/?linkid=872754.

MEDIA_FILE_PATH = "c:\dev\media\\"
RESPONSIVE_AD_MEDIA_FILE_NAME = "imageresponsivead1200x628.png"
IMAGE_AD_EXTENSION_MEDIA_FILE_NAME = "imageadextension300x200.png"
       
def main(authorization_data):    
    try:
        responsive_ad_image_media = get_image_media(
            "Image191x100",
            MEDIA_FILE_PATH + RESPONSIVE_AD_MEDIA_FILE_NAME)

        image_ad_extension_media = get_image_media(
            "Image15x10",
            MEDIA_FILE_PATH + IMAGE_AD_EXTENSION_MEDIA_FILE_NAME)

        add_media = { 
            'Media': 
            [
                responsive_ad_image_media,
                image_ad_extension_media
            ]
        }
        output_status_message("Ready to upload image media:")
        output_array_of_media(add_media)

        output_status_message("-----\nAddMedia:")
        media_ids = campaign_service.AddMedia(
            AccountId=authorization_data.account_id,
            Media=add_media)
        output_status_message("MediaIds:")
        output_array_of_long(media_ids)
        
        # Get the media representations to confirm the stored dimensions
        # and get the Url where you can later view or download the media.

        output_status_message("-----\nGetMediaMetaDataByAccountId:")
        get_responsive_ad_mediametadata = campaign_service.GetMediaMetaDataByAccountId(
            MediaEnabledEntities='ResponsiveAd',
            PageInfo=None)
        output_status_message("MediaMetaData:")
        output_array_of_mediametadata(get_responsive_ad_mediametadata)

        output_status_message("-----\nGetMediaMetaDataByAccountId:")
        get_image_ad_extension_mediametadata = campaign_service.GetMediaMetaDataByAccountId(
            MediaEnabledEntities='ImageAdExtension',
            PageInfo=None)
        output_status_message("MediaMetaData:")
        output_array_of_mediametadata(get_image_ad_extension_mediametadata)

        output_status_message("-----\nGetMediaMetaDataByIds:")
        get_mediametadata = campaign_service.GetMediaMetaDataByIds(
            MediaIds=media_ids).MediaMetaData
        output_status_message("MediaMetaData:")
        output_array_of_mediametadata(get_mediametadata)
        
        # Delete the account's media.

        output_status_message("-----\nDeleteMedia:")
        delete_media_response = campaign_service.DeleteMedia(
            authorization_data.account_id,
            media_ids)

        for id in media_ids['long']:
            output_status_message("Deleted Media Id {0}".format(id))

    except WebFault as ex:
        output_webfault_errors(ex)
    except Exception as ex:
        output_status_message(ex)

def get_image_media(
    media_type, 
    image_file_name):
    image = campaign_service.factory.create('Image')
    image.Data = get_bmp_base64_string(image_file_name)
    image.MediaType = media_type
    image.Type = "Image"

    return image

def get_bmp_base64_string(image_file_name):
    image = open(image_file_name, 'rb') 
    image_bytes = image.read() 
    base64_string = base64.encodestring(image_bytes)
    return base64_string

# Main execution
if __name__ == '__main__':

    print("Loading the web service client proxies...")
    
    authorization_data=AuthorizationData(
        account_id=None,
        customer_id=None,
        developer_token=DEVELOPER_TOKEN,
        authentication=None,
    )

    campaign_service=ServiceClient(
        service='CampaignManagementService', 
        version=13,
        authorization_data=authorization_data, 
        environment=ENVIRONMENT,
    )
        
    authenticate(authorization_data)
        
    main(authorization_data)
