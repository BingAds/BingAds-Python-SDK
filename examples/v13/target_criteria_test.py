import uuid
from auth_helper import *
from openapi_client.models.campaign import *

def main(authorization_data):
    try:
        # Create a campaign
        print("Creating campaign...")
        
        campaign = Campaign(
            name="Women's Shoes " + str(uuid.uuid4()),
            budget_type=BudgetLimitType.DAILYBUDGETSTANDARD,
            daily_budget=50.00,
            languages=['All'],
            time_zone='PacificTimeUSCanadaTijuana'
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
            end_date=Date(day=31, month=12, year=current_year)
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
        
        # Add campaign criterion (location target)
        print("\nAdding campaign criterion...")
        print("When you first create a campaign or ad group using the Bing Ads API, it will not have any")
        print("target criteria. Effectively, the brand new campaign and ad group target all ages, days, hours,")
        print("devices, genders, and locations. As a best practice, you should consider at a minimum")
        print("adding a campaign location criterion corresponding to the customer market country.")
        
        # Target United States at campaign level
        location_criterion = LocationCriterion(
            location_id="190"  # United States
        )
        
        campaign_criterion = BiddableCampaignCriterion(
            campaign_id=campaign_ids[0],
            criterion=location_criterion,
            criterion_bid=BidMultiplier(multiplier=0.0)
        )
        
        add_campaign_criterions_request = AddCampaignCriterionsRequest(
            campaign_criterions=[campaign_criterion],
            criterion_type=CampaignCriterionType.TARGETS
        )
        
        add_campaign_criterions_response = campaign_service.add_campaign_criterions(
            add_campaign_criterions_request=add_campaign_criterions_request
        )
        
        campaign_criterion_ids = add_campaign_criterions_response.CampaignCriterionIds
        print(f"Created Campaign Criterion IDs: {campaign_criterion_ids}")
        
        if add_campaign_criterions_response.NestedPartialErrors:
            print(f"Nested Partial Errors: {add_campaign_criterions_response.NestedPartialErrors}")
        else:
            print("Campaign criterion created successfully")
        
        # Add ad group criterion (negative location)
        print("\nAdding ad group criterion...")
        print("A negative location criterion is an excluded location.")
        print("Ads in this ad group will not be shown to people in Redmond, WA.")
        
        # Exclude Redmond, WA at ad group level
        negative_location_criterion = LocationCriterion(
            location_id="67555"  # Redmond, WA
        )
        
        ad_group_criterion = NegativeAdGroupCriterion(
            ad_group_id=ad_group_ids[0],
            criterion=negative_location_criterion
        )
        
        add_ad_group_criterions_request = AddAdGroupCriterionsRequest(
            ad_group_criterions=[ad_group_criterion],
            criterion_type=AdGroupCriterionType.TARGETS
        )
        
        add_ad_group_criterions_response = campaign_service.add_ad_group_criterions(
            add_ad_group_criterions_request=add_ad_group_criterions_request
        )
        
        ad_group_criterion_ids = add_ad_group_criterions_response.AdGroupCriterionIds
        print(f"Created Ad Group Criterion IDs: {ad_group_criterion_ids}")
        
        if add_ad_group_criterions_response.NestedPartialErrors:
            print(f"Nested Partial Errors: {add_ad_group_criterions_response.NestedPartialErrors}")
        else:
            print("Ad group criterion created successfully")
        
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