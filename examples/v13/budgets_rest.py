import uuid
from time import strftime, gmtime

from auth_helper_rest import *
from openapi_client.models.campaign import *


def main(authorization_data):
    try:
        # Add a budget that can be shared by campaigns in the same account.
        budget = Budget(
            amount=50,
            budget_type=BudgetLimitType.DAILYBUDGETSTANDARD,
            name="My Shared Budget " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        )
        budgets = [budget]

        add_budgets_request = AddBudgetsRequest(
            budgets=budgets
        )

        add_budgets_response = campaign_service.add_budgets(
            add_budgets_request=add_budgets_request
        )
        budget_ids = add_budgets_response.BudgetIds

        # Add a search campaign
        campaign = Campaign(
            budget_id=budget_ids[0],
            budget_type=BudgetLimitType.DAILYBUDGETSTANDARD,
            daily_budget=50,
            languages=['All'],
            name="Women's Shoes " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()),
            time_zone='PacificTimeUSCanadaTijuana'
        )
        campaigns = [campaign]

        add_campaigns_request = AddCampaignsRequest(
            account_id=authorization_data.account_id,
            campaigns=campaigns
        )

        add_campaigns_response = campaign_service.add_campaigns(
            add_campaigns_request=add_campaigns_request
        )
        campaign_ids = add_campaigns_response.CampaignIds

        # Delete the campaign and everything it contains e.g., ad groups and ads.
        delete_campaigns_request = DeleteCampaignsRequest(
            account_id=authorization_data.account_id,
            campaign_ids=campaign_ids
        )

        campaign_service.delete_campaigns(
            delete_campaigns_request=delete_campaigns_request
        )
        print(f"Deleted Campaign Id {campaign_ids[0]}")

        # Delete the budget
        delete_budgets_request = DeleteBudgetsRequest(
            budget_ids=budget_ids
        )

        campaign_service.delete_budgets(
            delete_budgets_request=delete_budgets_request
        )
        print(f"Deleted Budget Id {budget_ids[0]}")

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

    campaign_service = ServiceClient(
        service='CampaignManagementService',
        version=13,
        authorization_data=authorization_data,
        environment=ENVIRONMENT,
    )

    main(authorization_data)