from auth_helper import *
from campaignmanagement_example_helper import *

# You must provide credentials in auth_helper.py.

def main(authorization_data):
    
    try:
        
        # Add a campaign that will later be associated with ad extensions. 

        campaigns=campaign_service.factory.create('ArrayOfCampaign')
        campaign=set_elements_to_none(campaign_service.factory.create('Campaign'))
        campaign.Name="Summer Shoes " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        campaign.Description="Summer shoes line."
        campaign.BudgetType='DailyBudgetStandard'
        campaign.DailyBudget=10
        campaign.TimeZone='PacificTimeUSCanadaTijuana'
        campaign.Status='Paused'

        # Used with FinalUrls shown in the sitelinks that we will add below.
        campaign.TrackingUrlTemplate="http://tracker.example.com/?season={_season}&promocode={_promocode}&u={lpurl}"

        campaigns.Campaign.append(campaign)

        add_campaigns_response=campaign_service.AddCampaigns(
            AccountId=authorization_data.account_id,
            Campaigns=campaigns
        )
        campaign_ids={
            'long': add_campaigns_response.CampaignIds['long'] if add_campaigns_response.CampaignIds['long'] else None
        }
        if hasattr(add_campaigns_response.PartialErrors, 'BatchError'):
            output_array_of_batcherror(add_campaigns_response.PartialErrors)
        output_status_message("Added campaign(s) with Id(s):\n")
        output_array_of_long(campaign_ids)
        
        # Specify the extensions.

        ad_extensions=campaign_service.factory.create('ArrayOfAdExtension')
        
        app_ad_extension=set_elements_to_none(campaign_service.factory.create('AppAdExtension'))
        app_ad_extension.AppPlatform='Windows'
        app_ad_extension.AppStoreId='AppStoreIdGoesHere'
        app_ad_extension.DisplayText='Contoso'
        app_ad_extension.DestinationUrl='DestinationUrlGoesHere'
        # If you supply the AppAdExtension properties above, then you can add this line.
        #ad_extensions.AdExtension.append(app_ad_extension)

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
        ad_extensions.AdExtension.append(call_ad_extension)

        callout_ad_extension=set_elements_to_none(campaign_service.factory.create('CalloutAdExtension'))
        callout_ad_extension.Text="Callout Text"
        ad_extensions.AdExtension.append(callout_ad_extension)

        location_ad_extension=set_elements_to_none(campaign_service.factory.create('LocationAdExtension'))
        location_ad_extension.PhoneNumber="206-555-0100"
        location_ad_extension.CompanyName="Contoso Shoes"
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
        ad_extensions.AdExtension.append(location_ad_extension)

        review_ad_extension=set_elements_to_none(campaign_service.factory.create('ReviewAdExtension'))
        review_ad_extension.IsExact=True
        review_ad_extension.Source="Review Source Name"
        review_ad_extension.Text="Review Text"
        # The Url of the third-party review. This is not your business Url.
        review_ad_extension.Url="http://review.contoso.com" 
        ad_extensions.AdExtension.append(review_ad_extension)

        structured_snippet_ad_extension=set_elements_to_none(campaign_service.factory.create('StructuredSnippetAdExtension'))
        structured_snippet_ad_extension.Header = "Brands"
        values=campaign_service.factory.create('ns3:ArrayOfstring')
        values.string.append('Windows')
        values.string.append('Xbox')
        values.string.append('Skype')
        structured_snippet_ad_extension.Values=values
        ad_extensions.AdExtension.append(structured_snippet_ad_extension)
        
        ad_extensions.AdExtension.append(get_sample_sitelink_ad_extensions()['AdExtension'])

        # Add all extensions to the account's ad extension library
        add_ad_extensions_response=campaign_service.AddAdExtensions(
            AccountId=authorization_data.account_id,
            AdExtensions=ad_extensions
        )
        output_status_message("Added ad extensions.\n")
        ad_extension_identities={
            'AdExtensionIdentity': add_ad_extensions_response.AdExtensionIdentities['AdExtensionIdentity'] 
                if add_ad_extensions_response.AdExtensionIdentities['AdExtensionIdentity']
                else None
        }
        if hasattr(add_ad_extensions_response.NestedPartialErrors, 'BatchErrorCollection'):
            output_array_of_batcherrorcollection(add_ad_extensions_response.NestedPartialErrors)       

        # DeleteAdExtensionsAssociations, SetAdExtensionsAssociations, and GetAdExtensionsEditorialReasons 
        # operations each require a list of type AdExtensionIdToEntityIdAssociation.
        ad_extension_id_to_entity_id_associations=campaign_service.factory.create('ArrayOfAdExtensionIdToEntityIdAssociation')

        # GetAdExtensionsByIds requires a list of type long.
        ad_extension_ids=[]

        # Loop through the list of extension IDs and build any required data structures
        # for subsequent operations. 

        for ad_extension_identity in ad_extension_identities['AdExtensionIdentity']:
            ad_extension_id_to_entity_id_association=campaign_service.factory.create('AdExtensionIdToEntityIdAssociation')
            ad_extension_id_to_entity_id_association.AdExtensionId=ad_extension_identity.Id
            ad_extension_id_to_entity_id_association.EntityId=campaign_ids['long'][0]
            ad_extension_id_to_entity_id_associations.AdExtensionIdToEntityIdAssociation.append(ad_extension_id_to_entity_id_association)

            ad_extension_ids.append(ad_extension_identity.Id)

        # Associate the specified ad extensions with the respective campaigns or ad groups. 
        campaign_service.SetAdExtensionsAssociations(
            AccountId=authorization_data.account_id,
            AdExtensionIdToEntityIdAssociations=ad_extension_id_to_entity_id_associations,
            AssociationType='Campaign'
        )

        output_status_message("Set ad extension associations.\n")

        # Get editorial rejection reasons for the respective ad extension and entity associations.
        get_ad_extensions_editorial_reasons_response=campaign_service.GetAdExtensionsEditorialReasons(
            AccountId=authorization_data.account_id,
            AdExtensionIdToEntityIdAssociations=ad_extension_id_to_entity_id_associations,
            AssociationType='Campaign'
        )
        ad_extension_editorial_reason_collection={
            'AdExtensionEditorialReasonCollection': get_ad_extensions_editorial_reasons_response.EditorialReasons['AdExtensionEditorialReasonCollection'] 
                if get_ad_extensions_editorial_reasons_response.EditorialReasons['AdExtensionEditorialReasonCollection']
                else None
        }
        if hasattr(get_ad_extensions_editorial_reasons_response.PartialErrors, 'BatchError'):
            output_array_of_batcherror(get_ad_extensions_editorial_reasons_response.PartialErrors)

        ad_extensions_type_filter='AppAdExtension ' \
                                  'CallAdExtension ' \
                                  'CalloutAdExtension ' \
                                  'ImageAdExtension ' \
                                  'LocationAdExtension ' \
                                  'ReviewAdExtension ' \
                                  'SitelinkAdExtension ' \
                                  'StructuredSnippetAdExtension'
                
        # Get the specified ad extensions from the account's ad extension library.
        get_ad_extensions_by_ids_response=campaign_service.GetAdExtensionsByIds(
            AccountId=authorization_data.account_id,
            AdExtensionIds={'long': ad_extension_ids},
            AdExtensionType=ad_extensions_type_filter
        )
        ad_extensions={
            'AdExtension': get_ad_extensions_by_ids_response.AdExtensions['AdExtension'] 
                if get_ad_extensions_by_ids_response.AdExtensions['AdExtension']
                else None
        }
        if hasattr(get_ad_extensions_by_ids_response.PartialErrors, 'BatchError'):
            output_array_of_batcherror(get_ad_extensions_by_ids_response.PartialErrors)

        output_status_message("List of ad extensions that were added above:\n")
        output_array_of_adextension(ad_extensions)
        output_array_of_adextensioneditorialreasoncollection(get_ad_extensions_editorial_reasons_response.EditorialReasons)

        # Get only the location extensions and remove scheduling.

        adExtensionsTypeFilter = 'LocationAdExtension'

        get_ad_extensions_by_ids_response=campaign_service.GetAdExtensionsByIds(
            AccountId=authorization_data.account_id,
            AdExtensionIds={'long': ad_extension_ids},
            AdExtensionType=ad_extensions_type_filter
        )
        ad_extensions={
            'AdExtension': get_ad_extensions_by_ids_response.AdExtensions['AdExtension'] 
                if get_ad_extensions_by_ids_response.AdExtensions['AdExtension']
                else None
        }
        if hasattr(get_ad_extensions_by_ids_response.PartialErrors, 'BatchError'):
            output_array_of_batcherror(get_ad_extensions_by_ids_response.PartialErrors)

        update_extensions=campaign_service.factory.create('ArrayOfAdExtension')
        update_extension_ids = []

        for extension in ad_extensions['AdExtension']:

            # GetAdExtensionsByIds will return a nil element if the request filters / conditions were not met.
            if extension is not None and extension.Id is not None:
            
                # Remove read-only elements that would otherwise cause the update operation to fail.
                update_extension = set_read_only_ad_extension_elements_to_none(extension)

                # If you set the Scheduling element null, any existing scheduling set for the ad extension will remain unchanged. 
                # If you set this to any non-null Schedule object, you are effectively replacing existing scheduling 
                # for the ad extension. In this example, we will remove any existing scheduling by setting this element  
                # to an empty Schedule object.
                update_extension.Scheduling=campaign_service.factory.create('Schedule')

                update_extensions.AdExtension.append(update_extension)
                update_extension_ids.append(update_extension.Id)
        
        output_status_message("Removing scheduling from the location ad extensions..\n")
        campaign_service.UpdateAdExtensions(
            AccountId=authorization_data.account_id,
            AdExtensions=update_extensions
        )
        
        get_ad_extensions_by_ids_response=campaign_service.GetAdExtensionsByIds(
            AccountId=authorization_data.account_id,
            AdExtensionIds={'long': update_extension_ids},
            AdExtensionType=ad_extensions_type_filter
        )
        ad_extensions={
            'AdExtension': get_ad_extensions_by_ids_response.AdExtensions['AdExtension'] 
                if get_ad_extensions_by_ids_response.AdExtensions['AdExtension']
                else None
        }
        if hasattr(get_ad_extensions_by_ids_response.PartialErrors, 'BatchError'):
            output_array_of_batcherror(get_ad_extensions_by_ids_response.PartialErrors)

        output_status_message("List of ad extensions that were updated above:\n")
        output_array_of_adextension(ad_extensions)

        # Remove the specified associations from the respective campaigns or ad groups. 
        # The extesions are still available in the account's extensions library. 
        campaign_service.DeleteAdExtensionsAssociations(
            AccountId=authorization_data.account_id,
            AdExtensionIdToEntityIdAssociations=ad_extension_id_to_entity_id_associations,
            AssociationType='Campaign'
        )

        output_status_message("Deleted ad extension associations.\n")

        # Deletes the ad extensions from the account's ad extension library.
        campaign_service.DeleteAdExtensions(
            AccountId=authorization_data.account_id,
            AdExtensionIds={'long': ad_extension_ids},
        )

        output_status_message("Deleted ad extensions.\n")

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

def get_sample_sitelink_ad_extensions():
    sitelink_ad_extensions=campaign_service.factory.create('ArrayOfAdExtension')
    
    for index in range(2):
        sitelink_ad_extension=set_elements_to_none(campaign_service.factory.create('SitelinkAdExtension'))
        sitelink_ad_extension.Description1="Simple & Transparent."
        sitelink_ad_extension.Description2="No Upfront Cost."
        sitelink_ad_extension.DisplayText = "Women's Shoe Sale " + str(index)
            
        # With FinalUrls you can separate the tracking template, custom parameters, and 
        # landing page URLs.
        final_urls=campaign_service.factory.create('ns3:ArrayOfstring')
        final_urls.string.append('http://www.contoso.com/womenshoesale')
        sitelink_ad_extension.FinalUrls=final_urls

        # Final Mobile URLs can also be used if you want to direct the user to a different page 
        # for mobile devices.
        final_mobile_urls=campaign_service.factory.create('ns3:ArrayOfstring')
        final_mobile_urls.string.append('http://mobile.contoso.com/womenshoesale')
        sitelink_ad_extension.FinalMobileUrls=final_mobile_urls

        # You could use a tracking template which would override the campaign level
        # tracking template. Tracking templates defined for lower level entities 
        # override those set for higher level entities.
        # In this example we are using the campaign level tracking template.
        sitelink_ad_extension.TrackingUrlTemplate=None

        # Set custom parameters that are specific to this ad extension, 
        # and can be used by the ad extension, ad group, campaign, or account level tracking template. 
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
        sitelink_ad_extension.UrlCustomParameters=url_custom_parameters
        sitelink_ad_extensions.AdExtension.append(sitelink_ad_extension)

    return sitelink_ad_extensions

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

    customer_service=ServiceClient(
        'CustomerManagementService', 
        version=12,
        authorization_data=authorization_data, 
        environment=ENVIRONMENT,
    )

    # You should authenticate for Bing Ads production services with a Microsoft Account.
        
    authenticate(authorization_data)
        
    main(authorization_data)
