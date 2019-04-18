import base64

from auth_helper import *
from campaignmanagement_example_helper import *

# You must provide credentials in auth_helper.py.

# To run this example you'll need to provide your own image.  
# For required aspect ratios and recommended dimensions please see 
# Image remarks at https://go.microsoft.com/fwlink/?linkid=872754.

MEDIA_FILE_PATH = "c:\dev\media\\"
IMAGE_AD_EXTENSION_MEDIA_FILE_NAME = "imageadextension300x200.png"

def main(authorization_data):
    
    try:
        
        # Add a campaign to associate with ad extensions. 

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
        
        # Create media for the image ad extension that we'll add later. 

        image_ad_extension_media = get_image_media(
            "Image15x10",
            MEDIA_FILE_PATH + IMAGE_AD_EXTENSION_MEDIA_FILE_NAME)

        media = { 
            'Media': 
            [
                image_ad_extension_media
            ]
        }
        
        # Add the media to the account's library.

        output_status_message("-----\nAddMedia:")
        media_ids = campaign_service.AddMedia(
            AccountId=authorization_data.account_id,
            Media=media)
        output_status_message("MediaIds:")
        output_array_of_long(media_ids)
        
        # Add the extensions to the account's library.

        ad_extensions=campaign_service.factory.create('ArrayOfAdExtension')
        final_urls=campaign_service.factory.create('ns3:ArrayOfstring')
        final_urls.string.append('http://www.contoso.com/womenshoesale')

        action_ad_extension=set_elements_to_none(campaign_service.factory.create('ActionAdExtension'))
        action_ad_extension.ActionType='ActNow'
        action_ad_extension.FinalUrls=final_urls
        action_ad_extension.Language='English'
        action_ad_extension.Status='Active'
        ad_extensions.AdExtension.append(action_ad_extension)
        
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
        ad_extensions.AdExtension.append(location_ad_extension)

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
        ad_extensions.AdExtension.append(price_ad_extension)

        review_ad_extension=set_elements_to_none(campaign_service.factory.create('ReviewAdExtension'))
        review_ad_extension.IsExact=True
        review_ad_extension.Source="Review Source Name"
        review_ad_extension.Text="Review Text"
        # The Url of the third-party review. This is not your business Url.
        review_ad_extension.Url="http://review.contoso.com" 
        ad_extensions.AdExtension.append(review_ad_extension)

        sitelink_ad_extension=set_elements_to_none(campaign_service.factory.create('SitelinkAdExtension'))
        sitelink_ad_extension.Description1="Simple & Transparent."
        sitelink_ad_extension.Description2="No Upfront Cost."
        sitelink_ad_extension.DisplayText = "Women's Shoe Sale"
        sitelink_ad_extension.FinalUrls=final_urls
        ad_extensions.AdExtension.append(sitelink_ad_extension)

        structured_snippet_ad_extension=set_elements_to_none(campaign_service.factory.create('StructuredSnippetAdExtension'))
        structured_snippet_ad_extension.Header = "Brands"
        values=campaign_service.factory.create('ns3:ArrayOfstring')
        values.string.append('Windows')
        values.string.append('Xbox')
        values.string.append('Skype')
        structured_snippet_ad_extension.Values=values
        ad_extensions.AdExtension.append(structured_snippet_ad_extension)
        
        # Add all extensions to the account's ad extension library

        output_status_message("-----\nAddAdExtensions:")
        add_ad_extensions_response=campaign_service.AddAdExtensions(
            AccountId=authorization_data.account_id,
            AdExtensions=ad_extensions
        )
        output_status_message("AdExtensionIdentities:")
        ad_extension_identities={
            'AdExtensionIdentity': add_ad_extensions_response.AdExtensionIdentities['AdExtensionIdentity'] 
                if add_ad_extensions_response.AdExtensionIdentities['AdExtensionIdentity']
                else None
        }
        output_array_of_adextensionidentity(ad_extension_identities)
        output_status_message("NestedPartialErrors:")
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

        # Associate the ad extensions with the campaign. 

        output_status_message("-----\nSetAdExtensionsAssociations:")
        set_ad_extensions_associations_response=campaign_service.SetAdExtensionsAssociations(
            AccountId=authorization_data.account_id,
            AdExtensionIdToEntityIdAssociations=ad_extension_id_to_entity_id_associations,
            AssociationType='Campaign'
        )
        output_status_message("PartialErrors:")
        if hasattr(set_ad_extensions_associations_response, 'PartialErrors'):
            output_array_of_batcherror(set_ad_extensions_associations_response.PartialErrors)

        # Get editorial rejection reasons for the respective ad extension and entity associations.

        output_status_message("-----\nGetAdExtensionsEditorialReasons:")
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
        output_status_message("EditorialReasons:")
        output_array_of_adextensioneditorialreasoncollection(ad_extension_editorial_reason_collection)
        output_status_message("PartialErrors:")
        output_array_of_batcherror(get_ad_extensions_editorial_reasons_response.PartialErrors)

        # Get only the location extensions and remove scheduling.

        ad_extensions_type_filter = 'LocationAdExtension'

        # In this example partial errors will be returned for indices where the ad extensions 
        # are not location ad extensions.
        # This is an example, and ideally you would only send the required ad extension IDs.

        output_status_message("-----\nGetAdExtensionsByIds:")
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
        output_status_message("AdExtensions:")
        output_array_of_adextension(ad_extensions)
        output_status_message("PartialErrors:")
        output_array_of_batcherror(get_ad_extensions_by_ids_response.PartialErrors)

        update_extensions=campaign_service.factory.create('ArrayOfAdExtension')
        update_extension_ids = []

        for extension in ad_extensions['AdExtension']:

            # GetAdExtensionsByIds will return a nil element if the request conditions were not met.
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
        
        output_status_message("-----\nUpdateAdExtensions:")
        campaign_service.UpdateAdExtensions(
            AccountId=authorization_data.account_id,
            AdExtensions=update_extensions
        )
        output_status_message("Removed scheduling from the location ad extensions.")
        
        # Get only the location extension to output the result.

        output_status_message("-----\nGetAdExtensionsByIds:")
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
        output_status_message("AdExtensions:")
        output_array_of_adextension(ad_extensions)
        output_status_message("PartialErrors:")
        output_array_of_batcherror(get_ad_extensions_by_ids_response.PartialErrors)

        # Delete the ad extension associations, ad extensions, and campaign, that were previously added.  
        # At this point the ad extensions are still available in the account's ad extensions library. 

        output_status_message("-----\nDeleteAdExtensionsAssociations:")
        campaign_service.DeleteAdExtensionsAssociations(
            AccountId=authorization_data.account_id,
            AdExtensionIdToEntityIdAssociations=ad_extension_id_to_entity_id_associations,
            AssociationType='Campaign'
        )
        output_status_message("Deleted ad extension associations.")

        # Delete the ad extensions from the account's ad extension library.

        output_status_message("-----\nDeleteAdExtensions:")
        campaign_service.DeleteAdExtensions(
            AccountId=authorization_data.account_id,
            AdExtensionIds={'long': ad_extension_ids},
        )
        output_status_message("Deleted ad extensions.")

        # Delete the account's media that was used for the image ad extension.
        
        output_status_message("-----\nDeleteMedia:")
        delete_media_response = campaign_service.DeleteMedia(
            authorization_data.account_id,
            media_ids)

        for id in media_ids['long']:
            output_status_message("Deleted Media Id {0}".format(id))

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

def get_image_media(
    media_type, 
    image_file_name):
    image = campaign_service.factory.create('Image')
    image.Data = get_bmp_base64_string(image_file_name)
    image.MediaType = media_type
    image.Type = "Image"

    return image

def get_bmp_base64_string(image_file_name):
    image = open(image_file_name, 'rb') 
    image_bytes = image.read() 
    base64_string = base64.encodestring(image_bytes)
    return base64_string

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

    customer_service=ServiceClient(
        service='CustomerManagementService', 
        version=13,
        authorization_data=authorization_data, 
        environment=ENVIRONMENT,
    )
        
    authenticate(authorization_data)
        
    main(authorization_data)
