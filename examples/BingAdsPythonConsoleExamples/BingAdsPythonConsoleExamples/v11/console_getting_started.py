from auth_helper import *
from bulk_service_manager_helper import *
from output_helper import *

# You must provide credentials in auth_helper.py.

def main(authorization_data):

    try:
        #To discover all SOAP elements accessible for each service, you can print the soap client.
        #For example, print(campaign_service.soap_client) will return Campaign, AdGroup, ExpandedTextAd, Keyword, etc. 

        #You could use the Campaign Management ServiceClient to add a Campaign as follows:
        #add_campaigns_response=campaign_service.AddCampaigns(
        #    AccountId=authorization_data.account_id,
        #    Campaigns=campaigns
        #)

        #BulkEntity-derived classes can also contain the SOAP objects, for example BulkCampaign can contain a Campaign.
        #As shown below, you can use the BulkServiceManager to upload a BulkCampaign. 
        #You should take advantage of the Bulk service to efficiently manage ads and keywords for all campaigns in an account.
        
        CAMPAIGN_ID_KEY=-123

        bulk_campaign=BulkCampaign()
        
        #The client_id may be used to associate records in the bulk upload file with records in the results file. The value of this field  
        #is not used or stored by the server; it is simply copied from the uploaded record to the corresponding result record. 
        #Note: This bulk file Client Id is not related to an application Client Id for OAuth. 

        bulk_campaign.client_id='YourClientIdGoesHere'
        campaign=set_elements_to_none(campaign_service.factory.create('Campaign'))
        
        #When using the Campaign Management service, the Id cannot be set. In the context of a BulkCampaign, the Id is optional  
        #and may be used as a negative reference key during bulk upload. For example the same negative reference key for the campaign Id  
        #will be used when adding new ad groups to this new campaign, or when associating ad extensions with the campaign. 

        campaign.Id=CAMPAIGN_ID_KEY
        campaign.Name="Summer Shoes " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        campaign.Description="Summer shoes line."
        campaign.BudgetType='DailyBudgetStandard'
        campaign.DailyBudget=10
        campaign.TimeZone='PacificTimeUSCanadaTijuana'
        campaign.Status='Paused'
        bulk_campaign.campaign=campaign

        bulk_campaigns=[ bulk_campaign ]
    
        entity_upload_parameters=EntityUploadParameters(
            result_file_directory=FILE_DIRECTORY,
            result_file_name=RESULT_FILE_NAME,
            entities=bulk_campaigns,
            overwrite_result_file=True,
            response_mode='ErrorsAndResults'
        )
    
        output_status_message("Adding a BulkCampaign...\n")
        bulk_entities=list(bulk_service_manager.upload_entities(entity_upload_parameters))
    
        # Output the upload result entities
        for entity in bulk_entities:
            if isinstance(entity, BulkCampaign):
                output_bulk_campaigns([entity])
    
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
