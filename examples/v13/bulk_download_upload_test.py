import time
import os
from auth_helper import *
from openapi_client.models.bulk import *

# The full path to the bulk file
BULK_FILE_PATH = "c:\\dev\\bulk\\campaigns.zip"
UPLOAD_FILE_PATH = "c:\\dev\\bulk\\campaigns_upload.zip"

def main(authorization_data):
    try:
        # Confirm that the download folder exists
        folder = os.path.dirname(BULK_FILE_PATH)
        if not os.path.exists(folder):
            print(f"The output folder, {folder}, does not exist.")
            print("Ensure that the folder exists and try again.")
            return
        
        # Download campaigns by account IDs
        print("Requesting bulk download...")
        
        download_request = DownloadCampaignsByAccountIdsRequest(
            account_ids=[authorization_data.account_id],
            data_scope=DataScope.ENTITYDATA,
            download_entities=[DownloadEntity.ADGROUPS, DownloadEntity.CAMPAIGNS],
            download_file_type=DownloadFileType.CSV,
            format_version='6.0',
            last_sync_time_in_utc=None
        )
        
        download_response = bulk_service.download_campaigns_by_account_ids(
            download_campaigns_by_account_ids_request=download_request
        )
        
        download_request_id = download_response.DownloadRequestId
        
        if not download_request_id:
            print("DownloadRequestId should not be null")
            return
        
        print(f"Download Request ID: {download_request_id}")
        
        # Poll for download status
        print("\nPolling for download status...")
        
        download_success = False
        wait_time = 5
        result_file_url = None
        
        for i in range(10):
            time.sleep(wait_time)
            
            status_request = GetBulkDownloadStatusRequest(
                request_id=download_request_id
            )
            
            status_response = bulk_service.get_bulk_download_status(
                get_bulk_download_status_request=status_request
            )
            
            request_status = status_response.RequestStatus
            result_file_url = status_response.ResultFileUrl
            
            print(f"Attempt {i+1}:")
            print(f"  PercentComplete: {status_response.PercentComplete}")
            print(f"  RequestStatus: {request_status}")
            print(f"  ResultFileUrl: {result_file_url}")
            
            if request_status == "Completed":
                download_success = True
                break
        
        if download_success and result_file_url:
            print(f"\nDownloading file from {result_file_url}...")
            # In a real implementation, you would download the file here
            # For example, using requests library:
            # import requests
            # response = requests.get(result_file_url)
            # with open(BULK_FILE_PATH, 'wb') as f:
            #     f.write(response.content)
            print(f"File would be saved to: {BULK_FILE_PATH}")
        else:
            print(f"Download request failed or timed out. Request ID: {download_request_id}")
            return
        
        # Bulk Upload
        print("\n" + "="*50)
        print("Starting bulk upload...")
        
        get_upload_url_request = GetBulkUploadUrlRequest(
            response_mode=ResponseMode.ERRORSANDRESULTS,
            account_id=authorization_data.account_id
        )
        
        upload_url_response = bulk_service.get_bulk_upload_url(
            get_bulk_upload_url_request=get_upload_url_request
        )
        
        upload_request_id = upload_url_response.RequestId
        upload_url = upload_url_response.UploadUrl
        
        print(f"Upload Request ID: {upload_request_id}")
        print(f"Upload URL: {upload_url}")
        
        if not upload_request_id or not upload_url:
            print("UploadRequestId or UploadUrl should not be null")
            return
        
        # Upload the file
        print(f"\nUploading file {UPLOAD_FILE_PATH} to {upload_url}...")
        # In a real implementation, you would upload the file here
        # For example, using requests library with multipart upload:
        # import requests
        # with open(UPLOAD_FILE_PATH, 'rb') as f:
        #     files = {'payload': ('payload.zip', f, 'application/zip')}
        #     headers = {
        #         'DeveloperToken': DEVELOPER_TOKEN,
        #         'CustomerId': str(authorization_data.customer_id),
        #         'CustomerAccountId': str(authorization_data.account_id)
        #     }
        #     response = requests.post(upload_url, files=files, headers=headers)
        print("File upload would be performed here")
        
        # Poll for upload status
        print("\nPolling for upload status...")
        
        upload_success = False
        
        for i in range(10):
            time.sleep(wait_time)
            
            upload_status_request = GetBulkUploadStatusRequest(
                request_id=upload_request_id
            )
            
            upload_status_response = bulk_service.get_bulk_upload_status(
                get_bulk_upload_status_request=upload_status_request
            )
            
            request_status = upload_status_response.RequestStatus
            result_file_url = upload_status_response.ResultFileUrl
            
            print(f"Attempt {i+1}:")
            print(f"  PercentComplete: {upload_status_response.PercentComplete}")
            print(f"  RequestStatus: {request_status}")
            print(f"  ResultFileUrl: {result_file_url}")
            
            if request_status in ["Completed", "CompletedWithErrors"]:
                upload_success = True
                break
        
        if upload_success and result_file_url:
            print(f"\nDownloading result file from {result_file_url}...")
            print(f"Result file would be saved to: {BULK_FILE_PATH}")
        else:
            print(f"Upload request failed or timed out. Request ID: {upload_request_id}")
            
    except Exception as ex:
        print(f"Error occurred: {str(ex)}")

if __name__ == '__main__':
    print("Loading the web service client...")
    
    authorization_data = AuthorizationData(
        account_id=None,
        customer_id=None,
        developer_token=DEVELOPER_TOKEN,
        authentication=None,
    )
    
    authenticate(authorization_data)
    
    bulk_service = ServiceClient(
        service='BulkService',
        version=13,
        authorization_data=authorization_data,
        environment=ENVIRONMENT,
    )
    
    main(authorization_data)