from auth_helper import *
from campaignmanagement_example_helper import *

# You must provide credentials in auth_helper.py.

def main(authorization_data):

    try:
        # Create a Search campaign with one ad group and a responsive search ad.
                
        campaigns=campaign_service.factory.create('ArrayOfCampaign')
        campaign=set_elements_to_none(campaign_service.factory.create('Campaign'))
        campaign.BudgetType='DailyBudgetStandard'
        campaign.DailyBudget=50
        languages=campaign_service.factory.create('ns3:ArrayOfstring')
        languages.string.append('All')
        campaign.Languages=languages
        campaign.Name="Women's Shoes " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
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

        # Add keywords and ads within the ad group.
        
        keywords=campaign_service.factory.create('ArrayOfKeyword')
        keyword=set_elements_to_none(campaign_service.factory.create('Keyword'))
        keyword.Bid=campaign_service.factory.create('Bid')
        keyword.Bid.Amount=0.47
        keyword.Param2='10% Off'
        keyword.MatchType='Broad'
        keyword.Text='Brand-A Shoes'
        keywords.Keyword.append(keyword)

        output_status_message("-----\nAddKeywords:")
        add_keywords_response=campaign_service.AddKeywords(
            AdGroupId=ad_group_ids['long'][0],
            Keywords=keywords,
            ReturnInheritedBidStrategyTypes=False
        )
        keyword_ids={
            'long': add_keywords_response.KeywordIds['long'] if add_keywords_response.KeywordIds else None
        }
        output_status_message("KeywordIds:")
        output_array_of_long(keyword_ids)
        output_status_message("PartialErrors:")
        output_array_of_batcherror(add_keywords_response.PartialErrors)

        # The responsive search ad descriptions and headlines are stored as text assets. 
        # You must set between 2-4 descriptions and 3-15 headlines.
        
        ads=campaign_service.factory.create('ArrayOfAd')
        responsive_search_ad=set_elements_to_none(campaign_service.factory.create('ResponsiveSearchAd'))
        description_asset_links=campaign_service.factory.create('ArrayOfAssetLink')
        description_asset_link_a=set_elements_to_none(campaign_service.factory.create('AssetLink'))
        description_text_asset_a=set_elements_to_none(campaign_service.factory.create('TextAsset'))
        description_text_asset_a.Text="Find New Customers & Increase Sales!"
        description_asset_link_a.Asset=description_text_asset_a
        description_asset_link_a.PinnedField="Description1"
        description_asset_links.AssetLink.append(description_asset_link_a)
        description_asset_link_b=set_elements_to_none(campaign_service.factory.create('AssetLink'))
        description_text_asset_b=set_elements_to_none(campaign_service.factory.create('TextAsset'))
        description_text_asset_b.Text="Start Advertising on Contoso Today."
        description_asset_link_b.Asset=description_text_asset_b
        description_asset_link_b.PinnedField="Description2"
        description_asset_links.AssetLink.append(description_asset_link_b)
        responsive_search_ad.Descriptions=description_asset_links
        headline_asset_links=campaign_service.factory.create('ArrayOfAssetLink')
        headline_asset_link_a=set_elements_to_none(campaign_service.factory.create('AssetLink'))
        headline_text_asset_a=set_elements_to_none(campaign_service.factory.create('TextAsset'))
        headline_text_asset_a.Text="Contoso"
        headline_asset_link_a.Asset=headline_text_asset_a
        headline_asset_link_a.PinnedField="Headline1"
        headline_asset_links.AssetLink.append(headline_asset_link_a)
        headline_asset_link_b=set_elements_to_none(campaign_service.factory.create('AssetLink'))
        headline_text_asset_b=set_elements_to_none(campaign_service.factory.create('TextAsset'))
        headline_text_asset_b.Text="Quick & Easy Setup"
        headline_asset_link_b.Asset=headline_text_asset_b
        headline_asset_link_b.PinnedField=None
        headline_asset_links.AssetLink.append(headline_asset_link_b)
        headline_asset_link_c=set_elements_to_none(campaign_service.factory.create('AssetLink'))
        headline_text_asset_c=set_elements_to_none(campaign_service.factory.create('TextAsset'))
        headline_text_asset_c.Text="Seemless Integration"
        headline_asset_link_c.Asset=headline_text_asset_c
        headline_asset_link_c.PinnedField=None
        headline_asset_links.AssetLink.append(headline_asset_link_c)
        responsive_search_ad.Headlines=headline_asset_links
        responsive_search_ad.Path1='seattle'
        responsive_search_ad.Path2='shoe sale'
        responsive_search_ad.Type='ResponsiveSearch'
        final_urls=campaign_service.factory.create('ns3:ArrayOfstring')
        final_urls.string.append('https://www.contoso.com/womenshoesale')
        responsive_search_ad.FinalUrls=final_urls
        ads.Ad.append(responsive_search_ad)
        
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
