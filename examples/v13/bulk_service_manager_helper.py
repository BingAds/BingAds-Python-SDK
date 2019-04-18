from output_helper import output_percent_complete
from bingads.v13.bulk import *

ACTION_AD_EXTENSION_ID_KEY=-10
APP_AD_EXTENSION_ID_KEY=-11
CALL_AD_EXTENSION_ID_KEY=-12
CALLOUT_AD_EXTENSION_ID_KEY=-13
IMAGE_AD_EXTENSION_ID_KEY=-14
LOCATION_AD_EXTENSION_ID_KEY=-15
PRICE_AD_EXTENSION_ID_KEY=-16
REVIEW_AD_EXTENSION_ID_KEY=-17
SITELINK_AD_EXTENSION_ID_KEY=-18
STRUCTURED_SNIPPET_AD_EXTENSION_ID_KEY=-19
BUDGET_ID_KEY=-20
CAMPAIGN_ID_KEY=-123
AD_GROUP_ID_KEY=-1234

# The directory for the bulk files.
FILE_DIRECTORY='c:/bulk/'

# The name of the bulk download file.
DOWNLOAD_FILE_NAME='download.csv'

#The name of the bulk upload file.
UPLOAD_FILE_NAME='upload.csv'

# The name of the bulk upload result file.
RESULT_FILE_NAME='result.csv'

# The bulk file extension type as a string.
FILE_TYPE = 'Csv'

# The maximum amount of time (in milliseconds) that you want to wait for the bulk download or upload.
TIMEOUT_IN_MILLISECONDS=3600000

def write_entities_and_upload_file(bulk_service_manager, upload_entities):
    # Writes the specified entities to a local file and uploads the file. We could have uploaded directly
    # without writing to file. This example writes to file as an exercise so that you can view the structure 
    # of the bulk records being uploaded as needed. 
    writer=BulkFileWriter(FILE_DIRECTORY+UPLOAD_FILE_NAME)
    for entity in upload_entities:
        writer.write_entity(entity)
    writer.close()

    file_upload_parameters=FileUploadParameters(
        result_file_directory=FILE_DIRECTORY,
        compress_upload_file=True,
        result_file_name=RESULT_FILE_NAME,
        overwrite_result_file=True,
        upload_file_path=FILE_DIRECTORY+UPLOAD_FILE_NAME,
        response_mode='ErrorsAndResults'
    )

    bulk_file_path=bulk_service_manager.upload_file(file_upload_parameters, progress=output_percent_complete)

    download_entities=[]
    entities_generator=read_entities_from_bulk_file(file_path=bulk_file_path, result_file_type=ResultFileType.upload, file_type=FILE_TYPE)
    for entity in entities_generator:
        download_entities.append(entity)

    return download_entities

def download_file(bulk_service_manager, download_parameters):
    bulk_file_path=bulk_service_manager.download_file(download_parameters, progress=output_percent_complete)

    download_entities=[]
    entities_generator=read_entities_from_bulk_file(file_path=bulk_file_path, result_file_type=ResultFileType.full_download, file_type=FILE_TYPE)
    for entity in entities_generator:
        download_entities.append(entity)

    return download_entities

def read_entities_from_bulk_file(file_path, result_file_type, file_type):
    with BulkFileReader(file_path=file_path, result_file_type=result_file_type, file_type=file_type) as reader:
        for entity in reader:
            yield entity
