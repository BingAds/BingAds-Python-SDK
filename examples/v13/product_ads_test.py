import uuid
from auth_helper import *
from openapi_client.models.campaign import *

def main(authorization_data):
    try:
        # Create a shopping campaign
        print("Creating shopping campaign...")
        print("Note: You need a valid Store ID from your Microsoft Merchant Center account.")
        
        shopping_setting = ShoppingSetting(
            priority=0,
            sales_country_code="US",
            store_id="1"  # Replace with your actual Store ID from Microsoft Merchant Center
        )
        
        campaign = Campaign(
            name="Women's Shoes " + str(uuid.uuid4()),
            campaign_type=CampaignType.SHOPPING,
            budget_type=BudgetLimitType.DAILYBUDGETSTANDARD,
            daily_budget=50.00,
            languages=['All'],
            time_zone='PacificTimeUSCanadaTijuana',
            settings=[shopping_setting]
        )
        
        add_campaigns_request = AddCampaignsRequest(
            account_id=authorization_data.account_id,
            campaigns=[campaign]
        )
        
        add_campaigns_response = campaign_service.add_campaigns(
            add_campaigns_request=add_campaigns_request
        )
        
        campaign_ids = add_campaigns_response.CampaignIds
        print(f"Created Campaign ID: {campaign_ids[0]}")
        
        if add_campaigns_response.PartialErrors:
            print(f"Partial Errors: {add_campaigns_response.PartialErrors}")
        
        # Create an ad group
        print("\nCreating ad group...")
        
        current_year = datetime.now().year
        
        ad_group = AdGroup(
            name="Women's Red Shoe Sale" + str(uuid.uuid4())[:8],
            cpc_bid=Bid(amount=0.09),
            start_date=None,
            end_date=ModelDate(day=31, month=12, year=current_year)
        )
        
        add_ad_groups_request = AddAdGroupsRequest(
            campaign_id=campaign_ids[0],
            ad_groups=[ad_group]
        )
        
        add_ad_groups_response = campaign_service.add_ad_groups(
            add_ad_groups_request=add_ad_groups_request
        )
        
        ad_group_ids = add_ad_groups_response.AdGroupIds
        print(f"Created Ad Group ID: {ad_group_ids[0]}")
        
        if add_ad_groups_response.PartialErrors:
            print(f"Partial Errors: {add_ad_groups_response.PartialErrors}")
        
        # Create a product ad
        print("\nCreating product ad...")
        
        # Product ads are dynamically generated from your product catalog
        # No additional properties need to be set
        product_ad = ProductAd()
        
        add_ads_request = AddAdsRequest(
            ad_group_id=ad_group_ids[0],
            ads=[product_ad]
        )
        
        add_ads_response = campaign_service.add_ads(
            add_ads_request=add_ads_request
        )
        
        ad_ids = add_ads_response.AdIds
        print(f"Created Ad IDs: {ad_ids}")
        
        if add_ads_response.PartialErrors:
            print(f"Partial Errors: {add_ads_response.PartialErrors}")
        else:
            print("Product ad created successfully")
        
        # Delete campaign
        print("\nDeleting campaign...")
        
        delete_campaigns_request = DeleteCampaignsRequest(
            account_id=authorization_data.account_id,
            campaign_ids=campaign_ids
        )
        
        campaign_service.delete_campaigns(
            delete_campaigns_request=delete_campaigns_request
        )
        
        print(f"Deleted Campaign ID {campaign_ids[0]}")
        
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
    
    main(authorization_data)