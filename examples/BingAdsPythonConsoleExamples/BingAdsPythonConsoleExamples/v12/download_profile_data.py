import urllib2

from auth_helper import *
from campaignmanagement_example_helper import *

# You must provide credentials in auth_helper.py.

# The full path to the profile data.
LOCAL_FILE="c:\profiledata\profiledata.csv"

# The language and locale of the profile data available for download.
# This example uses 'en' (English). 

LANGUAGE_LOCALE = "en"
       
def main(authorization_data):    
    try:
        # Supported profile types are CompanyName, Industry, and JobFunction

        get_profile_data_file_url_response = campaign_service.GetProfileDataFileUrl(
            LANGUAGE_LOCALE,
            'CompanyName')
        
        output_status_message("FileUrl: {0}".format(get_profile_data_file_url_response.FileUrl))
        output_status_message("FileUrlExpiryTimeUtc: {0}".format(get_profile_data_file_url_response.FileUrlExpiryTimeUtc))
        output_status_message("LastModifiedTimeUtc: {0}".format(get_profile_data_file_url_response.LastModifiedTimeUtc))

        request=urllib2.Request(get_profile_data_file_url_response.FileUrl)
        response=urllib2.urlopen(request)
                
        if response.getcode() == 200:
            download_file(response)
            output_status_message("Downloaded the profile data to {0}.\n".format(LOCAL_FILE))
        
        output_status_message("Program execution completed")

    except urllib2.URLError as ex:
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

    # You should authenticate for Bing Ads production services with a Microsoft Account.
        
    authenticate(authorization_data)
        
    main(authorization_data)
