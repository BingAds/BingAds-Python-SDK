from auth_helper import *
from adinsight_example_helper import *

# You must provide credentials in auth_helper.py.

def main(authorization_data): 

    try:
        # Get the budget opportunities for each campaign in the current authenticated account.

        campaign_types=['Search', 'Shopping']
        campaigns=campaign_service.GetCampaignsByAccountId(authorization_data.account_id, campaign_types)

        for campaign in campaigns['Campaign']:
            if campaign.Id is not None:
                opportunities=adinsight_service.GetBudgetOpportunities(campaign.Id)
                output_status_message("Budget Opportunities for CampaignId {0}:\n".format(campaign.Id))
                output_array_of_budgetopportunity(opportunities)

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

    adinsight_service=ServiceClient(
        service='AdInsightService', 
        version=12,
        authorization_data=authorization_data, 
        environment=ENVIRONMENT,
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
   
