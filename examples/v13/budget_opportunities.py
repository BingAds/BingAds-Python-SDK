from auth_helper import *
from adinsight_example_helper import *
from campaignmanagement_example_helper import *

# You must provide credentials in auth_helper.py.

def main(authorization_data): 

    try:
        output_status_message("-----\nGetCampaignsByAccountId:")
        campaigns=campaign_service.GetCampaignsByAccountId(
            AccountId=authorization_data.account_id, 
            CampaignType=ALL_CAMPAIGN_TYPES)
        output_status_message("Campaigns:")
        output_array_of_campaign(campaigns)

        # Get the budget opportunities for each campaign in the current account.

        for campaign in campaigns['Campaign']:
            if campaign.Id is not None:
                output_status_message("-----\nGetBudgetOpportunities:")
                opportunities=adinsight_service.GetBudgetOpportunities(
                    CampaignId=campaign.Id)
                output_status_message("Opportunities:")
                output_array_of_budgetopportunity(opportunities)

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

    adinsight_service=ServiceClient(
        service='AdInsightService', 
        version=13,
        authorization_data=authorization_data, 
        environment=ENVIRONMENT,
    )
    
    campaign_service=ServiceClient(
        service='CampaignManagementService', 
        version=13,
        authorization_data=authorization_data, 
        environment=ENVIRONMENT,
    )
        
    authenticate(authorization_data)
        
    main(authorization_data)
   
