from auth_helper import *
from campaignmanagement_example_helper import *

# You must provide credentials in auth_helper.py.

def main(authorization_data):

    try:
        # Add a budget that can be shared by campaigns in the same account.
                
        budgets = campaign_service.factory.create('ArrayOfBudget')
        budget=set_elements_to_none(campaign_service.factory.create('Budget'))
        budget.Amount = 50
        budget.BudgetType = 'DailyBudgetStandard'
        budget.Name = "My Shared Budget " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        budgets.Budget.append(budget)

        output_status_message("-----\nAddBudgets:");    
        add_budgets_response = campaign_service.AddBudgets(
            Budgets=budgets
        )
        budget_ids={
            'long': add_budgets_response.BudgetIds['long'] if add_budgets_response.BudgetIds['long'] else None
        }
        output_status_message("Budget Ids:")
        output_array_of_long(budget_ids)
        output_status_message("PartialErrors:")
        output_array_of_batcherror(add_budgets_response.PartialErrors)

        # Add a search campaign
        
        campaigns=campaign_service.factory.create('ArrayOfCampaign')
        campaign=set_elements_to_none(campaign_service.factory.create('Campaign'))
        # We'll use the shared budget instead of defining a daily amount for this campaign.
        campaign.BudgetId=budget_ids['long'][0]
        campaign.BudgetType='DailyBudgetStandard'
        campaign.DailyBudget=50
        campaign.Description="Red shoes line."
        languages=campaign_service.factory.create('ns3:ArrayOfstring')
        languages.string.append('All')
        campaign.Languages=languages
        campaign.Name="Women's Shoes " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        campaign.TimeZone='PacificTimeUSCanadaTijuana'
        campaigns.Campaign.append(campaign)

        output_status_message("-----\nAddCampaigns:")
        add_campaigns_response=campaign_service.AddCampaigns(
            AccountId=authorization_data.account_id,
            Campaigns=campaigns
        )
        campaign_ids={
            'long': add_campaigns_response.CampaignIds['long'] if add_campaigns_response.CampaignIds['long'] else None
        }
        output_status_message("CampaignIds:")
        output_array_of_long(campaign_ids)
        output_status_message("PartialErrors:")
        output_array_of_batcherror(add_campaigns_response.PartialErrors)

        # Delete the campaign and everything it contains e.g., ad groups and ads.

        output_status_message("-----\nDeleteCampaigns:")
        campaign_service.DeleteCampaigns(
            AccountId=authorization_data.account_id,
            CampaignIds=campaign_ids
        )
        output_status_message("Deleted Campaign Id {0}".format(campaign_ids['long'][0]))
        
        output_status_message("-----\nDeleteBudgets:")
        campaign_service.DeleteBudgets(
            BudgetIds=budget_ids
        )
        output_status_message("Deleted BudgetId {0}".format(budget_ids['long'][0]))

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

    campaign_service=ServiceClient(
        service='CampaignManagementService', 
        version=12,
        authorization_data=authorization_data, 
        environment=ENVIRONMENT,
    )
        
    authenticate(authorization_data)
        
    main(authorization_data)
