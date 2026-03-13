"""
Bulk Keyword Bid Update Test

This example demonstrates how to download all keywords in an account,
update their bids, and upload the changes using the Bulk API with REST-style models.

The workflow:
1. Download all keywords using DownloadParameters
2. Find keywords with bids and increase them
3. Upload the modified keywords

Note: You must provide credentials in auth_helper.py.
"""
from auth_helper import *
from bingads.v13.bulk import *


def main(authorization_data):
    try:
        # Download all keywords in the account
        print("-----")
        print("Downloading all keywords in the account....")
        
        download_parameters = DownloadParameters(
            download_entities=['Keywords'],
            result_file_directory='c:/test/',
            result_file_name='download.csv',
            overwrite_result_file=True,
            last_sync_time_in_utc=None
            # campaign_ids=[OptionalCampaignId1GoesHere, OptionalCampaignId2GoesHere]
        )
        
        download_entities = list(bulk_service_manager.download_entities(
            download_parameters=download_parameters
        ))
        
        print("Download results:")
        for entity in download_entities:
            if isinstance(entity, BulkKeyword):
                if entity.keyword:
                    keyword = entity.keyword
                    bid_amount = keyword.Bid.Amount if keyword.Bid else None
                    print(f"  Keyword ID: {keyword.Id}, Text: {keyword.Text}, Bid: {bid_amount}")
        
        upload_entities = []
        
        # Within the downloaded records, find all keywords that have bids
        for entity in download_entities:
            if isinstance(entity, BulkKeyword) \
                    and entity.keyword is not None \
                    and entity.keyword.Bid is not None \
                    and entity.keyword.Bid.Amount is not None:
                # Increase all bids by some predetermined amount or percentage
                # Implement your own logic to update bids by varying amounts
                entity.keyword.Bid.Amount += 0.01
                upload_entities.append(entity)
        
        if len(upload_entities) > 0:
            print("-----")
            print(f"Changed local bid of {len(upload_entities)} keywords. Starting upload...")
            
            download_entities = list(bulk_service_manager.upload_entities(
                EntityUploadParameters(
                    entities=upload_entities,
                    response_mode='ErrorsAndResults'
                )
            ))
            
            print("Upload results:")
            for entity in download_entities:
                if isinstance(entity, BulkKeyword):
                    if entity.keyword:
                        keyword = entity.keyword
                        bid_amount = keyword.Bid.Amount if keyword.Bid else None
                        print(f"  Keyword ID: {keyword.Id}, Text: {keyword.Text}, Updated Bid: {bid_amount}")
                    if entity.has_errors:
                        print(f"    Errors: {entity.errors}")
        else:
            print("No keywords with bids found in account.")
        
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
