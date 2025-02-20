import base64

from auth_helper import *
from campaignmanagement_example_helper import *

# You must provide credentials in auth_helper.py.

def main(authorization_data):

    try:
        # To run this example you'll need to provide a valid Ad Final URL
        ad_final_url = "https://contoso.com"
        # Set false to disable cleanup of created entities at the end
        do_cleanup = True

        final_urls = campaign_service.factory.create('ns3:ArrayOfstring')
        final_urls.string.append(ad_final_url)

        output_status_message("-----\nCreateResponsiveAdRecommendation:");
        output_status_message(f"-----\nGetting ad recommendation for URL {ad_final_url} ...");
        responsive_ad_recommendation_response = campaign_service.CreateResponsiveAdRecommendation(
            FinalUrls=final_urls
        )
        responsive_ad = responsive_ad_recommendation_response.ResponsiveAd
        image_suggestions = responsive_ad_recommendation_response.ImageSuggestions['AdRecommendationImageSuggestion']

        # Select a few images from the suggested list. This example picks first 5 images
        selected_images = image_suggestions[:5]

        # Add selected images to your media library
        save_images(selected_images)

        images = campaign_service.factory.create('ArrayOfAssetLink')
        images.AssetLink = [obj.AssetLink for obj in selected_images]
        responsive_ad.Images = images

        responsive_ad.BusinessName = "Contoso"
        #responsive_ad.CallToAction = 'ShopNow'
        responsive_ad.CallToActionLanguage = 'English'

        # Create an Audience campaign with one ad group and a responsive ad
        campaigns = campaign_service.factory.create('ArrayOfCampaign')
        campaign = set_elements_to_none(campaign_service.factory.create('Campaign'))
        campaign.BudgetType = 'DailyBudgetStandard'
        # CampaignType must be set for Audience campaigns
        campaign.CampaignType = ['Audience']
        campaign.DailyBudget = 50.00
        languages = campaign_service.factory.create('ns3:ArrayOfstring')
        languages.string.append('All')
        campaign.Languages = languages
        campaign.Name = "Ad recommendation test " + str(datetime.now())
        campaign.TimeZone = 'PacificTimeUSCanadaTijuana'
        campaigns.Campaign.append(campaign)

        output_status_message("-----\nAddCampaigns:")
        add_campaigns_response = campaign_service.AddCampaigns(
            AccountId=authorization_data.account_id,
            Campaigns=campaigns
        )
        campaign_ids = {
            'long': add_campaigns_response.CampaignIds['long'] if add_campaigns_response.CampaignIds['long'] else None
        }
        output_status_message("CampaignIds:")
        output_array_of_long(campaign_ids)
        output_status_message("PartialErrors:")
        output_array_of_batcherror(add_campaigns_response.PartialErrors)

        # Add an ad group within the campaign.
        ad_groups = campaign_service.factory.create('ArrayOfAdGroup')
        ad_group = set_elements_to_none(campaign_service.factory.create('AdGroup'))
        ad_group.Name = "Holiday Sale"
        ad_group.StartDate = None
        end_date = campaign_service.factory.create('Date')
        end_date.Day = 31
        end_date.Month = 12
        current_time = gmtime()
        end_date.Year = current_time.tm_year
        ad_group.EndDate = end_date
        cpc_bid = campaign_service.factory.create('Bid')
        cpc_bid.Amount = 0.09
        ad_group.CpcBid = cpc_bid
        # Network cannot be set for ad groups in Audience campaigns
        ad_group.Network = None
        ad_groups.AdGroup.append(ad_group)

        output_status_message("-----\nAddAdGroups:")
        add_ad_groups_response = campaign_service.AddAdGroups(
            CampaignId=campaign_ids['long'][0],
            AdGroups=ad_groups,
            ReturnInheritedBidStrategyTypes=False
        )
        ad_group_ids = {
            'long': add_ad_groups_response.AdGroupIds['long'] if add_ad_groups_response.AdGroupIds['long'] else None
        }
        output_status_message("AdGroupIds:")
        output_array_of_long(ad_group_ids)
        output_status_message("PartialErrors:")
        output_array_of_batcherror(add_ad_groups_response.PartialErrors)

        # Add a responsive ad within the ad group
        ads = campaign_service.factory.create('ArrayOfAd')
        ads.Ad.append(responsive_ad)

        output_status_message("-----\nAddAds:")
        add_ads_response = campaign_service.AddAds(
            AdGroupId=ad_group_ids['long'][0],
            Ads=ads
        )
        ad_ids = {
            'long': add_ads_response.AdIds['long'] if add_ads_response.AdIds['long'] else None
        }
        output_status_message("AdIds:")
        output_array_of_long(ad_ids)
        output_status_message("PartialErrors:")
        output_array_of_batcherror(add_ads_response.PartialErrors)

        output_status_message(f"-----\nCreated campaign: + {campaign.Name}")

        if not do_cleanup:
            return
        else:
            # Delete the account's media
            output_status_message("-----\nDeleteMedia:")
            media_ids = campaign_service.factory.create('ns3:ArrayOflong')
            media_ids['long'] = [obj.Asset.Id for obj in responsive_ad.Images.AssetLink]
            delete_media_response = campaign_service.DeleteMedia(
                AccountId=authorization_data.account_id,
                MediaIds=media_ids
            )

            for media_id in media_ids['long']:
                output_status_message("Deleted Media Id {0}".format(media_id))

            # Delete the campaign and everything it contains e.g., ad groups and ads
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

def save_images(image_suggestions):
    medias_to_add = campaign_service.factory.create('ArrayOfMedia')
    for item in image_suggestions:
        image = item.Image
        image_bytes = download_bytes(item.ImageUrl)
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        image.Data = image_base64
        medias_to_add.Media.append(image)

    media_ids = campaign_service.AddMedia(
        AccountId=authorization_data.account_id,
        Media=medias_to_add
    )

    for i in range(len(media_ids['long'])):
        image_suggestions[i].AssetLink.Asset.Id = media_ids['long'][i]

def download_bytes(url):
    response = requests.get(url, stream=True)
    response.raise_for_status()

    output_stream = bytearray()

    for chunk in response.iter_content(chunk_size=4096):
        if chunk:
            output_stream.extend(chunk)

    return bytes(output_stream)

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
