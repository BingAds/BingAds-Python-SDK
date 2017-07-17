from auth_helper import *
from output_helper import *

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

    conditions=campaign_service.factory.create('ns0:ArrayOfWebpageCondition')
    condition=set_elements_to_none(campaign_service.factory.create('ns0:WebpageCondition'))
    condition.Operand='PageContent'
    condition.Argument='flowers'
    conditions.WebpageCondition.append(condition)

    webpage_parameter=set_elements_to_none(campaign_service.factory.create('ns0:WebpageParameter'))
    webpage_parameter.Conditions=conditions
    webpage_parameter.CriterionName='Ad Group Webpage Positive Page Content Criterion'

    webpage=set_elements_to_none(campaign_service.factory.create('ns0:Webpage'))
    webpage.Type='Webpage'
    webpage.Parameter=webpage_parameter
    biddable_ad_group_criterion.Criterion=webpage

    # DestinationUrl and FinalUrls are not supported with Webpage criterion. So,
    # we will leave them set to None. The Final URL is dynamically created at the ad level.

    # You could use a tracking template which would override the campaign level
    # tracking template. Tracking templates defined for lower-level entities 
    # override those set for higher-level entities.
    # In this example we are using the campaign-level tracking template. So,
    # we will leave TrackingUrlTemplate set to None.

    # Set custom parameters that are specific to this Webpage criterion, 
    # and can be used by the criterion, ad group, campaign, or account level tracking template. 
    # In this example we are using the campaign level tracking template.

    url_custom_parameters=campaign_service.factory.create('ns0:CustomParameters')
    parameters=campaign_service.factory.create('ns0:ArrayOfCustomParameter')
    custom_parameter1=campaign_service.factory.create('ns0:CustomParameter')
    custom_parameter1.Key='promoCode'
    custom_parameter1.Value='PROMO'
    parameters.CustomParameter.append(custom_parameter1)
    custom_parameter2=campaign_service.factory.create('ns0:CustomParameter')
    custom_parameter2.Key='season'
    custom_parameter2.Value='summer'
    parameters.CustomParameter.append(custom_parameter2)
    url_custom_parameters.Parameters=parameters
    biddable_ad_group_criterion.UrlCustomParameters=url_custom_parameters

    return biddable_ad_group_criterion

def get_ad_group_webpage_positive_category_example(ad_group_id, category_name):
    biddable_ad_group_criterion=set_elements_to_none(campaign_service.factory.create('BiddableAdGroupCriterion'))
    biddable_ad_group_criterion.Type='BiddableAdGroupCriterion'
    biddable_ad_group_criterion.AdGroupId=ad_group_id

    fixed_bid=set_elements_to_none(campaign_service.factory.create('FixedBid'))
    fixed_bid.Amount=0.50
    biddable_ad_group_criterion.CriterionBid=fixed_bid

    conditions=campaign_service.factory.create('ns0:ArrayOfWebpageCondition')
    condition=set_elements_to_none(campaign_service.factory.create('ns0:WebpageCondition'))
    condition.Argument=category_name
    condition.Operand='Category'
    conditions.WebpageCondition.append(condition)

    webpage_parameter=set_elements_to_none(campaign_service.factory.create('ns0:WebpageParameter'))
    webpage_parameter.Conditions=conditions
    webpage_parameter.CriterionName='Ad Group Webpage Positive Category Criterion'

    webpage=set_elements_to_none(campaign_service.factory.create('ns0:Webpage'))
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
    conditions=campaign_service.factory.create('ns0:ArrayOfWebpageCondition')
    condition=set_elements_to_none(campaign_service.factory.create('ns0:WebpageCondition'))
    condition.Operand='Url'
    condition.Argument=DOMAIN_NAME
    conditions.WebpageCondition.append(condition)

    webpage_parameter=set_elements_to_none(campaign_service.factory.create('ns0:WebpageParameter'))
    webpage_parameter.Conditions=conditions
    # If you do not specify any name, then it will be set to a concatenated list of conditions. 
    webpage_parameter.CriterionName=None

    webpage=set_elements_to_none(campaign_service.factory.create('ns0:Webpage'))
    webpage.Type='Webpage'
    webpage.Parameter=webpage_parameter
    negative_ad_group_criterion.Criterion=webpage

    return negative_ad_group_criterion


def get_campaign_webpage_negative_url_example(campaign_id):
    negative_campaign_criterion=set_elements_to_none(campaign_service.factory.create('NegativeCampaignCriterion'))
    negative_campaign_criterion.Type='NegativeCampaignCriterion'
    negative_campaign_criterion.CampaignId=campaign_id
    
    conditions=campaign_service.factory.create('ns0:ArrayOfWebpageCondition')
    condition=set_elements_to_none(campaign_service.factory.create('ns0:WebpageCondition'))
    condition.Argument=DOMAIN_NAME + "\\seattle"
    condition.Operand='Url'
    conditions.WebpageCondition.append(condition)

    webpage_parameter=set_elements_to_none(campaign_service.factory.create('ns0:WebpageParameter'))
    webpage_parameter.Conditions=conditions
    webpage_parameter.CriterionName='Campaign Negative Webpage Url Criterion'

    webpage=set_elements_to_none(campaign_service.factory.create('ns0:Webpage'))
    webpage.Type='Webpage'
    webpage.Parameter=webpage_parameter
    negative_campaign_criterion.Criterion=webpage

    return negative_campaign_criterion


def main(authorization_data):

    try:
        # To get started with dynamic search ads, first you'll need to add a new Campaign 
	    # with its type set to DynamicSearchAds. When you create the campaign, you'll need to 
	    # include a DynamicSearchAdsSetting that specifies the target web site domain and language.

        campaigns=campaign_service.factory.create('ArrayOfCampaign')
        campaign=set_elements_to_none(campaign_service.factory.create('Campaign'))
        campaign.CampaignType=['DynamicSearchAds']

        settings=campaign_service.factory.create('ArrayOfSetting')
        setting=set_elements_to_none(campaign_service.factory.create('DynamicSearchAdsSetting'))
        setting.DomainName=DOMAIN_NAME
        setting.Language=LANGUAGE
        settings.Setting.append(setting)
        campaign.Settings=settings

        campaign.Name="Women's Shoes " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        campaign.Description='Red shoes line.'

        # You must choose to set either the shared budget ID or daily amount.
        # You can set one or the other, but you may not set both.
        campaign.DailyBudget=50
        campaign.BudgetType='DailyBudgetStandard'

        # You can set your campaign bid strategy to Enhanced CPC (EnhancedCpcBiddingScheme) 
        # and then, at any time, set an individual ad group bid strategy to 
        # Manual CPC (ManualCpcBiddingScheme).
        campaign_bidding_scheme=set_elements_to_none(campaign_service.factory.create('EnhancedCpcBiddingScheme'))
        campaign.BiddingScheme=campaign_bidding_scheme

        campaign.TimeZone='PacificTimeUSCanadaTijuana'

        # Used with CustomParameters defined in lower level entities such as ads.
        campaign.TrackingUrlTemplate="http://tracker.example.com/?season={_season}&promocode={_promocode}&u={lpurl}"

        campaigns.Campaign.append(campaign)

        add_campaigns_response=campaign_service.AddCampaigns(
            AccountId=authorization_data.account_id,
            Campaigns=campaigns
        )

        campaign_ids={
            'long': add_campaigns_response.CampaignIds['long'] if add_campaigns_response.CampaignIds['long'] else None
        }

        output_status_message('Campaign Ids:')
        output_ids(campaign_ids)

        if hasattr(add_campaigns_response.PartialErrors, 'BatchError'):
            output_partial_errors(add_campaigns_response.PartialErrors)

        # Next, create a new AdGroup within the dynamic search ads campaign.

        ad_groups=campaign_service.factory.create('ArrayOfAdGroup')
        ad_group=set_elements_to_none(campaign_service.factory.create('AdGroup'))
        ad_group.Name="Women's Red Shoe Sale"
        ad_group.AdDistribution=['Search']
        end_date=campaign_service.factory.create('Date')
        end_date.Day=31
        end_date.Month=12
        current_time=gmtime()
        end_date.Year=current_time.tm_year + 1
        ad_group.EndDate=end_date
        search_bid=campaign_service.factory.create('Bid')
        search_bid.Amount=0.09
        ad_group.SearchBid=search_bid
        ad_group.Language='English'

        # For ad groups you can use either of the InheritFromParentBiddingScheme or ManualCpcBiddingScheme objects. 
        # If you do not set this element, then InheritFromParentBiddingScheme is used by default.
        ad_group_bidding_scheme=set_elements_to_none(campaign_service.factory.create('ManualCpcBiddingScheme'))
        ad_group.BiddingScheme=ad_group_bidding_scheme

        ad_groups.AdGroup.append(ad_group)

        add_ad_groups_response=campaign_service.AddAdGroups(
            CampaignId=campaign_ids['long'][0],
            AdGroups=ad_groups
        )

        ad_group_ids={
            'long': add_ad_groups_response.AdGroupIds['long'] if add_ad_groups_response.AdGroupIds['long'] else None
        }

        output_status_message("Ad Group Ids:")
        output_ids(ad_group_ids)

        if hasattr(add_ad_groups_response.PartialErrors, 'BatchError'):
            output_partial_errors(add_ad_groups_response.PartialErrors)

        # You can add one or more Webpage criterions to each ad group that helps determine 
        # whether or not to serve dynamic search ads.

        ad_group_criterions=campaign_service.factory.create('ArrayOfAdGroupCriterion')
        ad_group_webpage_positive_page_content=get_ad_group_webpage_positive_page_content_example(ad_group_ids['long'][0])
        ad_group_criterions.AdGroupCriterion.append(ad_group_webpage_positive_page_content)

        # To discover the categories that you can use for Webpage criterion (positive or negative), 
        # use the GetDomainCategories operation with the Ad Insight service.
        categories=adinsight_service.GetDomainCategories(
            DomainName=DOMAIN_NAME,
            Language=LANGUAGE
            )

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
        
        output_status_message("Adding Ad Group Webpage Criterion . . . \n")
        output_ad_group_criterions(ad_group_criterions)
        add_ad_group_criterions_response = campaign_service.AddAdGroupCriterions(
            AdGroupCriterions=ad_group_criterions,
            CriterionType='Webpage'
        )
        ad_group_criterion_ids={
            'long': add_ad_group_criterions_response.AdGroupCriterionIds['long'] if add_ad_group_criterions_response.AdGroupCriterionIds['long'] else None
        }
        output_status_message("Ad Group Criterion Ids:")
        output_ids(ad_group_criterion_ids)
        
        get_ad_group_criterions_by_ids_response = campaign_service.GetAdGroupCriterionsByIds(
            AdGroupId=ad_group_ids['long'][0],
            AdGroupCriterionIds=ad_group_criterion_ids,
            CriterionType='Webpage'
        )

        # The negative Webpage criterion at the campaign level applies to all ad groups 
        # within the campaign; however, if you define ad group level negative Webpage criterion, 
        # the campaign criterion is ignored for that ad group.

        campaign_criterions=campaign_service.factory.create('ArrayOfCampaignCriterion')
        campaign_webpage_negative_url = get_campaign_webpage_negative_url_example(campaign_ids['long'][0])
        campaign_criterions.CampaignCriterion.append(campaign_webpage_negative_url)

        output_status_message("Adding Campaign Webpage Criterion . . . \n")
        output_campaign_criterions(campaign_criterions)
        add_campaign_criterions_response = campaign_service.AddCampaignCriterions(
            CampaignCriterions=campaign_criterions,
            CriterionType='Webpage'
        )
        campaign_criterion_ids={
            'long': add_campaign_criterions_response.CampaignCriterionIds['long'] if add_campaign_criterions_response.CampaignCriterionIds['long'] else None
        }
        output_status_message("Campaign Criterion Ids:")
        output_ids(campaign_criterion_ids)

        # Finally you can add a DynamicSearchAd into the ad group. The ad title and display URL 
        # are generated automatically based on the website domain and language that you want to target.

        ads=campaign_service.factory.create('ArrayOfAd')
        dynamic_search_ad=set_elements_to_none(campaign_service.factory.create('DynamicSearchAd'))
        dynamic_search_ad.Text='Find New Customers & Increase Sales! Start Advertising on Contoso Today.'
        dynamic_search_ad.Path1='seattle'
        dynamic_search_ad.Path2='shoe sale'
        dynamic_search_ad.Type='DynamicSearch'
            
        # You cannot set FinalUrls. The Final URL will be a dynamically selected landing page.
        # The final URL is distinct from the path that customers will see and click on in your ad.
        dynamic_search_ad.FinalUrls=None

        # Final Mobile URLs can also be used if you want to direct the user to a different page 
        # for mobile devices.
        final_mobile_urls=campaign_service.factory.create('ns4:ArrayOfstring')
        final_mobile_urls.string.append('http://mobile.contoso.com/womenshoesale')
        dynamic_search_ad.FinalMobileUrls=final_mobile_urls

        # You could use a tracking template which would override the campaign level
        # tracking template. Tracking templates defined for lower level entities 
        # override those set for higher level entities.
        # In this example we are using the campaign level tracking template.
        dynamic_search_ad.TrackingUrlTemplate=None,

        # Set custom parameters that are specific to this ad, 
        # and can be used by the ad, webpage, ad group, campaign, or account level tracking template. 
        # In this example we are using the campaign level tracking template.
        url_custom_parameters=campaign_service.factory.create('ns0:CustomParameters')
        parameters=campaign_service.factory.create('ns0:ArrayOfCustomParameter')
        custom_parameter1=campaign_service.factory.create('ns0:CustomParameter')
        custom_parameter1.Key='promoCode'
        custom_parameter1.Value='PROMO'
        parameters.CustomParameter.append(custom_parameter1)
        custom_parameter2=campaign_service.factory.create('ns0:CustomParameter')
        custom_parameter2.Key='season'
        custom_parameter2.Value='summer'
        parameters.CustomParameter.append(custom_parameter2)
        url_custom_parameters.Parameters=parameters
        dynamic_search_ad.UrlCustomParameters=url_custom_parameters
        ads.Ad.append(dynamic_search_ad)
                
        add_ads_response=campaign_service.AddAds(
            AdGroupId=ad_group_ids['long'][0],
            Ads=ads
        )
        ad_ids={
            'long': add_ads_response.AdIds['long'] if add_ads_response.AdIds['long'] else None
        }
        ad_errors={
            'BatchError': add_ads_response.PartialErrors['BatchError'] if add_ads_response.PartialErrors else None
        }    
        output_status_message("Ad Ids:")
        output_ids(ad_ids)

        # Retrieve the Webpage criterion for the campaign.
        output_status_message("Retrieving the Campaign Webpage Criterions that we added . . . \n")
        get_campaign_criterions_by_ids_response = campaign_service.GetCampaignCriterionsByIds(
            CampaignId=campaign_ids['long'][0],
            CampaignCriterionIds=None,
            CriterionType='Webpage'
        )
        campaign_criterions= get_campaign_criterions_by_ids_response.CampaignCriterions['CampaignCriterion'] \
            if hasattr(get_campaign_criterions_by_ids_response.CampaignCriterions, 'CampaignCriterion') \
            else None
        output_campaign_criterions(campaign_criterions)

        # Retrieve the Webpage criterion for the ad group and then test some update scenarios.
        output_status_message("Retrieving the Ad Group Webpage Criterions that we added . . . \n")
        get_ad_group_criterions_by_ids_response = campaign_service.GetAdGroupCriterionsByIds(
            AdGroupId=ad_group_ids['long'][0],
            AdGroupCriterionIds=None,
            CriterionType='Webpage'
        )
        ad_group_criterions= get_ad_group_criterions_by_ids_response \
            if hasattr(get_ad_group_criterions_by_ids_response, 'AdGroupCriterion') \
            else None
        output_ad_group_criterions(ad_group_criterions)
                
        # You can update the bid for BiddableAdGroupCriterion

        update_bid=set_elements_to_none(campaign_service.factory.create('FixedBid'))
        update_bid.Amount=0.75
        
        # You can update the Webpage criterion name but cannot update the conditions. 
        # To update the conditions you must delete the criterion and add a new criterion.
        # This update attempt will return an error.
        
        conditions=campaign_service.factory.create('ns0:ArrayOfWebpageCondition')
        condition=set_elements_to_none(campaign_service.factory.create('ns0:WebpageCondition'))
        condition.Argument='Books'
        condition.Operand='PageContent'
        conditions.WebpageCondition.append(condition)

        failure_webpage_parameter=set_elements_to_none(campaign_service.factory.create('ns0:WebpageParameter'))
        failure_webpage_parameter.Conditions=conditions
        failure_webpage_parameter.CriterionName='Update Attempt Failure'

        update_criterion_attempt_failure=set_elements_to_none(campaign_service.factory.create('ns0:Webpage'))
        update_criterion_attempt_failure.Type='Webpage'
        update_criterion_attempt_failure.Parameter=failure_webpage_parameter
        
        success_webpage_parameter=set_elements_to_none(campaign_service.factory.create('ns0:WebpageParameter'))
        success_webpage_parameter.Conditions=None
        success_webpage_parameter.CriterionName='Update Attempt Success'

        update_criterion_attempt_success=set_elements_to_none(campaign_service.factory.create('ns0:Webpage'))
        update_criterion_attempt_success.Type='Webpage'
        update_criterion_attempt_success.Parameter=success_webpage_parameter

        for ad_group_criterion in ad_group_criterions['AdGroupCriterion']:
            if ad_group_criterion.Type == 'BiddableAdGroupCriterion':
                ad_group_criterion.CriterionBid = update_bid
                ad_group_criterion.Criterion = update_criterion_attempt_success
            elif ad_group_criterion.Type == 'NegativeAdGroupCriterion':
                ad_group_criterion.Criterion = update_criterion_attempt_failure     

        output_status_message("Updating Ad Group Webpage Criterion . . . \n")
        output_ad_group_criterions(ad_group_criterions)
        update_ad_group_criterions_response = campaign_service.UpdateAdGroupCriterions(
                AdGroupCriterions=ad_group_criterions,
                CriterionType='Webpage'
            )
        
        # Delete the campaign, ad group, criterion, and ad that were previously added. 
        # You should remove this line if you want to view the added entities in the 
        # Bing Ads web application or another tool.
        campaign_service.DeleteCampaigns(
            AccountId=authorization_data.account_id,
            CampaignIds=campaign_ids
        )

        for campaign_id in campaign_ids['long']:
            output_status_message("Deleted CampaignId {0}\n".format(campaign_id))

        output_status_message("Program execution completed")

    except WebFault as ex:
        output_webfault_errors(ex)
    except Exception as ex:
        output_status_message(ex)

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
        authorization_data=authorization_data, 
        environment=ENVIRONMENT,
        version=11,
    )
    
    adinsight_service=ServiceClient(
        service='AdInsightService', 
        authorization_data=authorization_data, 
        environment=ENVIRONMENT,
        version=11
    )

    # You should authenticate for Bing Ads production services with a Microsoft Account, 
    # instead of providing the Bing Ads username and password set. 
    # Authentication with a Microsoft Account is currently not supported in Sandbox.       

    authenticate(authorization_data)       

    main(authorization_data)