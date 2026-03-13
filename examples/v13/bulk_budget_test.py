"""
Bulk Budget and Campaign Test

This example demonstrates two ways to create campaigns with the SDK:
1. REST-style: Using Pydantic models from openapi_client (recommended for new code)
2. SOAP-style: Using factory-created objects (legacy approach)

The REST adapter automatically converts REST-style models to SOAP-compatible
format when assigned to bulk entities.
"""
from auth_helper import *
from bingads.v13.bulk import *
from openapi_client.models.campaign import Campaign, CampaignType, CampaignStatus, BudgetLimitType
from openapi_client.models.campaign import Budget
from openapi_client.models.campaign import EnhancedCpcBiddingScheme


def main(authorization_data):
    try:
        # Add a budget that can be shared by campaigns in the same account.
        print("Adding shared budget and campaign...")
        
        upload_entities = []

        bulk_budget = BulkBudget()
        bulk_budget.account_id = authorization_data.account_id
        
        # REST-style Budget creation - clean and type-safe
        budget = Budget(
            amount=50,
            budget_type='DailyBudgetStandard',
            name="My Shared Budget " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        )
        bulk_budget.budget = budget
        upload_entities.append(bulk_budget)

        bulk_campaign = BulkCampaign()
        bulk_campaign.account_id = authorization_data.account_id

        campaign = Campaign(
            budget_type=BudgetLimitType.DAILYBUDGETSTANDARD,
            daily_budget=20.0,
            name='REST Campaign - {0}'.format(uuid.uuid1()),
            status=CampaignStatus.ACTIVE,
            time_zone='PacificTimeUSCanadaTijuana',
            campaign_type=CampaignType.SEARCH,
            languages=['All'],
            audience_ads_bid_adjustment=0,
            final_url_suffix='',
            bidding_scheme=EnhancedCpcBiddingScheme(Type='EnhancedCpc'),
        )
        
        # The adapter automatically converts REST model to SOAP-compatible format
        bulk_campaign.campaign = campaign
        upload_entities.append(bulk_campaign)
        
        # Write and upload entities
        print("Uploading entities...")
        download_entities = bulk_service_manager.upload_entities(
            EntityUploadParameters(
                entities=upload_entities,
                response_mode='ErrorsAndResults'
            )
        )
        
        print("\nUpload results:")
        
        budget_results = []
        campaign_results = []
        
        for entity in download_entities:
            if isinstance(entity, BulkBudget):
                budget_results.append(entity)
                if entity.budget and entity.budget.Id:
                    print(f"Created Budget ID: {entity.budget.Id}, Name: {entity.budget.Name}")
                if entity.has_errors:
                    print(f"  Errors: {entity.errors}")
            elif isinstance(entity, BulkCampaign):
                campaign_results.append(entity)
                if entity.campaign and entity.campaign.Id:
                    print(f"Created Campaign ID: {entity.campaign.Id}, Name: {entity.campaign.Name}, Budget ID: {entity.campaign.BudgetId}")
                if entity.has_errors:
                    print(f"  Errors: {entity.errors}")
        
        # Delete the campaign and shared budget
        print("\nDeleting campaign and shared budget...")
        
        upload_entities = []
        
        for budget_result in budget_results:
            budget_result.status = 'Deleted'
            upload_entities.append(budget_result)
        
        for campaign_result in campaign_results:
            if campaign_result.campaign:
                campaign_result.campaign.Status = 'Deleted'
            upload_entities.append(campaign_result)
        
        download_entities = bulk_service_manager.upload_entities(
            EntityUploadParameters(
                entities=upload_entities,
                response_mode='ErrorsAndResults'
            )
        )
        
        print("Delete results:")
        for entity in download_entities:
            if isinstance(entity, BulkBudget):
                print(f"Deleted Budget ID: {entity.budget.Id if entity.budget else 'N/A'}")
                if entity.has_errors:
                    print(f"  Errors: {entity.errors}")
            elif isinstance(entity, BulkCampaign):
                print(f"Deleted Campaign ID: {entity.campaign.Id if entity.campaign else 'N/A'}")
                if entity.has_errors:
                    print(f"  Errors: {entity.errors}")
        
        print("\nProgram execution completed")
        
    except Exception as ex:
        print(f"Error occurred: {str(ex)}")
        import traceback
        traceback.print_exc()


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
    
    bulk_service_manager = BulkServiceManager(
        authorization_data=authorization_data,
        poll_interval_in_milliseconds=5000,
        environment=ENVIRONMENT,
    )
    
    main(authorization_data)
