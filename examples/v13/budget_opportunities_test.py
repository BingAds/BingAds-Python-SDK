from auth_helper import *
from openapi_client.models.adinsight import *
from openapi_client.models.campaign import *


def main(authorization_data):
    try:
        # Get all campaigns for the account
        get_campaigns_request = GetCampaignsByAccountIdRequest(
            account_id=authorization_data.account_id
        )
        
        campaigns_response = campaign_service.get_campaigns_by_account_id(
            get_campaigns_by_account_id_request=get_campaigns_request
        )
        
        campaigns = campaigns_response.Campaigns
        
        if not campaigns or len(campaigns) == 0:
            print("No campaigns found for the account.")
            return
        
        print(f"Found {len(campaigns)} campaigns. Getting budget opportunities...")
        
        # Get budget opportunities for each campaign
        for campaign in campaigns:
            if campaign.Id:
                try:
                    get_budget_opportunities_request = GetBudgetOpportunitiesRequest(
                        campaign_id=campaign.Id
                    )
                    
                    response = ad_insight_service.get_budget_opportunities(
                        get_budget_opportunities_request=get_budget_opportunities_request
                    )
                    
                    opportunities = response.Opportunities
                    
                    if opportunities and len(opportunities) > 0:
                        print(f"\nCampaign ID: {campaign.Id}, Name: {campaign.Name}")
                        print(f"Budget Opportunities: {len(opportunities)}")
                        for opportunity in opportunities:
                            print(f"  - Opportunity: {opportunity}")
                    else:
                        print(f"\nCampaign ID: {campaign.Id}, Name: {campaign.Name}")
                        print("  No budget opportunities found.")
                        
                except Exception as ex:
                    print(f"Error getting budget opportunities for campaign {campaign.Id}: {str(ex)}")
                    
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
    
    ad_insight_service = ServiceClient(
        service='AdInsightService',
        version=13,
        authorization_data=authorization_data,
        environment=ENVIRONMENT,
    )
    
    main(authorization_data)