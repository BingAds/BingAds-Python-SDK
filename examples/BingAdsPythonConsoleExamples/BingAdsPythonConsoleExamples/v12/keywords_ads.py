from auth_helper import *
from campaignmanagement_example_helper import *

# You must provide credentials in auth_helper.py.

def main(authorization_data):

    try:
        # Let's create a new budget and share it with a new campaign.
                
        budgets = campaign_service.factory.create('ArrayOfBudget')
        budget=set_elements_to_none(campaign_service.factory.create('Budget'))
        budget.Amount = 50
        budget.BudgetType = 'DailyBudgetStandard'
        budget.Name = "My Shared Budget " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        budgets.Budget.append(budget)
                    
        add_budgets_response = campaign_service.AddBudgets(budgets)
        budget_ids={
            'long': add_budgets_response.BudgetIds['long'] if add_budgets_response.BudgetIds['long'] else None
        }
        output_status_message("Budget Ids:")
        output_array_of_long(budget_ids)

        # Specify one or more campaigns.
        
        campaigns=campaign_service.factory.create('ArrayOfCampaign')
        campaign=set_elements_to_none(campaign_service.factory.create('Campaign'))
        campaign.Name="Summer Shoes " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        campaign.Description="Summer shoes line."

        # You must choose to set either the shared  budget ID or daily amount.
        # You can set one or the other, but you may not set both.
        campaign.BudgetId = budget_ids['long'][0] if len(budget_ids['long']) > 0 else None
        campaign.DailyBudget = None if len(budget_ids['long']) > 0 else 50
        campaign.BudgetType = 'DailyBudgetStandard'

        campaign.TimeZone='PacificTimeUSCanadaTijuana'
        campaign.Status='Paused'

        # You can set your campaign bid strategy to Enhanced CPC (EnhancedCpcBiddingScheme) 
        # and then, at any time, set an individual ad group or keyword bid strategy to 
        # Manual CPC (ManualCpcBiddingScheme).
        # For campaigns you can use either of the EnhancedCpcBiddingScheme or ManualCpcBiddingScheme objects. 
        # If you do not set this element, then ManualCpcBiddingScheme is used by default.
        campaign_bidding_scheme=set_elements_to_none(campaign_service.factory.create('EnhancedCpcBiddingScheme'))
        campaign.BiddingScheme=campaign_bidding_scheme

        # Used with FinalUrls shown in the expanded text ads that we will add below.
        campaign.TrackingUrlTemplate="http://tracker.example.com/?season={_season}&promocode={_promocode}&u={lpurl}"
        
        campaigns.Campaign.append(campaign)

        ad_groups=campaign_service.factory.create('ArrayOfAdGroup')
        ad_group=set_elements_to_none(campaign_service.factory.create('AdGroup'))
        ad_group.Name="Women's Red Shoes"
        ad_group.Network='OwnedAndOperatedAndSyndicatedSearch'
        ad_group.Status='Paused'
        end_date=campaign_service.factory.create('Date')
        end_date.Day=31
        end_date.Month=12
        end_date.Year=strftime("%Y", gmtime())
        ad_group.EndDate=end_date
        cpc_bid=campaign_service.factory.create('Bid')
        cpc_bid.Amount=0.09
        ad_group.CpcBid=cpc_bid
        ad_group.Language='English'

        # Applicable for all audiences that are associated with this ad group. Set TargetAndBid to True 
        # if you want to show ads only to people included in the remarketing list, with the option to change
        # the bid amount. 
        ad_group_settings=campaign_service.factory.create('ArrayOfSetting')
        ad_group_target_setting=campaign_service.factory.create('TargetSetting')
        ad_group_audience_target_setting_detail=campaign_service.factory.create('TargetSettingDetail')
        ad_group_audience_target_setting_detail.CriterionTypeGroup='Audience'
        ad_group_audience_target_setting_detail.TargetAndBid=True
        ad_group_target_setting.Details.TargetSettingDetail.append(ad_group_audience_target_setting_detail)
        ad_group_settings.Setting.append(ad_group_target_setting)
        ad_group.Settings=ad_group_settings
        
        # For ad groups you can use either of the InheritFromParentBiddingScheme or ManualCpcBiddingScheme objects. 
        # If you do not set this element, then InheritFromParentBiddingScheme is used by default.
        ad_group_bidding_scheme=set_elements_to_none(campaign_service.factory.create('ManualCpcBiddingScheme'))
        ad_group.BiddingScheme=ad_group_bidding_scheme
        
        # You could use a tracking template which would override the campaign level
        # tracking template. Tracking templates defined for lower level entities 
        # override those set for higher level entities.
        # In this example we are using the campaign level tracking template.
        ad_group.TrackingUrlTemplate=None

        ad_groups.AdGroup.append(ad_group)

        # In this example only the first 3 ads should succeed. 
        # The TitlePart2 of the fourth ad is empty and not valid,
        # and the fifth ad is a duplicate of the second ad.
        
        ads=campaign_service.factory.create('ArrayOfAd')
        
        for index in range(5):
            expanded_text_ad=set_elements_to_none(campaign_service.factory.create('ExpandedTextAd'))
            expanded_text_ad.TitlePart1='Contoso'
            expanded_text_ad.TitlePart2='Fast & Easy Setup'
            expanded_text_ad.Text='Huge Savings on red shoes.'
            expanded_text_ad.Path1='seattle'
            expanded_text_ad.Path2='shoe sale'
            expanded_text_ad.Type='ExpandedText'
            
            # With FinalUrls you can separate the tracking template, custom parameters, and 
            # landing page URLs.
            final_urls=campaign_service.factory.create('ns3:ArrayOfstring')
            final_urls.string.append('http://www.contoso.com/womenshoesale')
            expanded_text_ad.FinalUrls=final_urls

            # Final Mobile URLs can also be used if you want to direct the user to a different page 
            # for mobile devices.
            final_mobile_urls=campaign_service.factory.create('ns3:ArrayOfstring')
            final_mobile_urls.string.append('http://mobile.contoso.com/womenshoesale')
            expanded_text_ad.FinalMobileUrls=final_mobile_urls

            # You could use a tracking template which would override the campaign level
            # tracking template. Tracking templates defined for lower level entities 
            # override those set for higher level entities.
            # In this example we are using the campaign level tracking template.
            expanded_text_ad.TrackingUrlTemplate=None,

            # Set custom parameters that are specific to this ad, 
            # and can be used by the ad, ad group, campaign, or account level tracking template. 
            # In this example we are using the campaign level tracking template.
            url_custom_parameters=campaign_service.factory.create('CustomParameters')
            parameters=campaign_service.factory.create('ArrayOfCustomParameter')
            custom_parameter1=campaign_service.factory.create('CustomParameter')
            custom_parameter1.Key='promoCode'
            custom_parameter1.Value='PROMO' + str(index)
            parameters.CustomParameter.append(custom_parameter1)
            custom_parameter2=campaign_service.factory.create('CustomParameter')
            custom_parameter2.Key='season'
            custom_parameter2.Value='summer'
            parameters.CustomParameter.append(custom_parameter2)
            url_custom_parameters.Parameters=parameters
            expanded_text_ad.UrlCustomParameters=url_custom_parameters
            ads.Ad.append(expanded_text_ad)
        
        ads.Ad[1].TitlePart2="Quick & Easy Setup"
        ads.Ad[2].TitlePart2="Fast & Simple Setup"
        ads.Ad[3].TitlePart2=''
        ads.Ad[4].TitlePart2="Quick & Easy Setup"

        # In this example only the second keyword should succeed. The Text of the first keyword exceeds the limit,
        # and the third keyword is a duplicate of the second keyword.  

        keywords=campaign_service.factory.create('ArrayOfKeyword')
        
        for index in range(3):
            keyword=set_elements_to_none(campaign_service.factory.create('Keyword'))
            keyword.Bid=campaign_service.factory.create('Bid')
            keyword.Bid.Amount=0.47
            keyword.Param2='10% Off'
            keyword.MatchType='Broad'
            keyword.Text='Brand-A Shoes'

            # For keywords you can use either of the InheritFromParentBiddingScheme or ManualCpcBiddingScheme objects. 
            # If you do not set this element, then InheritFromParentBiddingScheme is used by default.
            keyword_bidding_scheme=set_elements_to_none(campaign_service.factory.create('InheritFromParentBiddingScheme'))
            keyword.BiddingScheme=keyword_bidding_scheme

            keywords.Keyword.append(keyword)
        
        keywords.Keyword[0].Text=(
            "Brand-A Shoes Brand-A Shoes Brand-A Shoes Brand-A Shoes Brand-A Shoes "
		    "Brand-A Shoes Brand-A Shoes Brand-A Shoes Brand-A Shoes Brand-A Shoes "
		    "Brand-A Shoes Brand-A Shoes Brand-A Shoes Brand-A Shoes Brand-A Shoes"
        )

        # Add the campaign, ad group, keywords, and ads
        
        add_campaigns_response=campaign_service.AddCampaigns(
            AccountId=authorization_data.account_id,
            Campaigns=campaigns
        )
        campaign_ids={
            'long': add_campaigns_response.CampaignIds['long'] if add_campaigns_response.CampaignIds['long'] else None
        }
        output_status_message("Campaign Ids:")
        output_array_of_long(campaign_ids)
        
        add_ad_groups_response=campaign_service.AddAdGroups(
            CampaignId=campaign_ids['long'][0],
            AdGroups=ad_groups
        )
        ad_group_ids={
            'long': add_ad_groups_response.AdGroupIds['long'] if add_ad_groups_response.AdGroupIds['long'] else None
        }
        output_status_message("Ad Group Ids:")
        output_array_of_long(ad_group_ids)
        
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
        output_array_of_long(ad_ids)
        
        add_keywords_response=campaign_service.AddKeywords(
            AdGroupId=ad_group_ids['long'][0],
            Keywords=keywords
        )
        keyword_ids={
            'long': add_keywords_response.KeywordIds['long'] if add_keywords_response.KeywordIds else None
        }
        keyword_errors={
            'BatchError': add_keywords_response.PartialErrors['BatchError'] if add_keywords_response.PartialErrors else None
        } 
        output_status_message("Keyword Ids:")
        output_array_of_long(keyword_ids)
        
        # Here is a simple example that updates the campaign budget.
        # If the campaign has a shared budget you cannot update the Campaign budget amount,
        # and you must instead update the amount in the Budget object. If you try to update 
        # the budget amount of a campaign that has a shared budget, the service will return 
        # the CampaignServiceCannotUpdateSharedBudget error code.

        get_campaigns=campaign_service.GetCampaignsByAccountId(
            AccountId=authorization_data.account_id,
            CampaignType=ALL_CAMPAIGN_TYPES
        )
        
        update_campaigns = campaign_service.factory.create('ArrayOfCampaign')
        update_budgets = campaign_service.factory.create('ArrayOfBudget')
        get_campaign_ids = []
        get_budget_ids = []

        # Increase existing budgets by 20%
        for campaign in get_campaigns['Campaign']:

            # If the campaign has a shared budget, let's add the budget ID to the list we will update later.
            if campaign is not None and campaign.BudgetId is not None and campaign.BudgetId > 0:
                get_budget_ids.append(campaign.BudgetId)
            # If the campaign has its own budget, let's add it to the list of campaigns to update later.
            elif campaign is not None:
                update_campaigns.Campaign.append(campaign)
        
        # Update shared budgets in Budget objects.
        if get_budget_ids is not None and len(get_budget_ids) > 0:
            # The UpdateBudgets operation only accepts 100 Budget objects per call. 
            # To simply the example we will update the first 100.
            distinct_budget_ids = {'long': list(set(get_budget_ids))[:100]}
            get_budgets = campaign_service.GetBudgetsByIds(
                BudgetIds=distinct_budget_ids
            ).Budgets

            output_status_message("List of shared budgets BEFORE update:\n")
            for budget in get_budgets['Budget']:
                output_status_message("Budget:")
                output_budget(budget)

            output_status_message("List of campaigns that share each budget:\n")
            get_campaign_id_collection = campaign_service.GetCampaignIdsByBudgetIds(distinct_budget_ids).CampaignIdCollection

            index=0

            for index in range(len(get_campaign_id_collection['IdCollection'])):
                output_status_message("BudgetId: {0}".format(distinct_budget_ids['long'][index]))
                output_status_message("Campaign Ids:")
                if get_campaign_id_collection['IdCollection'][index] is not None:
                    for id in get_campaign_id_collection['IdCollection'][index].Ids['long']:
                        output_status_message("\t{0}".format(id))
                index=index+1

            for budget in get_budgets['Budget']:
                if budget is not None:
                    # Increase budget by 20 %
                    budget.Amount *= 1.2
                    update_budgets.Budget.append(budget)
            campaign_service.UpdateBudgets(Budgets=update_budgets)

            get_budgets = campaign_service.GetBudgetsByIds(
                BudgetIds=distinct_budget_ids
            ).Budgets

            output_status_message("List of shared budgets AFTER update:\n")
            for budget in get_budgets['Budget']:
                output_status_message("Budget:")
                output_budget(budget)

        # Update unshared budgets in Campaign objects.
        if update_campaigns is not None:

            # The UpdateCampaigns operation only accepts 100 Campaign objects per call. 
            # To simply the example we will update the first 100.
            update_100_campaigns = update_campaigns['Campaign'][:100]
            update_campaigns = campaign_service.factory.create('ArrayOfCampaign')
            for campaign in update_100_campaigns:
                update_campaigns.Campaign.append(campaign)

            output_status_message("List of campaigns with unshared budget BEFORE budget update:\n")
            for campaign in update_campaigns['Campaign']:
                output_status_message("Campaign:")
                output_campaign(campaign)
                set_read_only_campaign_elements_to_none(campaign)

                # Increase budget by 20 %
                campaign.DailyBudget *= 1.2

                get_campaign_ids.append(campaign.Id)
            
            campaign_service.UpdateCampaigns(
                AccountId=authorization_data.account_id,
                Campaigns=update_campaigns
            )

            get_campaigns=campaign_service.GetCampaignsByIds(
                AccountId=authorization_data.account_id,
                CampaignIds={'long': get_campaign_ids},
                CampaignType=ALL_CAMPAIGN_TYPES
            ).Campaigns
            
            output_status_message("List of campaigns with unshared budget AFTER budget update:\n")
            for campaign in get_campaigns['Campaign']:
                output_status_message("Campaign:")
                output_campaign(campaign)
        
        # Update the Text for the 3 successfully created ads, and update some UrlCustomParameters.
        update_ads=campaign_service.factory.create('ArrayOfAd')

        # Set the UrlCustomParameters element to null or empty to retain any 
        # existing custom parameters.
        expanded_text_ad_0=set_elements_to_none(campaign_service.factory.create('ExpandedTextAd'))
        expanded_text_ad_0.Id=ad_ids['long'][0]
        expanded_text_ad_0.Text='Huge Savings on All Red Shoes.'
        expanded_text_ad_0.UrlCustomParameters=None
        expanded_text_ad_0.Type='ExpandedText'
        update_ads.Ad.append(expanded_text_ad_0)

        # To remove all custom parameters, set the Parameters element of the 
        # CustomParameters object to null or empty.
        expanded_text_ad_1=set_elements_to_none(campaign_service.factory.create('ExpandedTextAd'))
        expanded_text_ad_1.Id=ad_ids['long'][1]
        expanded_text_ad_1.Text='Huge Savings on All Red Shoes.'
        url_custom_parameters_1=campaign_service.factory.create('CustomParameters')
        parameters_1=campaign_service.factory.create('ArrayOfCustomParameter')
        custom_parameter_1=campaign_service.factory.create('CustomParameter')
        # Set the CustomParameter to None or leave unspecified to have the same effect
        #custom_parameter_1=None
        parameters_1.CustomParameter.append(custom_parameter_1)
        url_custom_parameters_1.Parameters=parameters_1
        expanded_text_ad_1.UrlCustomParameters=url_custom_parameters_1
        expanded_text_ad_1.Type='ExpandedText'
        update_ads.Ad.append(expanded_text_ad_1)

        # To remove a subset of custom parameters, specify the custom parameters that 
        # you want to keep in the Parameters element of the CustomParameters object.
        expanded_text_ad_2=set_elements_to_none(campaign_service.factory.create('ExpandedTextAd'))
        expanded_text_ad_2.Id=ad_ids['long'][2]
        expanded_text_ad_2.Text='Huge Savings on All Red Shoes.'
        url_custom_parameters_2=campaign_service.factory.create('CustomParameters')
        parameters_2=campaign_service.factory.create('ArrayOfCustomParameter')
        custom_parameter_2=campaign_service.factory.create('CustomParameter')
        custom_parameter_2.Key='promoCode'
        custom_parameter_2.Value='updatedpromo'
        parameters_2.CustomParameter.append(custom_parameter_2)
        url_custom_parameters_2.Parameters=parameters_2
        expanded_text_ad_2.UrlCustomParameters=url_custom_parameters_2
        expanded_text_ad_2.Type='ExpandedText'
        update_ads.Ad.append(expanded_text_ad_2)

        # As an exercise you can step through using the debugger and view the results.

        campaign_service.GetAdsByAdGroupId(
            AdGroupId=ad_group_ids['long'][0],
            AdTypes=ALL_AD_TYPES
        )
        campaign_service.UpdateAds(
            AdGroupId=ad_group_ids['long'][0],
            Ads=update_ads
        )
        campaign_service.GetAdsByAdGroupId(
            AdGroupId=ad_group_ids['long'][0],
            AdTypes=ALL_AD_TYPES
        )

        update_keywords=campaign_service.factory.create('ArrayOfKeyword')
        update_keyword=set_elements_to_none(campaign_service.factory.create('Keyword'))
        update_keyword.Id=keyword_ids['long'][0]
        
        # You can set the Bid.Amount property to change the keyword level bid.
        update_keyword.Bid=campaign_service.factory.create('Bid')
        update_keyword.Bid.Amount=0.46
        
        # When using the Campaign Management service with the Bing Ads Python SDK,
        # if you want to inherit the ad group level bid, instead of using the keyword level bid,
        # the service expects that you would have set the Bid.Amount null (new empty Bid). However, 
        # it is important to note that SUDS (used by the Bing Ads Python SDK) does not allow the 
        # Bid.Amount property to be null, so you will need to delete the keyword and then add a new 
        # keyword without the Bid set, or with Bid set to None. 

        # We recommend that you use the BulkServiceManager for keyword updates, i.e. upload BulkKeyword entities.
        # With the BulkKeyword upload, you won't have to delete and add keywords to inherit from the ad group level bid,
        # and you also have the flexibility of updating millions of keywords across all campaigns in your account.
        # For examples of how to use the Bulk service for keyword updates, please see BulkKeywordsAds.py.
        
        # When using the Campaign Management service with the Bing Ads Python SDK,
        # if the Bid property is not specified or is null, your keyword bid will not be updated.
        #update_keyword.Bid=None
        
        update_keywords.Keyword.append(update_keyword)

        campaign_service.GetKeywordsByAdGroupId(
            AdGroupId=ad_group_ids['long'][0]
        )
        campaign_service.UpdateKeywords(
            AdGroupId=ad_group_ids['long'][0],
            Keywords=update_keywords
        )
        campaign_service.GetKeywordsByAdGroupId(
            AdGroupId=ad_group_ids['long'][0]
        )
        
        # Delete the campaign, ad group, keyword, and ad that were previously added. 
        # You should remove this line if you want to view the added entities in the 
        # Bing Ads web application or another tool.

        campaign_service.DeleteCampaigns(
            AccountId=authorization_data.account_id,
            CampaignIds=campaign_ids
        )
        for campaign_id in campaign_ids['long']:
            output_status_message("Deleted CampaignId {0}\n".format(campaign_id))
        
        # This sample will attempt to delete the budget that was created above.
        if len(budget_ids['long']) > 0:
            campaign_service.DeleteBudgets(
                BudgetIds=budget_ids
            )
            for budget_id in budget_ids['long']:
                output_status_message("Deleted BudgetId {0}\n".format(budget_id))

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
        version=12,
        authorization_data=authorization_data, 
        environment=ENVIRONMENT,
    )

    # You should authenticate for Bing Ads production services with a Microsoft Account.
        
    authenticate(authorization_data)
        
    main(authorization_data)
