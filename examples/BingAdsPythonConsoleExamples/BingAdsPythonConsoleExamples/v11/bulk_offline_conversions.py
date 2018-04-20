from auth_helper import *
from bulk_service_manager_helper import *
from output_helper import *

# You must provide credentials in auth_helper.py.

def main(authorization_data):

    errors=[]

    try:
        
        upload_entities=[]

        bulk_offline_conversion=BulkOfflineConversion()
        offline_conversion=set_elements_to_none(campaign_service.factory.create('OfflineConversion'))
        # If you do not specify an offline conversion currency code, 
        # then the 'CurrencyCode' element of the goal's 'ConversionGoalRevenue' is used.
        offline_conversion.ConversionCurrencyCode = "USD"
        # The conversion name must match the 'Name' of the 'OfflineConversionGoal'.
        # If it does not match you won't observe any error, although the offline
        # conversion will not be counted.
        offline_conversion.ConversionName = "My Conversion Goal Name"
        # The date and time must be in UTC, should align to the date and time of the 
        # recorded click (MicrosoftClickId), and cannot be in the future.
        offline_conversion.ConversionTime = datetime.utcnow()
        # If you do not specify an offline conversion value, 
        # then the 'Value' element of the goal's 'ConversionGoalRevenue' is used.
        offline_conversion.ConversionValue = 10
        offline_conversion.MicrosoftClickId = "f894f652ea334e739002f7167ab8f8e3"
        bulk_offline_conversion.offline_conversion=offline_conversion
                
        upload_entities.append(bulk_offline_conversion)
    
        output_status_message("\nApplying offline conversions...\n")
        download_entities=write_entities_and_upload_file(bulk_service_manager, upload_entities)

        offlineconversion_results=[]

        for entity in download_entities:
            if isinstance(entity, BulkOfflineConversion):
                offlineconversion_results.append(entity)
                output_bulk_offlineconversions([entity])
            
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
