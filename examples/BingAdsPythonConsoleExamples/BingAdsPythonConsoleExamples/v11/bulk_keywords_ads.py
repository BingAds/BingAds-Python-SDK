from auth_helper import *
from bulk_service_manager_helper import *
from output_helper import *

# You must provide credentials in auth_helper.py.

def main(authorization_data):

    errors=[]

    try:
        # Let's create a new budget and share it with a new campaign.

        upload_entities=[]
        
        bulk_budget=BulkBudget()
        bulk_budget.client_id='YourClientIdGoesHere'
        budget=set_elements_to_none(campaign_service.factory.create('Budget'))
        budget.Amount=50
        budget.BudgetType='DailyBudgetStandard'
        budget.Id=BUDGET_ID_KEY
        budget.Name="My Shared Budget " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        bulk_budget.budget=budget
        upload_entities.append(bulk_budget)
                
        bulk_campaign=BulkCampaign()
        
        # The client_id may be used to associate records in the bulk upload file with records in the results file. The value of this field  
        # is not used or stored by the server; it is simply copied from the uploaded record to the corresponding result record. 
        # Note: This bulk file Client Id is not related to an application Client Id for OAuth. 
        
        bulk_campaign.client_id='YourClientIdGoesHere'
        campaign=set_elements_to_none(campaign_service.factory.create('Campaign'))
        
        # When using the Campaign Management service, the Id cannot be set. In the context of a BulkCampaign, the Id is optional  
        # and may be used as a negative reference key during bulk upload. For example the same negative reference key for the campaign Id  
        # will be used when adding new ad groups to this new campaign, or when associating ad extensions with the campaign. 

        campaign.Id=CAMPAIGN_ID_KEY
        campaign.Name="Summer Shoes " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        campaign.Description="Summer shoes line."

        # You must choose to set either the shared  budget ID or daily amount.
        # You can set one or the other, but you may not set both.
        campaign.BudgetId=BUDGET_ID_KEY
        campaign.DailyBudget=None
        campaign.BudgetType=None
        
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

        bulk_campaign.campaign=campaign

        bulk_ad_group=BulkAdGroup()
        bulk_ad_group.campaign_id=CAMPAIGN_ID_KEY
        ad_group=set_elements_to_none(campaign_service.factory.create('AdGroup'))
        ad_group.Id=AD_GROUP_ID_KEY
        ad_group.Name="Women's Red Shoes"
        ad_group.AdDistribution='Search'
        end_date=campaign_service.factory.create('Date')
        end_date.Day=31
        end_date.Month=12
        end_date.Year=strftime("%Y", gmtime())
        ad_group.EndDate=end_date
        search_bid=campaign_service.factory.create('Bid')
        search_bid.Amount=0.09
        ad_group.SearchBid=search_bid
        ad_group.Language='English'

        # For ad groups you can use either of the InheritFromParentBiddingScheme or ManualCpcBiddingScheme objects. 
        # If you do not set this element, then InheritFromParentBiddingScheme is used by default.
        ad_group_bidding_scheme=set_elements_to_none(campaign_service.factory.create('ManualCpcBiddingScheme'))
        ad_group.BiddingScheme=ad_group_bidding_scheme

        # You could use a tracking template which would override the campaign level
        # tracking template. Tracking templates defined for lower level entities 
        # override those set for higher level entities.
        # In this example we are using the campaign level tracking template.
        ad_group.TrackingUrlTemplate=None

        bulk_ad_group.ad_group=ad_group

        # In this example only the first 3 ads should succeed. 
        # The Title of the fourth ad is empty and not valid,
        # and the fifth ad is a duplicate of the second ad 

        bulk_expanded_text_ads=[]

        for index in range(5):
            bulk_expanded_text_ad=BulkExpandedTextAd()
            bulk_expanded_text_ad.ad_group_id=AD_GROUP_ID_KEY
            expanded_text_ad=set_elements_to_none(campaign_service.factory.create('ExpandedTextAd'))
            expanded_text_ad.TitlePart1='Contoso'
            expanded_text_ad.TitlePart2='Fast & Easy Setup'
            expanded_text_ad.Text='Huge Savings on red shoes.'
            expanded_text_ad.Path1='seattle'
            expanded_text_ad.Path2='shoe sale'
            expanded_text_ad.Type='ExpandedText'
            expanded_text_ad.Status=None
            expanded_text_ad.EditorialStatus=None
            
            # With FinalUrls you can separate the tracking template, custom parameters, and 
            # landing page URLs.
            final_urls=campaign_service.factory.create('ns4:ArrayOfstring')
            final_urls.string.append('http://www.contoso.com/womenshoesale')
            expanded_text_ad.FinalUrls=final_urls

            # Final Mobile URLs can also be used if you want to direct the user to a different page 
            # for mobile devices.
            final_mobile_urls=campaign_service.factory.create('ns4:ArrayOfstring')
            final_mobile_urls.string.append('http://mobile.contoso.com/womenshoesale')
            expanded_text_ad.FinalMobileUrls=final_mobile_urls

            # You could use a tracking template which would override the campaign level
            # tracking template. Tracking templates defined for lower level entities 
            # override those set for higher level entities.
            # In this example we are using the campaign level tracking template.
            expanded_text_ad.TrackingUrlTemplate=None

            # Set custom parameters that are specific to this ad, 
            # and can be used by the ad, ad group, campaign, or account level tracking template. 
            # In this example we are using the campaign level tracking template.
            url_custom_parameters=campaign_service.factory.create('ns0:CustomParameters')
            parameters=campaign_service.factory.create('ns0:ArrayOfCustomParameter')
            custom_parameter1=campaign_service.factory.create('ns0:CustomParameter')
            custom_parameter1.Key='promoCode'
            custom_parameter1.Value='PROMO' + str(index)
            parameters.CustomParameter.append(custom_parameter1)
            custom_parameter2=campaign_service.factory.create('ns0:CustomParameter')
            custom_parameter2.Key='season'
            custom_parameter2.Value='summer'
            parameters.CustomParameter.append(custom_parameter2)
            url_custom_parameters.Parameters=parameters
            expanded_text_ad.UrlCustomParameters=url_custom_parameters
            bulk_expanded_text_ad.ad=expanded_text_ad
            bulk_expanded_text_ads.append(bulk_expanded_text_ad)

        bulk_expanded_text_ads[1].ad.Title="Quick & Easy Setup"
        bulk_expanded_text_ads[2].ad.Title="Fast & Simple Setup"
        bulk_expanded_text_ads[3].ad.Title=''
        bulk_expanded_text_ads[4].ad.Title="Quick & Easy Setup"

        # In this example only the second keyword should succeed. The Text of the first keyword exceeds the limit,
        # and the third keyword is a duplicate of the second keyword.

        bulk_keywords=[]

        for index in range(3):
            bulk_keyword=BulkKeyword()
            bulk_keyword.ad_group_id=AD_GROUP_ID_KEY
            keyword=set_elements_to_none(campaign_service.factory.create('Keyword'))
            keyword.Bid=set_elements_to_none(campaign_service.factory.create('Bid'))
            keyword.Bid.Amount=0.47
            keyword.Param2='10% Off'
            keyword.MatchType='Broad'
            keyword.Text='Brand-A Shoes'

            # For keywords you can use either of the InheritFromParentBiddingScheme or ManualCpcBiddingScheme objects. 
            # If you do not set this element, then InheritFromParentBiddingScheme is used by default.
            keyword_bidding_scheme=set_elements_to_none(campaign_service.factory.create('InheritFromParentBiddingScheme'))
            keyword.BiddingScheme=keyword_bidding_scheme

            bulk_keyword.keyword=keyword
            bulk_keywords.append(bulk_keyword)

        bulk_keywords[0].keyword.Text=(
            "Brand-A Shoes Brand-A Shoes Brand-A Shoes Brand-A Shoes Brand-A Shoes "
		    "Brand-A Shoes Brand-A Shoes Brand-A Shoes Brand-A Shoes Brand-A Shoes "
		    "Brand-A Shoes Brand-A Shoes Brand-A Shoes Brand-A Shoes Brand-A Shoes"
        )

        # Write the entities created above, to temporary memory. 
        # Dependent entities such as BulkKeyword must be written after any dependencies,   
        # for example the BulkCampaign and BulkAdGroup. 

        upload_entities.append(bulk_campaign)
        upload_entities.append(bulk_ad_group)
        for bulk_expanded_text_ad in bulk_expanded_text_ads:
            upload_entities.append(bulk_expanded_text_ad)
        for bulk_keyword in bulk_keywords:
            upload_entities.append(bulk_keyword)      
        
        output_status_message("\nAdding campaign, budget, ad group, keywords, and ads . . .")
        download_entities=write_entities_and_upload_file(bulk_service_manager, upload_entities)

        budget_results=[]
        campaign_results=[]
        adgroup_results=[]
        keyword_results=[]

        for entity in download_entities:
            if isinstance(entity, BulkBudget):
                budget_results.append(entity)
                output_bulk_budgets([entity])
            if isinstance(entity, BulkCampaign):
                campaign_results.append(entity)
                output_bulk_campaigns([entity])
            if isinstance(entity, BulkAdGroup):
                adgroup_results.append(entity)
                output_bulk_ad_groups([entity])
            if isinstance(entity, BulkExpandedTextAd):
                output_bulk_expanded_text_ads([entity])
            if isinstance(entity, BulkKeyword):
                keyword_results.append(entity)
                output_bulk_keywords([entity])


        # Here is a simple example that updates the keyword bid to use the ad group bid.

        update_bulk_keyword=BulkKeyword()
        update_bulk_keyword.ad_group_id=adgroup_results[0].ad_group.Id
        update_keyword=campaign_service.factory.create('Keyword')

        update_keyword.Id=next((keyword_result.keyword.Id for keyword_result in keyword_results if 
                                keyword_result.keyword.Id is not None and keyword_result.ad_group_id==update_bulk_keyword.ad_group_id), None)

        # You can set the Bid.Amount property to change the keyword level bid.
        update_keyword.Bid=campaign_service.factory.create('Bid')
        update_keyword.Bid.Amount=0.46

        # The keyword bid will not be updated if the Bid property is not specified or if you create
        # an empty Bid.
        #update_keyword.Bid=campaign_service.factory.create('Bid')
        
        # The keyword level bid will be deleted ("delete_value" will be written in the bulk upload file), and
        # the keyword will effectively inherit the ad group level bid if you explicitly set the Bid property to None. 
        #update_keyword.Bid=None

        # It is important to note that the above behavior differs from the Bid settings that
        # are used to update keywords with the Campaign Management servivce.
        # When using the Campaign Management service with the Bing Ads Python SDK, if the 
        # Bid property is not specified or is set explicitly to None, your keyword bid will not be updated.
        # For examples of how to use the Campaign Management service for keyword updates, please see KeywordsAds.py.
                
        update_bulk_keyword.keyword=update_keyword

        upload_entities=[]

        upload_entities.append(update_bulk_keyword)
                   
        output_status_message("\nUpdating the keyword bid to use the ad group bid . . .")
        download_entities=write_entities_and_upload_file(bulk_service_manager, upload_entities)

        for entity in download_entities:
            if isinstance(entity, BulkKeyword):
                output_bulk_keywords([entity])

        # Here is a simple example that updates the campaign budget.
        
        download_parameters=DownloadParameters(
            download_entities=[
                'Budgets',
                'Campaigns'
            ],
            result_file_directory=FILE_DIRECTORY,
            result_file_name=DOWNLOAD_FILE_NAME,
            overwrite_result_file=True,
            last_sync_time_in_utc=None
        )

        upload_entities=[]
        get_budget_results=[]
        get_campaign_results=[]

        # Download all campaigns and shared budgets in the account.
        download_entities=download_file(bulk_service_manager, download_parameters)
        output_status_message("Downloaded all campaigns and shared budgets in the account.\n")
        for entity in download_entities:
            if isinstance(entity, BulkBudget):
                get_budget_results.append(entity)
                output_bulk_budgets([entity])
            if isinstance(entity, BulkCampaign):
                get_campaign_results.append(entity)
                output_bulk_campaigns([entity])
        
        # If the campaign has a shared budget you cannot update the Campaign budget amount,
        # and you must instead update the amount in the Budget record. If you try to update 
        # the budget amount of a Campaign that has a shared budget, the service will return 
        # the CampaignServiceCannotUpdateSharedBudget error code.
        for entity in get_budget_results:
            if entity.budget.Id > 0:
                # Increase budget by 20 %
                entity.budget.Amount *= Decimal(1.2)
                upload_entities.append(entity)
        
        for entity in get_campaign_results:
            if entity.campaign.BudgetId == None or entity.campaign.BudgetId <= 0:
                # Increase budget by 20 %
                entity.campaign.DailyBudget *= 1.2
                upload_entities.append(entity)
                    
        if len(upload_entities) > 0:
            output_status_message("Changed local campaign budget amounts. Starting upload.\n")

            download_entities=write_entities_and_upload_file(bulk_service_manager, upload_entities)       
            for entity in download_entities:
                if isinstance(entity, BulkBudget):
                    get_budget_results.append(entity)
                    output_bulk_budgets([entity])
                if isinstance(entity, BulkCampaign):
                    get_campaign_results.append(entity)
                    output_bulk_campaigns([entity])
        else:
            output_status_message("No campaigns or shared budgets in account.\n")

        # Delete the campaign, ad group, keywords, and ads that were previously added. 
        # You should remove this region if you want to view the added entities in the 
        # Bing Ads web application or another tool.
                
        upload_entities=[]

        for budget_result in budget_results:
            budget_result.status='Deleted'
            upload_entities.append(budget_result)

        for campaign_result in campaign_results:
            campaign_result.campaign.Status='Deleted'
            upload_entities.append(campaign_result)
            
        output_status_message("\nDeleting campaign, budget, ad group, ads, and keywords . . .")
        download_entities=write_entities_and_upload_file(bulk_service_manager, upload_entities)

        for entity in download_entities:
            if isinstance(entity, BulkBudget):
                output_bulk_budgets([entity])
            if isinstance(entity, BulkCampaign):
                output_bulk_campaigns([entity])
            
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

    bulk_service_manager=BulkServiceManager(
        authorization_data=authorization_data, 
        poll_interval_in_milliseconds=5000, 
        environment=ENVIRONMENT,
    )

    campaign_service=ServiceClient(
        service='CampaignManagementService', 
        authorization_data=authorization_data, 
        environment=ENVIRONMENT,
        version=11,
    )

    # You should authenticate for Bing Ads production services with a Microsoft Account, 
    # instead of providing the Bing Ads username and password set. 
            
    authenticate(authorization_data)
        
    main(authorization_data)
