from auth_helper import *
from adinsight_example_helper import *
from campaignmanagement_example_helper import *

# You must provide credentials in auth_helper.py.

DOMAIN_NAME="contoso.com"
LANGUAGE="EN"

def get_ad_group_webpage_positive_page_content_example(ad_group_id):
    biddable_ad_group_criterion=set_elements_to_none(campaign_service.factory.create('BiddableAdGroupCriterion'))
    biddable_ad_group_criterion.Type='BiddableAdGroupCriterion'
    biddable_ad_group_criterion.AdGroupId=ad_group_id
    fixed_bid=set_elements_to_none(campaign_service.factory.create('FixedBid'))
    fixed_bid.Amount=0.45
    biddable_ad_group_criterion.CriterionBid=fixed_bid
    conditions=campaign_service.factory.create('ArrayOfWebpageCondition')
    condition=set_elements_to_none(campaign_service.factory.create('WebpageCondition'))
    condition.Operand='PageContent'
    condition.Argument='flowers'
    conditions.WebpageCondition.append(condition)
    webpage_parameter=set_elements_to_none(campaign_service.factory.create('WebpageParameter'))
    webpage_parameter.Conditions=conditions
    webpage_parameter.CriterionName='Ad Group Webpage Positive Page Content Criterion'
    webpage=set_elements_to_none(campaign_service.factory.create('Webpage'))
    webpage.Type='Webpage'
    webpage.Parameter=webpage_parameter
    biddable_ad_group_criterion.Criterion=webpage

    return biddable_ad_group_criterion

def get_ad_group_webpage_positive_category_example(ad_group_id, category_name):
    biddable_ad_group_criterion=set_elements_to_none(campaign_service.factory.create('BiddableAdGroupCriterion'))
    biddable_ad_group_criterion.Type='BiddableAdGroupCriterion'
    biddable_ad_group_criterion.AdGroupId=ad_group_id
    fixed_bid=set_elements_to_none(campaign_service.factory.create('FixedBid'))
    fixed_bid.Amount=0.50
    biddable_ad_group_criterion.CriterionBid=fixed_bid
    conditions=campaign_service.factory.create('ArrayOfWebpageCondition')
    condition=set_elements_to_none(campaign_service.factory.create('WebpageCondition'))
    condition.Argument=category_name
    condition.Operand='Category'
    conditions.WebpageCondition.append(condition)
    webpage_parameter=set_elements_to_none(campaign_service.factory.create('WebpageParameter'))
    webpage_parameter.Conditions=conditions
    webpage_parameter.CriterionName='Ad Group Webpage Positive Category Criterion'
    webpage=set_elements_to_none(campaign_service.factory.create('Webpage'))
    webpage.Type='Webpage'
    webpage.Parameter=webpage_parameter
    biddable_ad_group_criterion.Criterion=webpage

    return biddable_ad_group_criterion

def get_ad_group_webpage_negative_url_example(ad_group_id):
    negative_ad_group_criterion=set_elements_to_none(campaign_service.factory.create('NegativeAdGroupCriterion'))
    negative_ad_group_criterion.Type='NegativeAdGroupCriterion'
    negative_ad_group_criterion.AdGroupId=ad_group_id    
    # You can choose whether you want the criterion argument to match partial URLs, 
    # page content, page title, or categories that Bing thinks applies to your website.
    conditions=campaign_service.factory.create('ArrayOfWebpageCondition')
    condition=set_elements_to_none(campaign_service.factory.create('WebpageCondition'))
    condition.Operand='Url'
    condition.Argument=DOMAIN_NAME
    conditions.WebpageCondition.append(condition)
    webpage_parameter=set_elements_to_none(campaign_service.factory.create('WebpageParameter'))
    webpage_parameter.Conditions=conditions
    # If you do not specify any name, then it will be set to a concatenated list of conditions. 
    webpage_parameter.CriterionName=None
    webpage=set_elements_to_none(campaign_service.factory.create('Webpage'))
    webpage.Type='Webpage'
    webpage.Parameter=webpage_parameter
    negative_ad_group_criterion.Criterion=webpage

    return negative_ad_group_criterion

def get_campaign_webpage_negative_url_example(campaign_id):
    negative_campaign_criterion=set_elements_to_none(campaign_service.factory.create('NegativeCampaignCriterion'))
    negative_campaign_criterion.Type='NegativeCampaignCriterion'
    negative_campaign_criterion.CampaignId=campaign_id
    
    conditions=campaign_service.factory.create('ArrayOfWebpageCondition')
    condition=set_elements_to_none(campaign_service.factory.create('WebpageCondition'))
    condition.Argument=DOMAIN_NAME + "\\seattle"
    condition.Operand='Url'
    conditions.WebpageCondition.append(condition)

    webpage_parameter=set_elements_to_none(campaign_service.factory.create('WebpageParameter'))
    webpage_parameter.Conditions=conditions
    webpage_parameter.CriterionName='Campaign Negative Webpage Url Criterion'

    webpage=set_elements_to_none(campaign_service.factory.create('Webpage'))
    webpage.Type='Webpage'
    webpage.Parameter=webpage_parameter
    negative_campaign_criterion.Criterion=webpage

    return negative_campaign_criterion

def main(authorization_data):

    try:
        # To get started with dynamic search ads, first you'll need to add a new Search campaign 
        # Include a DynamicSearchAdsSetting that specifies the target website domain and language.

        campaigns=campaign_service.factory.create('ArrayOfCampaign')
        campaign=set_elements_to_none(campaign_service.factory.create('Campaign'))
        campaign.BudgetType='DailyBudgetStandard'
        campaign.CampaignType=['DynamicSearchAds']
        campaign.DailyBudget=50
        languages=campaign_service.factory.create('ns3:ArrayOfstring')
        languages.string.append('All')
        campaign.Languages=languages
        campaign.Name="Women's Shoes " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        settings=campaign_service.factory.create('ArrayOfSetting')
        setting=set_elements_to_none(campaign_service.factory.create('DynamicSearchAdsSetting'))
        setting.DomainName=DOMAIN_NAME
        setting.Language=LANGUAGE
        settings.Setting.append(setting)
        campaign.Settings=settings
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

        # Create a new ad group with type set to "SearchDynamic"

        ad_groups=campaign_service.factory.create('ArrayOfAdGroup')
        ad_group=set_elements_to_none(campaign_service.factory.create('AdGroup'))
        ad_group.AdGroupType='SearchDynamic'
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

        # You can add one or more Webpage criterions to each ad group that helps determine 
        # whether or not to serve dynamic search ads.

        ad_group_criterions=campaign_service.factory.create('ArrayOfAdGroupCriterion')
        ad_group_webpage_positive_page_content=get_ad_group_webpage_positive_page_content_example(ad_group_ids['long'][0])
        ad_group_criterions.AdGroupCriterion.append(ad_group_webpage_positive_page_content)

        # To discover the categories that you can use for Webpage criterion (positive or negative), 
        # use the GetDomainCategories operation with the Ad Insight service.

        output_status_message("-----\nGetDomainCategories:")
        categories=adinsight_service.GetDomainCategories(
            CategoryName=None,
            DomainName=DOMAIN_NAME,
            Language=LANGUAGE
        )
        output_status_message("DomainCategories:")
        output_array_of_domaincategory(categories)

        # If any categories are available let's use one as a condition.
        if(categories is not None and len(categories) > 0):
            ad_group_webpage_positive_category=get_ad_group_webpage_positive_category_example(
                ad_group_ids['long'][0], 
                categories['DomainCategory'][0].CategoryName
                )
            ad_group_criterions.AdGroupCriterion.append(ad_group_webpage_positive_category)

        # If you want to exclude certain portions of your website, you can add negative Webpage 
        # criterion at the campaign and ad group level. 

        ad_group_webpage_negative_url=get_ad_group_webpage_negative_url_example(ad_group_ids['long'][0])
        ad_group_criterions.AdGroupCriterion.append(ad_group_webpage_negative_url)
        
        output_status_message("-----\nAddAdGroupCriterions:")
        add_ad_group_criterions_response = campaign_service.AddAdGroupCriterions(
            AdGroupCriterions=ad_group_criterions,
            CriterionType='Webpage'
        )
        ad_group_criterion_ids={
            'long': add_ad_group_criterions_response.AdGroupCriterionIds['long'] 
            if add_ad_group_criterions_response.AdGroupCriterionIds['long'] else None
        }
        output_status_message("AdGroupCriterionIds:")
        output_array_of_long(ad_group_criterion_ids)
        output_status_message("NestedPartialErrors:")
        output_array_of_batcherrorcollection(add_ad_group_criterions_response.NestedPartialErrors) 
        
        # The negative Webpage criterion at the campaign level applies to all ad groups 
        # within the campaign; however, if you define ad group level negative Webpage criterion, 
        # the campaign criterion is ignored for that ad group.

        campaign_criterions=campaign_service.factory.create('ArrayOfCampaignCriterion')
        campaign_webpage_negative_url = get_campaign_webpage_negative_url_example(campaign_ids['long'][0])
        campaign_criterions.CampaignCriterion.append(campaign_webpage_negative_url)

        output_status_message("-----\nAddCampaignCriterions:")
        add_campaign_criterions_response = campaign_service.AddCampaignCriterions(
            CampaignCriterions=campaign_criterions,
            CriterionType='Webpage'
        )
        campaign_criterion_ids={
            'long': add_campaign_criterions_response.CampaignCriterionIds['long'] 
            if add_campaign_criterions_response.CampaignCriterionIds['long'] else None
        }
        output_status_message("CampaignCriterionIds:")
        output_array_of_long(campaign_criterion_ids)
        output_status_message("NestedPartialErrors:")
        output_array_of_batcherrorcollection(add_campaign_criterions_response.NestedPartialErrors) 

        # Finally you must add at least one DynamicSearchAd into the ad group. The ad title and display URL 
        # are generated automatically based on the website domain and language that you want to target.

        ads=campaign_service.factory.create('ArrayOfAd')
        dynamic_search_ad=set_elements_to_none(campaign_service.factory.create('DynamicSearchAd'))
        dynamic_search_ad.Text='Find New Customers & Increase Sales!'
        dynamic_search_ad.TextPart2='Start Advertising on Contoso Today.'
        dynamic_search_ad.Path1='seattle'
        dynamic_search_ad.Path2='shoe sale'
        dynamic_search_ad.Type='DynamicSearch'
        # You cannot set FinalUrls for dynamic search ads. 
        # The Final URL will be a dynamically selected landing page.
        # The final URL is distinct from the path that customers will see and click on in your ad.
        dynamic_search_ad.FinalUrls=None
        ads.Ad.append(dynamic_search_ad)
                
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
    
    adinsight_service=ServiceClient(
        service='AdInsightService', 
        version=13,
        authorization_data=authorization_data, 
        environment=ENVIRONMENT,
    )     

    authenticate(authorization_data)       

    main(authorization_data)
