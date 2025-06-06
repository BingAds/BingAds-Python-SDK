import base64
import uuid

from auth_helper_rest import *
from openapi_client.models.campaign import *


def main(authorization_data):
    try:
        ad_final_url = "https://contoso.com"
        final_urls = [ad_final_url]
        create_responsive_ad_recommendation_request = CreateResponsiveAdRecommendationRequest(
            final_urls=final_urls
        )

        responsive_ad_recommendation_response = campaign_service.create_responsive_ad_recommendation(
            create_responsive_ad_recommendation_request=create_responsive_ad_recommendation_request
        )

        responsive_ad = responsive_ad_recommendation_response.ResponsiveAd
        image_suggestions = responsive_ad_recommendation_response.ImageSuggestions

        # Select a few images from the suggested list. This example picks first 5 images
        selected_images = image_suggestions[:5]

        # Add selected images to your media library
        save_images(selected_images)

        images = [obj.AssetLink for obj in selected_images]
        responsive_ad.Images = images
        responsive_ad.BusinessName = "Contoso"
        responsive_ad.CallToActionLanguage = LanguageName.ENGLISH

        # Create an Audience campaign with one ad group and a responsive ad
        campaign = Campaign()
        campaign.BudgetType = BudgetLimitType.DAILYBUDGETACCELERATED
        # CampaignType must be set for Audience campaigns
        campaign.CampaignType = CampaignType.AUDIENCE
        campaign.DailyBudget = 50.00
        campaign.Languages = ['All']
        campaign.Name = "Ad recommendation test " + str(uuid.uuid4())
        campaign.TimeZone = 'PacificTimeUSCanadaTijuana'
        campaigns = [campaign]

        add_campaigns_request = AddCampaignsRequest(
            account_id=authorization_data.account_id,
            campaigns=campaigns,
        )

        add_campaigns_response = campaign_service.add_campaigns(
            add_campaigns_request=add_campaigns_request
        )
        campaign_ids = add_campaigns_response.CampaignIds

        # Add an ad group within the campaign.
        ad_group = AdGroup()
        ad_group.Name = "Holiday Sale"
        ad_group.StartDate = None
        end_date = ModelDate()
        end_date.Day = 31
        end_date.Month = 12
        current_time = gmtime()
        end_date.Year = current_time.tm_year
        ad_group.EndDate = end_date
        cpc_bid = Bid()
        cpc_bid.Amount = 0.09
        ad_group.CpcBid = cpc_bid
        # Network cannot be set for ad groups in Audience campaigns
        ad_group.Network = None
        ad_groups = [ad_group]

        add_ad_groups_request = AddAdGroupsRequest(
            campaign_id=campaign_ids[0],
            ad_groups=ad_groups
        )

        add_ad_groups_response = campaign_service.add_ad_groups(
            add_ad_groups_request=add_ad_groups_request
        )
        ad_group_ids = add_ad_groups_response.AdGroupIds

        # Add a responsive ad within the ad group
        ad = Ad(responsive_ad)
        ads = [ad]
        add_ads_request = AddAdsRequest(
            ad_group_id=ad_group_ids[0],
            ads=ads
        )

        add_ads_response = campaign_service.add_ads(
            add_ads_request=add_ads_request
        )
        ad_ids = add_ads_response.AdIds

        # Clean up
        media_ids = [obj.Asset.Id for obj in responsive_ad.Images]
        delete_media_request = DeleteMediaRequest(
            account_id=authorization_data.account_id,
            media_ids=media_ids
        )

        campaign_service.delete_media(
            delete_media_request=delete_media_request
        )

        delete_campaigns_request = DeleteCampaignsRequest(
            account_id=authorization_data.account_id,
            campaign_ids=campaign_ids
        )

        campaign_service.delete_campaigns(
            delete_campaigns_request=delete_campaigns_request
        )

    except Exception as ex:
        print(f"Error occurred: {str(ex)}")


def download_bytes(url):
    """Download bytes from a URL using streaming."""
    response = requests.get(url, stream=True)
    response.raise_for_status()

    output_stream = bytearray()
    for chunk in response.iter_content(chunk_size=4096):
        if chunk:
            output_stream.extend(chunk)
    return bytes(output_stream)


def save_images(image_suggestions):
    """Save image suggestions to the media library."""
    medias_to_add = []
    for item in image_suggestions:
        image = item.Image
        image_bytes = download_bytes(item.ImageUrl)
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        image.Data = image_base64
        media = Media(image)
        medias_to_add.append(media)

    add_media_request = AddMediaRequest(
        account_id=authorization_data.account_id,
        media=medias_to_add
    )

    add_media_response = campaign_service.add_media(
        add_media_request=add_media_request
    )
    media_ids = add_media_response.media_ids

    for i in range(len(media_ids)):
        image_suggestions[i].AssetLink.Asset.id = str(media_ids[i])

    return image_suggestions


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
