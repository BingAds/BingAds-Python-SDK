from auth_helper import *
from campaignmanagement_example_helper import *

# You must provide credentials in auth_helper.py.

def main(authorization_data):

    try:
        # Add a search campaign.
                
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
        
        ads=campaign_service.factory.create('ArrayOfAd')
        expanded_text_ad=set_elements_to_none(campaign_service.factory.create('ExpandedTextAd'))
        expanded_text_ad.TitlePart1='Contoso'
        expanded_text_ad.TitlePart2='Quick & Easy Setup'
        expanded_text_ad.TitlePart3='Seemless Integration'
        expanded_text_ad.Text='Find New Customers & Increase Sales!'
        expanded_text_ad.TextPart2='Start Advertising on Contoso Today.'
        expanded_text_ad.Path1='seattle'
        expanded_text_ad.Path2='shoe sale'
        expanded_text_ad.Type='ExpandedText'
        final_urls=campaign_service.factory.create('ns3:ArrayOfstring')
        final_urls.string.append('http://www.contoso.com/womenshoesale')
        expanded_text_ad.FinalUrls=final_urls
        ads.Ad.append(expanded_text_ad)
        
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
