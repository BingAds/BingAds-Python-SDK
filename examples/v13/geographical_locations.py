import urllib3 as urllib
from urllib.error import URLError
from urllib.request import urlopen, Request

from auth_helper import *
from campaignmanagement_example_helper import *

# You must provide credentials in auth_helper.py.

# The full path to the local machine's copy of the geographical locations file.
LOCAL_FILE="c:\geolocations\geolocations.csv"

# The language and locale of the geographical locations file available for download.
# This example uses 'en' (English). Supported locales are 'zh-Hant' (Traditional Chinese), 'en' (English), 'fr' (French), 
# 'de' (German), 'it' (Italian), 'pt-BR' (Portuguese - Brazil), and 'es' (Spanish). 

LANGUAGE_LOCALE = "en"

# The latest supported file format version is 2.0. 

VERSION = "2.0"
       
def main(authorization_data):    
    try:
        output_status_message("-----\nGetGeoLocationsFileUrl:")
        get_geo_locations_file_url_response = campaign_service.GetGeoLocationsFileUrl(
            Version=VERSION, 
            LanguageLocale=LANGUAGE_LOCALE)

        output_status_message("FileUrl: {0}".format(get_geo_locations_file_url_response.FileUrl))
        output_status_message("FileUrlExpiryTimeUtc: {0}".format(get_geo_locations_file_url_response.FileUrlExpiryTimeUtc))
        output_status_message("LastModifiedTimeUtc: {0}".format(get_geo_locations_file_url_response.LastModifiedTimeUtc))

        request=Request(get_geo_locations_file_url_response.FileUrl)
        response=urlopen(request)
                
        if response.getcode() == 200:
            download_file(response)
            output_status_message("Downloaded the geographical locations to {0}.".format(LOCAL_FILE))

    except URLError as ex:
        if hasattr(ex, 'code'):
            output_status_message("Error code: {0}".format(ex.code))
        elif hasattr(ex, 'reason'):
            output_status_message("Reason: {0}".format(ex.reason))
        
    except WebFault as ex:
        output_webfault_errors(ex)
    except Exception as ex:
        output_status_message(ex)

def download_file(response):
    CHUNK=16 * 1024
    with open(LOCAL_FILE, 'wb') as f:
        while True:
            chunk=response.read(CHUNK)
            if not chunk: break
            f.write(chunk)
            f.flush()

# Main execution
if __name__ == '__main__':

    output_status_message("Loading the web service client proxies...")
    
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
        
    authenticate(authorization_data)
        
    main(authorization_data)
