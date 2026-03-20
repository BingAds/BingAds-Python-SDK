import uuid
from datetime import datetime
from auth_helper import *
from openapi_client.models.campaign import *


def main(authorization_data):
    try:
        # Add a new campaign with DSA settings
        # Dynamic search ad campaign creation is no longer allowed. 
        # Please create a search campaign with DSA settings instead.
        print("Creating campaign with Dynamic Search Ads settings...")
        
        dynamic_search_setting = DynamicSearchAdsSetting(
            domain_name="www.contoso.com",
            language="English"
        )
        
        campaign = Campaign(
            name="Women's Shoes " + str(uuid.uuid4()),
            budget_type=BudgetLimitType.DAILYBUDGETSTANDARD,
            campaign_type=CampaignType.SEARCH,
            daily_budget=50.00,
            languages=['All'],
            time_zone='PacificTimeUSCanadaTijuana',
            settings=[dynamic_search_setting]
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
        
        # Create a new ad group within the dynamic search ads campaign
        print("\nCreating ad group...")
        
        current_year = datetime.now().year
        
        ad_group = AdGroup(
            name="Women's Red Shoe Sale" + str(uuid.uuid4()),
            cpc_bid=Bid(amount=0.09),
            start_date=None,
            end_date=Date(day=31, month=12, year=current_year),
            ad_group_type="SearchDynamic"
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
        
        # Add one or more Webpage criteria to each ad group
        print("\nAdding positive ad group webpage criterion...")
        
        webpage_criterion = Webpage(
            parameter=WebpageParameter(
                conditions=[
                    WebpageCondition(
                        operand=WebpageConditionOperand.PAGECONTENT,
                        argument="flowers"
                    )
                ],
                criterion_name="Ad Group Webpage Positive Page Content Criterion" + str(uuid.uuid4())
            )
        )
        
        biddable_ad_group_criterion = BiddableAdGroupCriterion(
            ad_group_id=ad_group_ids[0],
            criterion=webpage_criterion,
            criterion_bid=FixedBid(amount=0.50)
        )
        
        add_ad_group_criterions_request = AddAdGroupCriterionsRequest(
            ad_group_criterions=[biddable_ad_group_criterion],
            criterion_type=AdGroupCriterionType.WEBPAGE
        )
        
        add_ad_group_criterions_response = campaign_service.add_ad_group_criterions(
            add_ad_group_criterions_request=add_ad_group_criterions_request
        )
        
        ad_group_criterion_ids = add_ad_group_criterions_response.AdGroupCriterionIds
        print(f"Created Ad Group Criterion IDs: {ad_group_criterion_ids}")
        
        if add_ad_group_criterions_response.NestedPartialErrors:
            print(f"Nested Partial Errors: {add_ad_group_criterions_response.NestedPartialErrors}")
        
        # Add negative Webpage criterion at ad group level
        print("\nAdding negative ad group webpage criterion...")
        
        negative_webpage = Webpage(
            parameter=WebpageParameter(
                conditions=[
                    WebpageCondition(
                        operand=WebpageConditionOperand.URL,
                        argument="contoso.com"
                    )
                ]
            )
        )
        
        negative_ad_group_criterion = NegativeAdGroupCriterion(
            ad_group_id=ad_group_ids[0],
            criterion=negative_webpage
        )
        
        add_negative_ad_group_request = AddAdGroupCriterionsRequest(
            ad_group_criterions=[negative_ad_group_criterion],
            criterion_type=AdGroupCriterionType.WEBPAGE
        )
        
        add_negative_ad_group_response = campaign_service.add_ad_group_criterions(
            add_ad_group_criterions_request=add_negative_ad_group_request
        )
        
        print(f"Created Negative Ad Group Criterion IDs: {add_negative_ad_group_response.AdGroupCriterionIds}")
        
        if add_negative_ad_group_response.NestedPartialErrors:
            print(f"Nested Partial Errors: {add_negative_ad_group_response.NestedPartialErrors}")
        
        # Add negative Webpage criterion at campaign level
        # The negative Webpage criterion at the campaign level applies to all ad groups
        # within the campaign; however, if you define ad group level negative Webpage criterion,
        # the campaign criterion is ignored for that ad group.
        print("\nAdding negative campaign webpage criterion...")
        
        negative_campaign_webpage = Webpage(
            parameter=WebpageParameter(
                conditions=[
                    WebpageCondition(
                        operand=WebpageConditionOperand.URL,
                        argument="contoso.com\\seattle"
                    )
                ],
                criterion_name="Negative Campaign Criterion"
            )
        )
        
        negative_campaign_criterion = NegativeCampaignCriterion(
            campaign_id=campaign_ids[0],
            criterion=negative_campaign_webpage
        )
        
        add_campaign_criterions_request = AddCampaignCriterionsRequest(
            campaign_criterions=[negative_campaign_criterion],
            criterion_type=CampaignCriterionType.WEBPAGE
        )
        
        add_campaign_criterions_response = campaign_service.add_campaign_criterions(
            add_campaign_criterions_request=add_campaign_criterions_request
        )
        
        print(f"Created Campaign Criterion IDs: {add_campaign_criterions_response.CampaignCriterionIds}")
        
        if add_campaign_criterions_response.NestedPartialErrors:
            print(f"Nested Partial Errors: {add_campaign_criterions_response.NestedPartialErrors}")
        
        # Add at least one DynamicSearchAd into the ad group
        # The ad title and display URL are generated automatically based on the 
        # website domain and language that you want to target.
        print("\nAdding dynamic search ad...")
        
        dynamic_search_ad = DynamicSearchAd(
            text="Find New Customers & Increase Sales! Start Advertising on Contoso Today.",
            path1="seattle",
            path2="shoe sale"
            # You cannot set FinalUrls for dynamic search ads.
            # The Final URL will be a dynamically selected landing page.
            # The final URL is distinct from the path that customers will see and click on in your ad.
        )
        
        add_ads_request = AddAdsRequest(
            ad_group_id=ad_group_ids[0],
            ads=[dynamic_search_ad]
        )
        
        add_ads_response = campaign_service.add_ads(
            add_ads_request=add_ads_request
        )
        
        ad_ids = add_ads_response.AdIds
        print(f"Created Ad IDs: {ad_ids}")
        
        if add_ads_response.PartialErrors:
            print(f"Partial Errors: {add_ads_response.PartialErrors}")
        
        # Clean up - delete the campaign and everything it contains
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