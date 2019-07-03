from auth_helper import *
from bulk_service_manager_helper import *
from output_helper import *

# You must provide credentials in auth_helper.py.

def main(authorization_data):

    try:
        download_parameters=DownloadParameters(
            download_entities=['AdGroupProductPartitions'],
            result_file_directory=FILE_DIRECTORY,
            result_file_name=DOWNLOAD_FILE_NAME,
            overwrite_result_file=True,
            last_sync_time_in_utc=None
        )

        output_status_message("-----\nDownloading all product partitions in the account....")
        download_entities=download_file(
            bulk_service_manager=bulk_service_manager, 
            download_parameters=download_parameters)
        
        output_status_message("Download results:")
        for entity in download_entities:
            if isinstance(entity, BulkAdGroupProductPartition):
                output_bulk_ad_group_product_partitions([entity])
        
        upload_entities=[]

        # Within the downloaded records, find all product partition leaf nodes that have bids.
        for entity in download_entities:
            if isinstance(entity, BulkAdGroupProductPartition)  \
            and entity.ad_group_criterion.Type == 'BiddableAdGroupCriterion' \
            and entity.ad_group_criterion.Criterion.PartitionType == 'Unit' \
            and entity.ad_group_criterion.CriterionBid is not None \
            and entity.ad_group_criterion.CriterionBid.Amount is not None:
                # Increase all bids by some predetermined amount or percentage. 
                # Implement your own logic to update bids by varying amounts.
                entity.ad_group_criterion.CriterionBid.Amount += 0.01
                upload_entities.append(entity)
        
        if len(upload_entities) > 0:
            output_status_message("-----\nChanged local bid of all product partitions. Starting upload...")
            download_entities=write_entities_and_upload_file(
                bulk_service_manager=bulk_service_manager, 
                upload_entities=upload_entities)

            output_status_message("Upload results:")

            for entity in download_entities:
                if isinstance(entity, BulkAdGroupProductPartition):
                    output_bulk_ad_group_product_partitions([entity])
        else:
            output_status_message("No product partitions in account.")

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
        
    authenticate(authorization_data)
        
    main(authorization_data)
