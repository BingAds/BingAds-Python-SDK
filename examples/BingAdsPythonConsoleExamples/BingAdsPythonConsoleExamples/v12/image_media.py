import base64

from auth_helper import *
from campaignmanagement_example_helper import *

# You must provide credentials in auth_helper.py.

# To run this example you'll need access to image media files 
# for responsive ads and image ad extensions.

MEDIA_FILE_PATH = "c:\dev\media\\"

# For required aspect ratios and recommended dimensions please see 
# Image remarks at https://go.microsoft.com/fwlink/?linkid=872754.

LANDSCAPE_IMAGE_MEDIA_FILE_NAME = "imageresponsivead1200x628.png"
LANDSCAPE_LOGO_MEDIA_FILE_NAME = "imageresponsivead1200x300.png"
SQUARE_IMAGE_MEDIA_FILE_NAME = "imageresponsivead1200x1200.png"
SQUARE_LOGO_MEDIA_FILE_NAME = "imageresponsivead1100x1100.png"
IMAGE_AD_EXTENSION_MEDIA_FILE_NAME = "imageadextension300x200.png"
       
def main(authorization_data):    
    try:
        landscape_image_media = get_image_media(
            "Image191x100",
            MEDIA_FILE_PATH + LANDSCAPE_IMAGE_MEDIA_FILE_NAME)

        landscape_logo_media = get_image_media(
            "Image4x1",
            MEDIA_FILE_PATH + LANDSCAPE_LOGO_MEDIA_FILE_NAME)

        square_image_media = get_image_media(
            "Image1x1",
            MEDIA_FILE_PATH + SQUARE_IMAGE_MEDIA_FILE_NAME)

        square_logo_media = get_image_media(
            "Image1x1",
            MEDIA_FILE_PATH + SQUARE_LOGO_MEDIA_FILE_NAME)

        image_ad_extension_media = get_image_media(
            "Image15x10",
            MEDIA_FILE_PATH + IMAGE_AD_EXTENSION_MEDIA_FILE_NAME)

        add_media = { 
            'Media': 
            [
                landscape_image_media,
                landscape_logo_media,
                square_image_media,
                square_logo_media,
                image_ad_extension_media
            ]
        }
        output_array_of_media(add_media)

        image_media_ids = campaign_service.AddMedia(
            authorization_data.account_id,
            add_media)

        # The index of returned IDs is consistent with the order you submitted them in the request;
        # however, the sequence of the IDs themselves is not guaranteed. For example you might observe:
        # - Landscape Image Media Id == image_media_ids['long'][0] == 1
        # - Landscape Logo Media Id == image_media_ids['long'][1] == 4
        # - Square Image Media Id == image_media_ids['long'][2] == 3
        # - Square Logo Media Id == image_media_ids['long'][3] == 2
        # - Image Ad Extension Media Id == image_media_ids['long'][4] == 0

        # You can use the first four Media Ids when you add or update a Responsive Ad
        # in an Audience campaign e.g., see audience_campaigns.py. 

        ad_media_ids = {
            'long':
            [ image_media_ids['long'][0], image_media_ids['long'][1], image_media_ids['long'][2], image_media_ids['long'][3] ]
        } 
        output_status_message("Media Ids for Responsive Ad:\n")
        output_array_of_long(ad_media_ids)

        # You can use the fifth Media Id when you add or update an Image Ad Extension
        # in a Search campaign e.g., see ad_extensions.py.

        extension_media_ids = { 'long': [ image_media_ids['long'][4] ] }
        output_status_message("Media Ids for Image Ad Extension:\n")
        output_array_of_long(extension_media_ids)
        
        # Get the media representations to confirm the stored dimensions
        # and get the Url where you can later view or download the media.

        get_responsive_ad_mediametadata = campaign_service.GetMediaMetaDataByAccountId('ResponsiveAd')
        output_array_of_mediametadata(get_responsive_ad_mediametadata)

        get_image_ad_extension_mediametadata = campaign_service.GetMediaMetaDataByAccountId('ImageAdExtension')
        output_array_of_mediametadata(get_image_ad_extension_mediametadata)

        get_mediametadata = campaign_service.GetMediaMetaDataByIds(image_media_ids).MediaMetaData
        output_array_of_mediametadata(get_mediametadata)
        
        # Comment out (disable) the delete operation if you want to use the media IDs  
        # in another example e.g., audience_campaigns.py.

        delete_media_response = campaign_service.DeleteMedia(
            authorization_data.account_id,
            image_media_ids)

        for id in image_media_ids['long']:
            output_status_message("Deleted Media Id {0}\n".format(id))

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

    print("Python loads the web service proxies at runtime, so you will observe " \
          "a performance delay between program launch and main execution...\n")
    
    authorization_data=AuthorizationData(
        account_id=None,
        customer_id=None,
        developer_token=DEVELOPER_TOKEN,
        authentication=None,
    )

    campaign_service=ServiceClient(
        service='CampaignManagementService', 
        version=12,
        authorization_data=authorization_data, 
        environment=ENVIRONMENT,
    )

    # You should authenticate for Bing Ads production services with a Microsoft Account.
        
    authenticate(authorization_data)
        
    main(authorization_data)
