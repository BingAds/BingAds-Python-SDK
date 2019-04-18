from auth_helper import *
from bulk_service_manager_helper import *
from output_helper import *

# You must provide credentials in auth_helper.py.

def main(authorization_data):

    errors=[]

    try:

        # Add a new campaign and associate it with ad extensions. 

        bulk_campaign=BulkCampaign()
        bulk_campaign.client_id='YourClientIdGoesHere'
        campaign=set_elements_to_none(campaign_service.factory.create('Campaign'))
        campaign.BudgetType='DailyBudgetStandard'
        campaign.DailyBudget=50
        languages=campaign_service.factory.create('ns3:ArrayOfstring')
        languages.string.append('All')
        campaign.Languages=languages
        campaign.Name="Women's Shoes " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        campaign.TimeZone='PacificTimeUSCanadaTijuana'
        campaign.Id=CAMPAIGN_ID_KEY
        bulk_campaign.campaign=campaign

        ad_extensions=campaign_service.factory.create('ArrayOfAdExtension')
        final_urls=campaign_service.factory.create('ns3:ArrayOfstring')
        final_urls.string.append('http://www.contoso.com/womenshoesale')

        bulk_action_ad_extension=BulkActionAdExtension()
        bulk_action_ad_extension.account_id=authorization_data.account_id
        action_ad_extension=set_elements_to_none(campaign_service.factory.create('ActionAdExtension'))
        action_ad_extension.ActionType='ActNow'
        action_ad_extension.FinalUrls=final_urls
        action_ad_extension.Language='English'
        action_ad_extension.Status='Active'
        action_ad_extension.Id=ACTION_AD_EXTENSION_ID_KEY
        bulk_action_ad_extension.action_ad_extension=action_ad_extension

        bulk_campaign_action_ad_extension=BulkCampaignActionAdExtension()
        action_ad_extension_id_to_entity_id_association=campaign_service.factory.create('AdExtensionIdToEntityIdAssociation')
        action_ad_extension_id_to_entity_id_association.AdExtensionId=ACTION_AD_EXTENSION_ID_KEY
        action_ad_extension_id_to_entity_id_association.EntityId=CAMPAIGN_ID_KEY
        bulk_campaign_action_ad_extension.ad_extension_id_to_entity_id_association=action_ad_extension_id_to_entity_id_association

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
        # Include the call extension Monday - Friday from 9am - 9pm
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
        # Include the location extension every Saturday morning
        # in the search user's time zone.
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

        bulk_price_ad_extension=BulkPriceAdExtension()
        bulk_price_ad_extension.account_id=authorization_data.account_id
        price_ad_extension=set_elements_to_none(campaign_service.factory.create('PriceAdExtension'))
        price_ad_extension.Language="English"
        price_ad_extension.PriceExtensionType='Events'
        table_rows=campaign_service.factory.create('ArrayOfPriceTableRow')
        table_row_a=campaign_service.factory.create('PriceTableRow')
        table_row_a.CurrencyCode="USD"
        table_row_a.Description="Come to the event"
        table_row_a.FinalUrls=final_urls
        table_row_a.Header="New Event"
        table_row_a.Price=9.99
        table_row_a.PriceQualifier='From'
        table_row_a.PriceUnit='PerDay'
        table_rows.PriceTableRow.append(table_row_a)
        table_row_b=campaign_service.factory.create('PriceTableRow')
        table_row_b.CurrencyCode="USD"
        table_row_b.Description="Come to the next event"
        table_row_b.FinalUrls=final_urls
        table_row_b.Header="Next Event"
        table_row_b.Price=9.99
        table_row_b.PriceQualifier='From'
        table_row_b.PriceUnit='PerDay'
        table_rows.PriceTableRow.append(table_row_b)
        table_row_c=campaign_service.factory.create('PriceTableRow')
        table_row_c.CurrencyCode="USD"
        table_row_c.Description="Come to the final event"
        table_row_c.FinalUrls=final_urls
        table_row_c.Header="Final Event"
        table_row_c.Price=9.99
        table_row_c.PriceQualifier='From'
        table_row_c.PriceUnit='PerDay'
        table_rows.PriceTableRow.append(table_row_c)
        price_ad_extension.TableRows=table_rows
        price_ad_extension.Id=PRICE_AD_EXTENSION_ID_KEY
        bulk_price_ad_extension.price_ad_extension=price_ad_extension

        bulk_campaign_price_ad_extension=BulkCampaignPriceAdExtension()
        price_ad_extension_id_to_entity_id_association=campaign_service.factory.create('AdExtensionIdToEntityIdAssociation')
        price_ad_extension_id_to_entity_id_association.AdExtensionId=PRICE_AD_EXTENSION_ID_KEY
        price_ad_extension_id_to_entity_id_association.EntityId=CAMPAIGN_ID_KEY
        bulk_campaign_price_ad_extension.ad_extension_id_to_entity_id_association=price_ad_extension_id_to_entity_id_association

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

        bulk_sitelink_ad_extension=BulkSitelinkAdExtension()
        bulk_sitelink_ad_extension.account_id=authorization_data.account_id
        sitelink_ad_extension=set_elements_to_none(campaign_service.factory.create('SitelinkAdExtension'))
        sitelink_ad_extension.Description1="Simple & Transparent."
        sitelink_ad_extension.Description2="No Upfront Cost."
        sitelink_ad_extension.DisplayText = "Women's Shoe Sale"
        sitelink_ad_extension.FinalUrls=final_urls
        sitelink_ad_extension.Id=SITELINK_AD_EXTENSION_ID_KEY
        bulk_sitelink_ad_extension.sitelink_ad_extension=sitelink_ad_extension

        bulk_campaign_sitelink_ad_extension=BulkCampaignSitelinkAdExtension()
        sitelink_ad_extension_id_to_entity_id_association=campaign_service.factory.create('AdExtensionIdToEntityIdAssociation')
        sitelink_ad_extension_id_to_entity_id_association.AdExtensionId=SITELINK_AD_EXTENSION_ID_KEY
        sitelink_ad_extension_id_to_entity_id_association.EntityId=CAMPAIGN_ID_KEY
        bulk_campaign_sitelink_ad_extension.ad_extension_id_to_entity_id_association=sitelink_ad_extension_id_to_entity_id_association
        
        bulk_structured_snippet_ad_extension=BulkStructuredSnippetAdExtension()
        bulk_structured_snippet_ad_extension.account_id=authorization_data.account_id
        structured_snippet_ad_extension=set_elements_to_none(campaign_service.factory.create('StructuredSnippetAdExtension'))
        structured_snippet_ad_extension.Header = "Brands"
        values=campaign_service.factory.create('ns3:ArrayOfstring')
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

        upload_entities=[]
        upload_entities.append(bulk_campaign)
        upload_entities.append(bulk_action_ad_extension)
        upload_entities.append(bulk_campaign_action_ad_extension)
        upload_entities.append(bulk_app_ad_extension)
        upload_entities.append(bulk_campaign_app_ad_extension)
        upload_entities.append(bulk_call_ad_extension)
        upload_entities.append(bulk_campaign_call_ad_extension)
        upload_entities.append(bulk_callout_ad_extension)
        upload_entities.append(bulk_campaign_callout_ad_extension)
        upload_entities.append(bulk_location_ad_extension)
        upload_entities.append(bulk_campaign_location_ad_extension)
        upload_entities.append(bulk_price_ad_extension)
        upload_entities.append(bulk_campaign_price_ad_extension)
        upload_entities.append(bulk_review_ad_extension)
        upload_entities.append(bulk_campaign_review_ad_extension)
        upload_entities.append(bulk_sitelink_ad_extension)
        upload_entities.append(bulk_campaign_sitelink_ad_extension)
        upload_entities.append(bulk_structured_snippet_ad_extension)
        upload_entities.append(bulk_campaign_structured_snippet_ad_extension)

        output_status_message("-----\nAdding campaign, ad extensions, and associations...")
        download_entities=write_entities_and_upload_file(
            bulk_service_manager=bulk_service_manager, 
            upload_entities=upload_entities)

        output_status_message("Upload results:")

        campaign_results=[]
        action_ad_extension_results=[]
        app_ad_extension_results=[]
        call_ad_extension_results=[]
        callout_ad_extension_results=[]
        location_ad_extension_results=[]
        price_ad_extension_results=[]
        review_ad_extension_results=[]
        sitelink_ad_extension_results=[]
        structured_snippet_ad_extension_results=[]

        for entity in download_entities:
            if isinstance(entity, BulkCampaign):
                campaign_results.append(entity)
                output_bulk_campaigns([entity])
            if isinstance(entity, BulkActionAdExtension):
                action_ad_extension_results.append(entity)
                output_bulk_action_ad_extensions([entity])
            if isinstance(entity, BulkCampaignActionAdExtension):
                output_bulk_campaign_action_ad_extensions([entity])
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
            if isinstance(entity, BulkPriceAdExtension):
                price_ad_extension_results.append(entity)
                output_bulk_price_ad_extensions([entity])
            if isinstance(entity, BulkCampaignPriceAdExtension):
                output_bulk_campaign_price_ad_extensions([entity])
            if isinstance(entity, BulkReviewAdExtension):
                review_ad_extension_results.append(entity)
                output_bulk_review_ad_extensions([entity])
            if isinstance(entity, BulkCampaignReviewAdExtension):
                output_bulk_campaign_review_ad_extensions([entity])
            if isinstance(entity, BulkSitelinkAdExtension):
                sitelink_ad_extension_results.append(entity)
                output_bulk_sitelink_ad_extensions([entity])
            if isinstance(entity, BulkCampaignSitelinkAdExtension):
                output_bulk_campaign_sitelink_ad_extensions([entity])
            if isinstance(entity, BulkStructuredSnippetAdExtension):
                structured_snippet_ad_extension_results.append(entity)
                output_bulk_structured_snippet_ad_extensions([entity])
            if isinstance(entity, BulkCampaignStructuredSnippetAdExtension):
                output_bulk_campaign_structured_snippet_ad_extensions([entity])
            
        # Delete the campaign and ad extensions that were previously added. 

        upload_entities=[]

        for campaign_result in campaign_results:
            campaign_result.campaign.Status='Deleted'
            upload_entities.append(campaign_result)

        for action_ad_extension_result in action_ad_extension_results:
            action_ad_extension_result.action_ad_extension.Status='Deleted'
            upload_entities.append(action_ad_extension_result)
        
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

        for price_ad_extension_result in price_ad_extension_results:
            price_ad_extension_result.price_ad_extension.Status='Deleted'
            upload_entities.append(price_ad_extension_result)

        for review_ad_extension_result in review_ad_extension_results:
            review_ad_extension_result.review_ad_extension.Status='Deleted'
            upload_entities.append(review_ad_extension_result)

        for sitelink_ad_extension_result in sitelink_ad_extension_results:
            sitelink_ad_extension_result.sitelink_ad_extension.Status='Deleted'
            upload_entities.append(sitelink_ad_extension_result)

        for structured_snippet_ad_extension_result in structured_snippet_ad_extension_results:
            structured_snippet_ad_extension_result.structured_snippet_ad_extension.Status='Deleted'
            upload_entities.append(structured_snippet_ad_extension_result)

        output_status_message("\nDeleting campaign and ad extensions . . .")
        download_entities=write_entities_and_upload_file(
            bulk_service_manager=bulk_service_manager, 
            upload_entities=upload_entities)

        for entity in download_entities:
            if isinstance(entity, BulkCampaign):
                output_bulk_campaigns([entity])
            if isinstance(entity, BulkActionAdExtension):
                output_bulk_action_ad_extensions([entity])
            if isinstance(entity, BulkAppAdExtension):
                output_bulk_app_ad_extensions([entity])
            if isinstance(entity, BulkCallAdExtension):
                output_bulk_call_ad_extensions([entity])
            if isinstance(entity, BulkCalloutAdExtension):
                output_bulk_callout_ad_extensions([entity])
            if isinstance(entity, BulkLocationAdExtension):
                output_bulk_location_ad_extensions([entity])
            if isinstance(entity, BulkPriceAdExtension):
                output_bulk_price_ad_extensions([entity])
            if isinstance(entity, BulkReviewAdExtension):
                output_bulk_review_ad_extensions([entity])
            if isinstance(entity, BulkSitelinkAdExtension):
                output_bulk_sitelink_ad_extensions([entity])
            if isinstance(entity, BulkStructuredSnippetAdExtension):
                output_bulk_structured_snippet_ad_extensions([entity])

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

    bulk_service_manager=BulkServiceManager(
        authorization_data=authorization_data, 
        poll_interval_in_milliseconds=5000, 
        environment=ENVIRONMENT,
    )

    campaign_service=ServiceClient(
        service='CampaignManagementService', 
        version=13,
        authorization_data=authorization_data, 
        environment=ENVIRONMENT,
    )
    
    customer_service=ServiceClient(
        service='CustomerManagementService', 
        version=13,
        authorization_data=authorization_data, 
        environment=ENVIRONMENT,
    )
        
    authenticate(authorization_data)
        
    main(authorization_data)
