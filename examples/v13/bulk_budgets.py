from auth_helper import *
from bulk_service_manager_helper import *
from output_helper import *

# You must provide credentials in auth_helper.py.

def main(authorization_data):

    errors=[]

    try:
        # Add a budget that can be shared by campaigns in the same account.                
        # Map properties in the Bulk file to the BulkBudget.

        upload_entities=[]
        
        bulk_budget=BulkBudget()
        bulk_budget.client_id='YourClientIdGoesHere'
        budget=set_elements_to_none(campaign_service.factory.create('Budget'))
        budget.Amount=50
        budget.BudgetType='DailyBudgetStandard'
        budget.Id=BUDGET_ID_KEY
        budget.Name="My Shared Budget " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        bulk_budget.budget=budget
        upload_entities.append(bulk_budget)
                
        bulk_campaign=BulkCampaign()
        bulk_campaign.client_id='YourClientIdGoesHere'
        campaign=set_elements_to_none(campaign_service.factory.create('Campaign'))
        # You must set either the shared budget ID or daily amount.
        campaign.BudgetId=BUDGET_ID_KEY
        campaign.BudgetType=None
        campaign.DailyBudget=None
        languages=campaign_service.factory.create('ns3:ArrayOfstring')
        languages.string.append('All')
        campaign.Languages=languages
        campaign.Name="Women's Shoes " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        campaign.TimeZone='PacificTimeUSCanadaTijuana'
        campaign.Id=CAMPAIGN_ID_KEY
        bulk_campaign.campaign=campaign
        upload_entities.append(bulk_campaign)     
        
        output_status_message("-----\nAdding shared budget and campaign...")
        download_entities=write_entities_and_upload_file(
            bulk_service_manager=bulk_service_manager, 
            upload_entities=upload_entities)

        budget_results=[]
        campaign_results=[]

        for entity in download_entities:
            if isinstance(entity, BulkBudget):
                budget_results.append(entity)
                output_bulk_budgets([entity])
            if isinstance(entity, BulkCampaign):
                campaign_results.append(entity)
                output_bulk_campaigns([entity])

        # Delete the campaign and everything it contains e.g., ad groups and ads.
        # Delete the account's shared budget. 

        upload_entities=[]

        for budget_result in budget_results:
            budget_result.status='Deleted'
            upload_entities.append(budget_result)

        for campaign_result in campaign_results:
            campaign_result.campaign.Status='Deleted'
            upload_entities.append(campaign_result)
            
        output_status_message("-----\nDeleting the campaign and shared budget...")
        download_entities=write_entities_and_upload_file(
            bulk_service_manager=bulk_service_manager, 
            upload_entities=upload_entities)

        output_status_message("Upload results:")

        for entity in download_entities:
            if isinstance(entity, BulkBudget):
                output_bulk_budgets([entity])
            if isinstance(entity, BulkCampaign):
                output_bulk_campaigns([entity])
            
        output_status_message("Program execution completed")

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

    campaign_service=ServiceClient(
        service='CampaignManagementService', 
        version=13,
        authorization_data=authorization_data, 
        environment=ENVIRONMENT,
    )

    authenticate(authorization_data)
        
    main(authorization_data)
