from auth_helper import *
from bulk_helper import *
from output_helper import *

# You must provide credentials in auth_helper.py.

def main(authorization_data):

    errors=[]

    try:
        # To prepare for the sitelink ad extensions migration by the end of September 2017, you will need 
        # to determine whether the account has been migrated from SiteLinksAdExtension to Sitelink2AdExtension. 
        # All ad extension service operations available for both types of sitelinks; however you will 
        # need to determine which type to add, update, and retrieve.

        SITELINK_MIGRATION = 'SiteLinkAdExtension'
        sitelink_migration_is_completed = False

        # Optionally you can find out which pilot features the customer is able to use. Even if the customer 
        # is in pilot for sitelink migrations, the accounts that it contains might not be migrated.
        feature_pilot_flags = customer_service.GetCustomerPilotFeatures(authorization_data.customer_id)

        # The pilot flag value for Sitelink ad extension migration is 253.
        # Pilot flags apply to all accounts within a given customer; however,
        # each account goes through migration individually and has its own migration status.
        if(253 in feature_pilot_flags['int']):
            # Account migration status below will be either NotStarted, InProgress, or Completed.
            output_status_message("Customer is in pilot for Sitelink migration.\n")
        else:
            # Account migration status below will be NotInPilot.
            output_status_message("Customer is not in pilot for Sitelink migration.\n")
        
        # Even if you have multiple accounts per customer, each account will have its own
        # migration status. This example checks one account using the provided AuthorizationData.
        account_migration_statuses_infos = campaign_service.GetAccountMigrationStatuses(
            {'long': authorization_data.account_id},
            SITELINK_MIGRATION
        )

        for account_migration_statuses_info in account_migration_statuses_infos['AccountMigrationStatusesInfo']:
            output_account_migration_statuses_info(account_migration_statuses_info)
            for migration_status_info in account_migration_statuses_info['MigrationStatusInfo']:
                if migration_status_info[1][0].Status == 'Completed' and SITELINK_MIGRATION == migration_status_info[1][0].MigrationType: 
                    sitelink_migration_is_completed = True
        
        
        # Prepare the bulk entities that you want to upload. Each bulk entity contains the corresponding campaign management object,  
        # and additional elements needed to read from and write to a bulk file.

        bulk_campaign=BulkCampaign()
    
        # The client_id may be used to associate records in the bulk upload file with records in the results file. The value of this field  
        # is not used or stored by the server; it is simply copied from the uploaded record to the corresponding result record. 
        # Note: This bulk file Client Id is not related to an application Client Id for OAuth. 

        bulk_campaign.client_id='YourClientIdGoesHere'
        campaign=set_elements_to_none(campaign_service.factory.create('Campaign'))
    
        # When using the Campaign Management service, the Id cannot be set. In the context of a BulkCampaign, the Id is optional  
        # and may be used as a negative reference key during bulk upload. For example the same negative reference key for the campaign Id  
        # will be used when associating ad extensions with the campaign. 

        campaign.Id=CAMPAIGN_ID_KEY
        campaign.Name="Summer Shoes " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        campaign.Description="Summer shoes line."
        campaign.BudgetType='DailyBudgetStandard'
        campaign.DailyBudget=10
        campaign.TimeZone='PacificTimeUSCanadaTijuana'
        campaign.Status='Paused'

        # Used with FinalUrls shown in the sitelinks that we will add below.
        campaign.TrackingUrlTemplate="http://tracker.example.com/?season={_season}&promocode={_promocode}&u={lpurl}"

        bulk_campaign.campaign=campaign

        bulk_app_ad_extension=BulkAppAdExtension()
        bulk_app_ad_extension.account_id=authorization_data.account_id
        app_ad_extension=set_elements_to_none(campaign_service.factory.create('AppAdExtension'))
        app_ad_extension.Id=APP_AD_EXTENSION_ID_KEY
        app_ad_extension.AppPlatform='Windows'
        app_ad_extension.AppStoreId='AppStoreIdGoesHere'
        app_ad_extension.DisplayText='Contoso'
        app_ad_extension.DestinationUrl='DestinationUrlGoesHere'
        app_ad_extension.Status=None
        bulk_app_ad_extension.app_ad_extension=app_ad_extension

        bulk_campaign_app_ad_extension=BulkCampaignAppAdExtension()
        app_ad_extension_id_to_entity_id_association=campaign_service.factory.create('AdExtensionIdToEntityIdAssociation')
        app_ad_extension_id_to_entity_id_association.AdExtensionId=APP_AD_EXTENSION_ID_KEY
        app_ad_extension_id_to_entity_id_association.EntityId=CAMPAIGN_ID_KEY
        bulk_campaign_app_ad_extension.ad_extension_id_to_entity_id_association=app_ad_extension_id_to_entity_id_association

        bulk_call_ad_extension=BulkCallAdExtension()
        bulk_call_ad_extension.account_id=authorization_data.account_id
        call_ad_extension=set_elements_to_none(campaign_service.factory.create('CallAdExtension'))
        call_ad_extension.CountryCode="US"
        call_ad_extension.PhoneNumber="2065550100"
        call_ad_extension.IsCallOnly=False
        call_ad_extension.Status=None
        # For this example assume the call center is open Monday - Friday from 9am - 9pm
        # in the account's time zone.
        call_scheduling=set_elements_to_none(campaign_service.factory.create('Schedule'))
        call_day_time_ranges=campaign_service.factory.create('ArrayOfDayTime')
        call_monday=set_elements_to_none(campaign_service.factory.create('DayTime'))
        call_monday.Day='Monday'
        call_monday.StartHour=9
        call_monday.StartMinute='Zero'
        call_monday.EndHour=21
        call_monday.EndMinute='Zero'
        call_day_time_ranges.DayTime.append(call_monday)
        call_tuesday=set_elements_to_none(campaign_service.factory.create('DayTime'))
        call_tuesday.Day='Tuesday'
        call_tuesday.StartHour=9
        call_tuesday.StartMinute='Zero'
        call_tuesday.EndHour=21
        call_tuesday.EndMinute='Zero'
        call_day_time_ranges.DayTime.append(call_tuesday)
        call_wednesday=set_elements_to_none(campaign_service.factory.create('DayTime'))
        call_wednesday.Day='Wednesday'
        call_wednesday.StartHour=9
        call_wednesday.StartMinute='Zero'
        call_wednesday.EndHour=21
        call_wednesday.EndMinute='Zero'
        call_day_time_ranges.DayTime.append(call_wednesday)
        call_thursday=set_elements_to_none(campaign_service.factory.create('DayTime'))
        call_thursday.Day='Thursday'
        call_thursday.StartHour=9
        call_thursday.StartMinute='Zero'
        call_thursday.EndHour=21
        call_thursday.EndMinute='Zero'
        call_day_time_ranges.DayTime.append(call_thursday)
        call_friday=set_elements_to_none(campaign_service.factory.create('DayTime'))
        call_friday.Day='Friday'
        call_friday.StartHour=9
        call_friday.StartMinute='Zero'
        call_friday.EndHour=21
        call_friday.EndMinute='Zero'
        call_day_time_ranges.DayTime.append(call_friday)
        call_scheduling.DayTimeRanges=call_day_time_ranges
        call_scheduling_end_date=campaign_service.factory.create('Date')
        call_scheduling_end_date.Day=31
        call_scheduling_end_date.Month=12
        call_scheduling_end_date.Year=strftime("%Y", gmtime())
        call_scheduling.EndDate=call_scheduling_end_date
        call_scheduling.StartDate=None
        call_ad_extension.Scheduling=call_scheduling
        call_ad_extension.Id=CALL_AD_EXTENSION_ID_KEY
        bulk_call_ad_extension.call_ad_extension=call_ad_extension

        bulk_campaign_call_ad_extension=BulkCampaignCallAdExtension()
        call_ad_extension_id_to_entity_id_association=campaign_service.factory.create('AdExtensionIdToEntityIdAssociation')
        call_ad_extension_id_to_entity_id_association.AdExtensionId=CALL_AD_EXTENSION_ID_KEY
        call_ad_extension_id_to_entity_id_association.EntityId=CAMPAIGN_ID_KEY
        bulk_campaign_call_ad_extension.ad_extension_id_to_entity_id_association=call_ad_extension_id_to_entity_id_association

        bulk_callout_ad_extension=BulkCalloutAdExtension()
        bulk_callout_ad_extension.account_id=authorization_data.account_id
        callout_ad_extension=set_elements_to_none(campaign_service.factory.create('CalloutAdExtension'))
        callout_ad_extension.Text="Callout Text"
        callout_ad_extension.Status=None
        callout_ad_extension.Id=CALLOUT_AD_EXTENSION_ID_KEY
        bulk_callout_ad_extension.callout_ad_extension=callout_ad_extension

        bulk_campaign_callout_ad_extension=BulkCampaignCalloutAdExtension()
        callout_ad_extension_id_to_entity_id_association=campaign_service.factory.create('AdExtensionIdToEntityIdAssociation')
        callout_ad_extension_id_to_entity_id_association.AdExtensionId=CALLOUT_AD_EXTENSION_ID_KEY
        callout_ad_extension_id_to_entity_id_association.EntityId=CAMPAIGN_ID_KEY
        bulk_campaign_callout_ad_extension.ad_extension_id_to_entity_id_association=callout_ad_extension_id_to_entity_id_association

        bulk_location_ad_extension=BulkLocationAdExtension()
        bulk_location_ad_extension.account_id=authorization_data.account_id
        location_ad_extension=set_elements_to_none(campaign_service.factory.create('LocationAdExtension'))
        location_ad_extension.PhoneNumber="206-555-0100"
        location_ad_extension.CompanyName="Contoso Shoes"
        location_ad_extension.IconMediaId=None
        location_ad_extension.ImageMediaId=None
        location_ad_extension.Status=None
        location_ad_extension.GeoCodeStatus=None
        location_ad_extension.GeoPoint=None
        address=campaign_service.factory.create('Address')
        address.StreetAddress="1234 Washington Place"
        address.StreetAddress2="Suite 1210"
        address.CityName="Woodinville"
        address.ProvinceName="WA"
        address.CountryCode="US"
        address.PostalCode="98608"
        location_ad_extension.Address=address
        location_scheduling=set_elements_to_none(campaign_service.factory.create('Schedule'))
        location_day_time_ranges=campaign_service.factory.create('ArrayOfDayTime')
        location_day_time=set_elements_to_none(campaign_service.factory.create('DayTime'))
        location_day_time.Day='Saturday'
        location_day_time.StartHour=9
        location_day_time.StartMinute='Zero'
        location_day_time.EndHour=12
        location_day_time.EndMinute='Zero'
        location_day_time_ranges.DayTime.append(location_day_time)
        location_scheduling.DayTimeRanges=location_day_time_ranges
        location_scheduling_end_date=campaign_service.factory.create('Date')
        location_scheduling_end_date.Day=31
        location_scheduling_end_date.Month=12
        location_scheduling_end_date.Year=strftime("%Y", gmtime())
        location_scheduling.EndDate=location_scheduling_end_date
        location_scheduling.StartDate=None
        location_ad_extension.Scheduling=location_scheduling
        location_ad_extension.Id=LOCATION_AD_EXTENSION_ID_KEY
        bulk_location_ad_extension.location_ad_extension=location_ad_extension

        bulk_campaign_location_ad_extension=BulkCampaignLocationAdExtension()
        location_ad_extension_id_to_entity_id_association=campaign_service.factory.create('AdExtensionIdToEntityIdAssociation')
        location_ad_extension_id_to_entity_id_association.AdExtensionId=LOCATION_AD_EXTENSION_ID_KEY
        location_ad_extension_id_to_entity_id_association.EntityId=CAMPAIGN_ID_KEY
        bulk_campaign_location_ad_extension.ad_extension_id_to_entity_id_association=location_ad_extension_id_to_entity_id_association

        bulk_review_ad_extension=BulkReviewAdExtension()
        bulk_review_ad_extension.account_id=authorization_data.account_id
        review_ad_extension=set_elements_to_none(campaign_service.factory.create('ReviewAdExtension'))
        review_ad_extension.IsExact=True
        review_ad_extension.Source="Review Source Name"
        review_ad_extension.Text="Review Text"
        review_ad_extension.Url="http://review.contoso.com" # The Url of the third-party review. This is not your business Url.
        review_ad_extension.Status=None
        review_ad_extension.Id=REVIEW_AD_EXTENSION_ID_KEY
        bulk_review_ad_extension.review_ad_extension=review_ad_extension

        bulk_campaign_review_ad_extension=BulkCampaignReviewAdExtension()
        review_ad_extension_id_to_entity_id_association=campaign_service.factory.create('AdExtensionIdToEntityIdAssociation')
        review_ad_extension_id_to_entity_id_association.AdExtensionId=REVIEW_AD_EXTENSION_ID_KEY
        review_ad_extension_id_to_entity_id_association.EntityId=CAMPAIGN_ID_KEY
        bulk_campaign_review_ad_extension.ad_extension_id_to_entity_id_association=review_ad_extension_id_to_entity_id_association

        bulk_structured_snippet_ad_extension=BulkStructuredSnippetAdExtension()
        bulk_structured_snippet_ad_extension.account_id=authorization_data.account_id
        structured_snippet_ad_extension=set_elements_to_none(campaign_service.factory.create('StructuredSnippetAdExtension'))
        structured_snippet_ad_extension.Header = "Brands"
        values=campaign_service.factory.create('ns4:ArrayOfstring')
        values.string.append('Windows')
        values.string.append('Xbox')
        values.string.append('Skype')
        structured_snippet_ad_extension.Values=values
        structured_snippet_ad_extension.Id=STRUCTURED_SNIPPET_AD_EXTENSION_ID_KEY
        bulk_structured_snippet_ad_extension.structured_snippet_ad_extension=structured_snippet_ad_extension

        bulk_campaign_structured_snippet_ad_extension=BulkCampaignStructuredSnippetAdExtension()
        structured_snippet_ad_extension_id_to_entity_id_association=campaign_service.factory.create('AdExtensionIdToEntityIdAssociation')
        structured_snippet_ad_extension_id_to_entity_id_association.AdExtensionId=STRUCTURED_SNIPPET_AD_EXTENSION_ID_KEY
        structured_snippet_ad_extension_id_to_entity_id_association.EntityId=CAMPAIGN_ID_KEY
        bulk_campaign_structured_snippet_ad_extension.ad_extension_id_to_entity_id_association=structured_snippet_ad_extension_id_to_entity_id_association

        
        # Upload the entities created above. 
        # Dependent entities such as BulkCampaignCallAdExtension must be written after any dependencies,  
        # for example the BulkCampaign and BulkCallAdExtension. 

        upload_entities=[]
        upload_entities.append(bulk_campaign)
        upload_entities.append(bulk_app_ad_extension)
        upload_entities.append(bulk_campaign_app_ad_extension)
        upload_entities.append(bulk_call_ad_extension)
        upload_entities.append(bulk_campaign_call_ad_extension)
        upload_entities.append(bulk_callout_ad_extension)
        upload_entities.append(bulk_campaign_callout_ad_extension)
        upload_entities.append(bulk_location_ad_extension)
        upload_entities.append(bulk_campaign_location_ad_extension)
        upload_entities.append(bulk_review_ad_extension)
        upload_entities.append(bulk_campaign_review_ad_extension)
        upload_entities.append(bulk_structured_snippet_ad_extension)
        upload_entities.append(bulk_campaign_structured_snippet_ad_extension)

        if sitelink_migration_is_completed:
            for entity in get_sample_bulk_sitelink2_ad_extensions(authorization_data.account_id):
                upload_entities.append(entity)
        else:
            for entity in get_sample_bulk_site_links_ad_extensions(authorization_data.account_id):
                upload_entities.append(entity)

        output_status_message("\nAdding campaign, ad extensions, and associations . . .")
        download_entities=write_entities_and_upload_file(bulk_service_manager, upload_entities)

        campaign_results=[]
        app_ad_extension_results=[]
        call_ad_extension_results=[]
        callout_ad_extension_results=[]
        location_ad_extension_results=[]
        review_ad_extension_results=[]
        site_link_ad_extension_results=[]
        sitelink2_ad_extension_results=[]
        structured_snippet_ad_extension_results=[]

        for entity in download_entities:
            if isinstance(entity, BulkCampaign):
                campaign_results.append(entity)
                output_bulk_campaigns([entity])
            if isinstance(entity, BulkAppAdExtension):
                app_ad_extension_results.append(entity)
                output_bulk_app_ad_extensions([entity])
            if isinstance(entity, BulkCampaignAppAdExtension):
                output_bulk_campaign_app_ad_extensions([entity])
            if isinstance(entity, BulkCallAdExtension):
                call_ad_extension_results.append(entity)
                output_bulk_call_ad_extensions([entity])
            if isinstance(entity, BulkCampaignCallAdExtension):
                output_bulk_campaign_call_ad_extensions([entity])
            if isinstance(entity, BulkCalloutAdExtension):
                callout_ad_extension_results.append(entity)
                output_bulk_callout_ad_extensions([entity])
            if isinstance(entity, BulkCampaignCalloutAdExtension):
                output_bulk_campaign_callout_ad_extensions([entity])
            if isinstance(entity, BulkLocationAdExtension):
                location_ad_extension_results.append(entity)
                output_bulk_location_ad_extensions([entity])
            if isinstance(entity, BulkCampaignLocationAdExtension):
                output_bulk_campaign_location_ad_extensions([entity])
            if isinstance(entity, BulkReviewAdExtension):
                review_ad_extension_results.append(entity)
                output_bulk_review_ad_extensions([entity])
            if isinstance(entity, BulkCampaignReviewAdExtension):
                output_bulk_campaign_review_ad_extensions([entity])
            if isinstance(entity, BulkSiteLinkAdExtension):
                site_link_ad_extension_results.append(entity)
                output_bulk_site_link_ad_extensions([entity])
            if isinstance(entity, BulkCampaignSiteLinkAdExtension):
                output_bulk_campaign_site_link_ad_extensions([entity])
            if isinstance(entity, BulkSitelink2AdExtension):
                sitelink2_ad_extension_results.append(entity)
                output_bulk_sitelink2_ad_extensions([entity])
            if isinstance(entity, BulkCampaignSitelink2AdExtension):
                output_bulk_campaign_sitelink2_ad_extensions([entity])
            if isinstance(entity, BulkStructuredSnippetAdExtension):
                structured_snippet_ad_extension_results.append(entity)
                output_bulk_structured_snippet_ad_extensions([entity])
            if isinstance(entity, BulkCampaignStructuredSnippetAdExtension):
                output_bulk_campaign_structured_snippet_ad_extensions([entity])
            
              
        # Use only the location extension results and remove scheduling.

        upload_entities=[]
        
        for location_ad_extension_result in location_ad_extension_results:
            if location_ad_extension_result.location_ad_extension.Id > 0:
                # If you set the Scheduling element null, any existing scheduling set for the ad extension will remain unchanged. 
                # If you set this to any non-null Schedule object, you are effectively replacing existing scheduling 
                # for the ad extension. In this example, we will remove any existing scheduling by setting this element  
                # to an empty Schedule object.
                location_ad_extension_result.location_ad_extension.Scheduling=set_elements_to_none(campaign_service.factory.create('Schedule'))
                upload_entities.append(location_ad_extension_result);
            
        # Upload and write the output

        output_status_message("\nRemoving scheduling from location ad extensions . . .\n")
        download_entities=write_entities_and_upload_file(bulk_service_manager, upload_entities)
        
        for entity in download_entities:
            if isinstance(entity, BulkLocationAdExtension):
                output_bulk_location_ad_extensions([entity])

        # Delete the campaign and ad extensions that were previously added. 
        # You should remove this region if you want to view the added entities in the 
        # Bing Ads web application or another tool.

        # You must set the Id field to the corresponding entity identifier, and the Status field to Deleted. 

        # When you delete a BulkCampaign or BulkCallAdExtension, dependent entities such as BulkCampaignCallAdExtension 
        # are deleted without being specified explicitly.  

        upload_entities=[]

        for campaign_result in campaign_results:
            campaign_result.campaign.Status='Deleted'
            upload_entities.append(campaign_result)
        
        for app_ad_extension_result in app_ad_extension_results:
            app_ad_extension_result.app_ad_extension.Status='Deleted'
            # By default the sample does not successfully create any app ad extensions,
            # because you need to provide details such as the AppStoreId.
            # You can uncomment the following line if you added an app ad extension above.
            # upload_entities.append(app_ad_extension_result)

        for call_ad_extension_result in call_ad_extension_results:
            call_ad_extension_result.call_ad_extension.Status='Deleted'
            upload_entities.append(call_ad_extension_result)

        for callout_ad_extension_result in callout_ad_extension_results:
            callout_ad_extension_result.callout_ad_extension.Status='Deleted'
            upload_entities.append(callout_ad_extension_result)

        for location_ad_extension_result in location_ad_extension_results:
            location_ad_extension_result.location_ad_extension.Status='Deleted'
            upload_entities.append(location_ad_extension_result)

        for review_ad_extension_result in review_ad_extension_results:
            review_ad_extension_result.review_ad_extension.Status='Deleted'
            upload_entities.append(review_ad_extension_result)

        for site_link_ad_extension_result in site_link_ad_extension_results:
            site_link_ad_extension_result.site_links_ad_extension.Status='Deleted'
            upload_entities.append(site_link_ad_extension_result)

        for sitelink2_ad_extension_result in sitelink2_ad_extension_results:
            sitelink2_ad_extension_result.sitelink2_ad_extension.Status='Deleted'
            upload_entities.append(sitelink2_ad_extension_result)

        for structured_snippet_ad_extension_result in structured_snippet_ad_extension_results:
            structured_snippet_ad_extension_result.structured_snippet_ad_extension.Status='Deleted'
            upload_entities.append(structured_snippet_ad_extension_result)

        output_status_message("\nDeleting campaign and ad extensions . . .")
        download_entities=write_entities_and_upload_file(bulk_service_manager, upload_entities)

        for entity in download_entities:
            if isinstance(entity, BulkCampaign):
                output_bulk_campaigns([entity])
            if isinstance(entity, BulkAppAdExtension):
                output_bulk_app_ad_extensions([entity])
            if isinstance(entity, BulkCallAdExtension):
                output_bulk_call_ad_extensions([entity])
            if isinstance(entity, BulkCalloutAdExtension):
                output_bulk_callout_ad_extensions([entity])
            if isinstance(entity, BulkLocationAdExtension):
                output_bulk_location_ad_extensions([entity])
            if isinstance(entity, BulkReviewAdExtension):
                output_bulk_review_ad_extensions([entity])
            if isinstance(entity, BulkSiteLinkAdExtension):
                output_bulk_site_link_ad_extensions([entity])
            if isinstance(entity, BulkSitelink2AdExtension):
                output_bulk_sitelink2_ad_extensions([entity])
            if isinstance(entity, BulkStructuredSnippetAdExtension):
                output_bulk_structured_snippet_ad_extensions([entity])

        output_status_message("Program execution completed")

    except WebFault as ex:
        output_webfault_errors(ex)
    except Exception as ex:
        output_status_message(ex)

def get_sample_bulk_sitelink2_ad_extensions(account_id):
    entities=[]

    for index in range(2):
        bulk_sitelink2_ad_extension=BulkSitelink2AdExtension()
        bulk_sitelink2_ad_extension.account_id=account_id
        sitelink2_ad_extension=set_elements_to_none(campaign_service.factory.create('Sitelink2AdExtension'))
        sitelink2_ad_extension.Description1="Simple & Transparent."
        sitelink2_ad_extension.Description2="No Upfront Cost."
        sitelink2_ad_extension.DisplayText = "Women's Shoe Sale " + str(index+1)

        # If you are currently using the Destination URL, you must upgrade to Final URLs. 
        # Here is an example of a DestinationUrl you might have used previously. 
        # sitelink2_ad_extension.DestinationUrl='http://www.contoso.com/womenshoesale/?season=spring&promocode=PROMO123'

        # To migrate from DestinationUrl to FinalUrls, you can set DestinationUrl
        # to an empty string when updating the ad extension. If you are removing DestinationUrl,
        # then FinalUrls is required.
        # sitelink2_ad_extension.DestinationUrl=""
            
        # With FinalUrls you can separate the tracking template, custom parameters, and 
        # landing page URLs.
        final_urls=campaign_service.factory.create('ns4:ArrayOfstring')
        final_urls.string.append('http://www.contoso.com/womenshoesale')
        sitelink2_ad_extension.FinalUrls=final_urls

        # Final Mobile URLs can also be used if you want to direct the user to a different page 
        # for mobile devices.
        final_mobile_urls=campaign_service.factory.create('ns4:ArrayOfstring')
        final_mobile_urls.string.append('http://mobile.contoso.com/womenshoesale')
        sitelink2_ad_extension.FinalMobileUrls=final_mobile_urls

        # You could use a tracking template which would override the campaign level
        # tracking template. Tracking templates defined for lower level entities 
        # override those set for higher level entities.
        # In this example we are using the campaign level tracking template.
        sitelink2_ad_extension.TrackingUrlTemplate=None

        # Set custom parameters that are specific to this ad extension, 
        # and can be used by the ad extension, ad group, campaign, or account level tracking template. 
        # In this example we are using the campaign level tracking template.
        url_custom_parameters=campaign_service.factory.create('ns0:CustomParameters')
        parameters=campaign_service.factory.create('ns0:ArrayOfCustomParameter')
        custom_parameter1=campaign_service.factory.create('ns0:CustomParameter')
        custom_parameter1.Key='promoCode'
        custom_parameter1.Value='PROMO' + str(index+1)
        parameters.CustomParameter.append(custom_parameter1)
        custom_parameter2=campaign_service.factory.create('ns0:CustomParameter')
        custom_parameter2.Key='season'
        custom_parameter2.Value='summer'
        parameters.CustomParameter.append(custom_parameter2)
        url_custom_parameters.Parameters=parameters
        sitelink2_ad_extension.UrlCustomParameters=url_custom_parameters

        sitelink2_ad_extension.Status=None
        sitelink2_ad_extension.Id=SITELINK2_AD_EXTENSION_ID_KEY
        bulk_sitelink2_ad_extension.sitelink2_ad_extension=sitelink2_ad_extension

        entities.append(bulk_sitelink2_ad_extension)

    bulk_campaign_sitelink2_ad_extension=BulkCampaignSitelink2AdExtension()
    sitelink2_ad_extension_id_to_entity_id_association=campaign_service.factory.create('AdExtensionIdToEntityIdAssociation')
    sitelink2_ad_extension_id_to_entity_id_association.AdExtensionId=SITELINK2_AD_EXTENSION_ID_KEY
    sitelink2_ad_extension_id_to_entity_id_association.EntityId=CAMPAIGN_ID_KEY
    bulk_campaign_sitelink2_ad_extension.ad_extension_id_to_entity_id_association=sitelink2_ad_extension_id_to_entity_id_association
        
    entities.append(bulk_campaign_sitelink2_ad_extension)

    return entities

def get_sample_bulk_site_links_ad_extensions(account_id):
    entities=[]

    bulk_site_link_ad_extension=BulkSiteLinkAdExtension()
    bulk_site_link_ad_extension.account_id=account_id
    site_links_ad_extension=set_elements_to_none(campaign_service.factory.create('SiteLinksAdExtension'))
    site_links=campaign_service.factory.create('ArrayOfSiteLink')

    for index in range(2):
        site_link=set_elements_to_none(campaign_service.factory.create('SiteLink'))
        site_link.Description1="Simple & Transparent."
        site_link.Description2="No Upfront Cost."
        site_link.DisplayText = "Women's Shoe Sale " + str(index+1)

        # If you are currently using the Destination URL, you must upgrade to Final URLs. 
        # Here is an example of a DestinationUrl you might have used previously. 
        # site_link.DestinationUrl='http://www.contoso.com/womenshoesale/?season=spring&promocode=PROMO123'

        # To migrate from DestinationUrl to FinalUrls, you can set DestinationUrl
        # to an empty string when updating the sitelink. If you are removing DestinationUrl,
        # then FinalUrls is required.
        # site_link.DestinationUrl=""
            
        # With FinalUrls you can separate the tracking template, custom parameters, and 
        # landing page URLs.
        final_urls=campaign_service.factory.create('ns4:ArrayOfstring')
        final_urls.string.append('http://www.contoso.com/womenshoesale')
        site_link.FinalUrls=final_urls

        # Final Mobile URLs can also be used if you want to direct the user to a different page 
        # for mobile devices.
        final_mobile_urls=campaign_service.factory.create('ns4:ArrayOfstring')
        final_mobile_urls.string.append('http://mobile.contoso.com/womenshoesale')
        site_link.FinalMobileUrls=final_mobile_urls

        # You could use a tracking template which would override the campaign level
        # tracking template. Tracking templates defined for lower level entities 
        # override those set for higher level entities.
        # In this example we are using the campaign level tracking template.
        site_link.TrackingUrlTemplate=None

        # Set custom parameters that are specific to this sitelink, 
        # and can be used by the sitelink, ad group, campaign, or account level tracking template. 
        # In this example we are using the campaign level tracking template.
        url_custom_parameters=campaign_service.factory.create('ns0:CustomParameters')
        parameters=campaign_service.factory.create('ns0:ArrayOfCustomParameter')
        custom_parameter1=campaign_service.factory.create('ns0:CustomParameter')
        custom_parameter1.Key='promoCode'
        custom_parameter1.Value='PROMO' + str(index+1)
        parameters.CustomParameter.append(custom_parameter1)
        custom_parameter2=campaign_service.factory.create('ns0:CustomParameter')
        custom_parameter2.Key='season'
        custom_parameter2.Value='summer'
        parameters.CustomParameter.append(custom_parameter2)
        url_custom_parameters.Parameters=parameters
        site_link.UrlCustomParameters=url_custom_parameters
        site_links.SiteLink.append(site_link)

    site_links_ad_extension.SiteLinks=site_links
    site_links_ad_extension.Status=None
    site_links_ad_extension.Id=SITE_LINK_AD_EXTENSION_ID_KEY
    bulk_site_link_ad_extension.site_links_ad_extension=site_links_ad_extension

    entities.append(bulk_site_link_ad_extension)

    bulk_campaign_site_link_ad_extension=BulkCampaignSiteLinkAdExtension()
    site_link_ad_extension_id_to_entity_id_association=campaign_service.factory.create('AdExtensionIdToEntityIdAssociation')
    site_link_ad_extension_id_to_entity_id_association.AdExtensionId=SITE_LINK_AD_EXTENSION_ID_KEY
    site_link_ad_extension_id_to_entity_id_association.EntityId=CAMPAIGN_ID_KEY
    bulk_campaign_site_link_ad_extension.ad_extension_id_to_entity_id_association=site_link_ad_extension_id_to_entity_id_association
        
    entities.append(bulk_campaign_site_link_ad_extension)

    return entities

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
    
    customer_service=ServiceClient(
        'CustomerManagementService', 
        authorization_data=authorization_data, 
        environment=ENVIRONMENT,
        version=11,
    )

    # You should authenticate for Bing Ads production services with a Microsoft Account, 
    # instead of providing the Bing Ads username and password set. 
    # Authentication with a Microsoft Account is currently not supported in Sandbox.
        
    authenticate(authorization_data)
        
    main(authorization_data)
