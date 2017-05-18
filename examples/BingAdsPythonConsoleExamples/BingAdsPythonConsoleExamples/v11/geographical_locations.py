import urllib.request as urllib2

from auth_helper import *
from output_helper import *

# You must provide credentials in auth_helper.py.

# The full path to the local machine's copy of the geographical locations file.
LOCAL_FILE="c:\geolocations\geolocations.csv"

# The language and locale of the geographical locations file available for download.
# This example uses 'en' (English). Supported locales are 'zh-Hant' (Traditional Chinese), 'en' (English), 'fr' (French), 
# 'de' (German), 'it' (Italian), 'pt-BR' (Portuguese - Brazil), and 'es' (Spanish). 

LANGUAGE_LOCALE = "en"

# The only supported file format version is 1.0. 

VERSION = "1.0"
       
def main(authorization_data):    
    try:
        get_geo_locations_file_url_response = campaign_service.GetGeoLocationsFileUrl(VERSION, LANGUAGE_LOCALE)

        request=urllib.request.Request(get_geo_locations_file_url_response.FileUrl)
        response=urllib.request.urlopen(request)
                
        if response.getcode() == 200:
            download_locations_file(response)
            print(("Downloaded the geographical locations to {0}.\n".format(LOCAL_FILE)))
        
        output_status_message("Program execution completed")

    except urllib.error.URLError as ex:
        if hasattr(ex, 'code'):
            print(("Error code: {0}".format(ex.code)))
        elif hasattr(ex, 'reason'):
            print(("Reason: {0}".format(ex.reason)))
        
    except WebFault as ex:
        output_webfault_errors(ex)
    except Exception as ex:
        output_status_message(ex)

def download_locations_file(response):
    CHUNK=16 * 1024
    with open(LOCAL_FILE, 'wb') as f:
        while True:
            chunk=response.read(CHUNK)
            if not chunk: break
            f.write(chunk)
            f.flush()

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
        authorization_data=authorization_data, 
        environment=ENVIRONMENT,
        version=11,
    )

    # You should authenticate for Bing Ads production services with a Microsoft Account, 
    # instead of providing the Bing Ads username and password set. 
    # Authentication with a Microsoft Account is currently not supported in Sandbox.
        
    authenticate(authorization_data)
        
    main(authorization_data)