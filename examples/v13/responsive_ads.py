import base64

from auth_helper import *
from campaignmanagement_example_helper import *

# You must provide credentials in auth_helper.py.

# To run this example you'll need to provide your own image.  
# For required aspect ratios and recommended dimensions please see 
# Image remarks at https://go.microsoft.com/fwlink/?linkid=872754.

MEDIA_FILE_PATH="c:\dev\media\\"
RESPONSIVE_AD_MEDIA_FILE_NAME="imageresponsivead1200x628.png"

def main(authorization_data):

    try:
        # Add an image to your media library. 
        # The image asset is needed later to create the responsive ad.

        responsive_ad_image_media=get_image_media(
            "Image191x100",
            MEDIA_FILE_PATH + RESPONSIVE_AD_MEDIA_FILE_NAME)

        add_media={ 
            'Media': 
            [
                responsive_ad_image_media
            ]
        }

        output_status_message("-----\nAddMedia:")
        media_ids=campaign_service.AddMedia(
            AccountId=authorization_data.account_id,
            Media=add_media)
        output_status_message("MediaIds:")
        output_array_of_long(media_ids)

        # Create an Audience campaign with one ad group and a responsive ad.

        campaigns=campaign_service.factory.create('ArrayOfCampaign')
        campaign=set_elements_to_none(campaign_service.factory.create('Campaign'))
        # CampaignType must be set for Audience campaigns
        campaign.CampaignType=['Audience']
        # Languages must be set for Audience campaigns
        languages=campaign_service.factory.create('ns3:ArrayOfstring')
        languages.string.append('All')
        campaign.Languages=languages
        campaign.Name="Women's Shoes " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        campaign.DailyBudget=50
        campaign.BudgetType='DailyBudgetStandard'
        campaign.TimeZone='PacificTimeUSCanadaTijuana'
        campaigns.Campaign.append(campaign)

        output_status_message("-----\nAddCampaigns:")
        add_campaigns_response=campaign_service.AddCampaigns(
            AccountId=authorization_data.account_id,
            Campaigns=campaigns
        )
        campaign_ids={
            'long': add_campaigns_response.CampaignIds['long'] if add_campaigns_response.CampaignIds['long'] else None
        }
        output_status_message("CampaignIds:")
        output_array_of_long(campaign_ids)
        output_status_message("PartialErrors:")
        output_array_of_batcherror(add_campaigns_response.PartialErrors)

        # Add an ad group within the campaign.

        ad_groups=campaign_service.factory.create('ArrayOfAdGroup')
        ad_group=set_elements_to_none(campaign_service.factory.create('AdGroup'))
        ad_group.Name="Women's Red Shoe Sale"
        end_date=campaign_service.factory.create('Date')
        end_date.Day=31
        end_date.Month=12
        current_time=gmtime()
        end_date.Year=current_time.tm_year + 1
        ad_group.EndDate=end_date
        cpc_bid=campaign_service.factory.create('Bid')
        cpc_bid.Amount=0.09
        ad_group.CpcBid=cpc_bid
        # Network cannot be set for ad groups in Audience campaigns
        ad_group.Network=None
        ad_groups.AdGroup.append(ad_group)

        output_status_message("-----\nAddAdGroups:")
        add_ad_groups_response=campaign_service.AddAdGroups(
            CampaignId=campaign_ids['long'][0],
            AdGroups=ad_groups,
            ReturnInheritedBidStrategyTypes=False
        )
        ad_group_ids={
            'long': add_ad_groups_response.AdGroupIds['long'] if add_ad_groups_response.AdGroupIds['long'] else None
        }
        output_status_message("AdGroupIds:")
        output_array_of_long(ad_group_ids)
        output_status_message("PartialErrors:")
        output_array_of_batcherror(add_ad_groups_response.PartialErrors)

        # Add a responsive ad within the ad group.        

        ads=campaign_service.factory.create('ArrayOfAd')
        responsive_ad=set_elements_to_none(campaign_service.factory.create('ResponsiveAd'))
        responsive_ad.BusinessName="Contoso"
        responsive_ad.CallToAction='AddToCart'
        final_urls=campaign_service.factory.create('ns3:ArrayOfstring')
        final_urls.string.append('https://www.contoso.com/womenshoesale')
        responsive_ad.FinalUrls=final_urls
        responsive_ad.Headline="Fast & Easy Setup"
        # You are only required to provide a landscape image asset. 
        # Optionally you can include additional asset links, i.e., one image asset for each supported sub type. 
        # For any image asset sub types that you do not explicitly set, 
        # the service will automatically create image asset links by cropping the LandscapeImageMedia.
        images=campaign_service.factory.create('ArrayOfAssetLink')
        landscape_image_media_asset_link=set_elements_to_none(campaign_service.factory.create('AssetLink'))
        landscape_image_media_asset=set_elements_to_none(campaign_service.factory.create('ImageAsset'))
        landscape_image_media_asset.CropHeight=None
        landscape_image_media_asset.CropWidth=None
        landscape_image_media_asset.CropX=None
        landscape_image_media_asset.CropY=None
        landscape_image_media_asset.Id=media_ids['long'][0]
        landscape_image_media_asset.Name="My LandscapeImageMedia"
        landscape_image_media_asset.SubType="LandscapeImageMedia"
        landscape_image_media_asset_link.Asset=landscape_image_media_asset
        images.AssetLink.append(landscape_image_media_asset_link)
        responsive_ad.Images=images
        responsive_ad.LongHeadline="Find New Customers & Increase Sales!"
        responsive_ad.Text="Find New Customers & Increase Sales! Start Advertising on Contoso Today."
        responsive_ad.Type='ResponsiveAd'
        ads.Ad.append(responsive_ad)
        
        output_status_message("-----\nAddAds:")
        add_ads_response=campaign_service.AddAds(
            AdGroupId=ad_group_ids['long'][0],
            Ads=ads
        )
        ad_ids={
            'long': add_ads_response.AdIds['long'] if add_ads_response.AdIds['long'] else None
        }
        output_status_message("AdIds:")
        output_array_of_long(ad_ids)
        output_status_message("PartialErrors:")
        output_array_of_batcherror(add_ads_response.PartialErrors)

        # Delete the account's media.

        output_status_message("-----\nDeleteMedia:")
        delete_media_response=campaign_service.DeleteMedia(
            authorization_data.account_id,
            media_ids)

        for id in media_ids['long']:
            output_status_message("Deleted Media Id {0}".format(id))
        
        # Delete the campaign and everything it contains e.g., ad groups and ads.

        output_status_message("-----\nDeleteCampaigns:")
        campaign_service.DeleteCampaigns(
            AccountId=authorization_data.account_id,
            CampaignIds=campaign_ids
        )
        output_status_message("Deleted Campaign Id {0}".format(campaign_ids['long'][0]))

    except WebFault as ex:
        output_webfault_errors(ex)
    except Exception as ex:
        output_status_message(ex)

def get_image_media(
    media_type, 
    image_file_name):
    image=campaign_service.factory.create('Image')
    image.Data=get_bmp_base64_string(image_file_name)
    image.MediaType=media_type
    image.Type="Image"

    return image

def get_bmp_base64_string(image_file_name):
    image=open(image_file_name, 'rb') 
    image_bytes=image.read() 
    base64_string=base64.encodestring(image_bytes)
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
