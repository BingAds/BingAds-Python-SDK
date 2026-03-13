"""
Bulk Offline Conversions Test

This example demonstrates how to upload offline conversions using the Bulk API 
with REST-style models.

Offline conversions allow you to track conversions that happen outside of 
direct ad interactions, such as phone calls or in-store purchases.

Prerequisites:
- You must have an OfflineConversionGoal set up in your account
- The conversion name must match the 'Name' of the 'OfflineConversionGoal'
- The MicrosoftClickId must be from a valid ad click

Note: You must provide credentials in auth_helper.py.
"""
from auth_helper import *
from bingads.v13.bulk import *
from openapi_client.models.campaign import OfflineConversion
from datetime import datetime


def main(authorization_data):
    try:
        upload_entities = []
        
        # Create a BulkOfflineConversion
        bulk_offline_conversion = BulkOfflineConversion()
        
        # Create offline conversion using REST-style model
        # If you do not specify an offline conversion currency code,
        # then the 'CurrencyCode' element of the goal's 'ConversionGoalRevenue' is used.
        offline_conversion = OfflineConversion(
            conversion_currency_code="USD",
            # The conversion name must match the 'Name' of the 'OfflineConversionGoal'.
            # If it does not match you won't observe any error, although the offline
            # conversion will not be counted.
            conversion_name="My Conversion Goal Name",
            # The date and time must be in UTC, should align to the date and time of the
            # recorded click (MicrosoftClickId), and cannot be in the future.
            conversion_time=datetime.utcnow(),
            # If you do not specify an offline conversion value,
            # then the 'Value' element of the goal's 'ConversionGoalRevenue' is used.
            conversion_value=10,
            # The MicrosoftClickId must be from a valid ad click
            microsoft_click_id="f894f652ea334e739002f7167ab8f8e3"
        )
        
        bulk_offline_conversion.offline_conversion = offline_conversion
        upload_entities.append(bulk_offline_conversion)
        
        print("-----")
        print("Applying offline conversions...")
        
        download_entities = list(bulk_service_manager.upload_entities(
            EntityUploadParameters(
                entities=upload_entities,
                response_mode='ErrorsAndResults'
            )
        ))
        
        print("\nUpload results:")
        
        offline_conversion_results = []
        
        for entity in download_entities:
            if isinstance(entity, BulkOfflineConversion):
                offline_conversion_results.append(entity)
                if entity.offline_conversion:
                    conversion = entity.offline_conversion
                    print(f"  Conversion Name: {conversion.ConversionName}")
                    print(f"  Conversion Time: {conversion.ConversionTime}")
                    print(f"  Conversion Value: {conversion.ConversionValue}")
                    print(f"  Microsoft Click ID: {conversion.MicrosoftClickId}")
                    print(f"  Currency Code: {conversion.ConversionCurrencyCode}")
                if entity.has_errors:
                    print(f"  Errors: {entity.errors}")
        
        print(f"\nProcessed {len(offline_conversion_results)} offline conversion(s)")
        print("\nProgram execution completed")
        
    except Exception as ex:
        print(f"Error occurred: {str(ex)}")
        import traceback
        traceback.print_exc()


# Main execution
if __name__ == '__main__':
    print("Loading the web service client...")
    
    authorization_data = AuthorizationData(
        account_id=None,
        customer_id=None,
        developer_token=DEVELOPER_TOKEN,
        authentication=None,
    )
    
    authenticate(authorization_data)
    
    bulk_service_manager = BulkServiceManager(
        authorization_data=authorization_data,
        poll_interval_in_milliseconds=5000,
        environment=ENVIRONMENT,
    )
    
    main(authorization_data)
