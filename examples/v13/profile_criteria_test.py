import uuid
from auth_helper import *
from openapi_client.models.campaign import *

def main(authorization_data):
    try:
        # Create an audience campaign
        print("Creating audience campaign...")
        
        campaign = Campaign(
            name="Women's Shoes " + str(uuid.uuid4()),
            campaign_type=CampaignType.AUDIENCE,
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
        
        # Create an ad group with target settings
        print("\nCreating ad group with target settings...")
        
        current_year = datetime.now().year
        
        # Configure target settings for profile criteria
        target_setting = TargetSetting(
            details=[
                TargetSettingDetail(
                    criterion_type_group=CriterionTypeGroup.COMPANYNAME,
                    target_and_bid=True
                ),
                TargetSettingDetail(
                    criterion_type_group=CriterionTypeGroup.INDUSTRY,
                    target_and_bid=True
                ),
                TargetSettingDetail(
                    criterion_type_group=CriterionTypeGroup.JOBFUNCTION,
                    target_and_bid=True
                )
            ]
        )
        
        ad_group = AdGroup(
            name="Women's Red Shoe Sale" + str(uuid.uuid4())[:8],
            cpc_bid=Bid(amount=0.09),
            start_date=None,
            end_date=Date(day=31, month=12, year=current_year),
            settings=[target_setting]
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
        
        # Add ad group criterions (profile criteria and negative age criterion)
        print("\nAdding ad group criterions...")
        
        criterions = []
        
        # Add ProfileCriterion for CompanyName (Microsoft)
        company_name_criterion = ProfileCriterion(
            profile_id="808251207",  # Microsoft
            profile_type=ProfileType.COMPANYNAME
        )
        
        criterions.append(
            BiddableAdGroupCriterion(
                ad_group_id=ad_group_ids[0],
                criterion=company_name_criterion,
                criterion_bid=BidMultiplier(multiplier=20.0)
            )
        )
        
        # Add ProfileCriterion for JobFunction (Engineering)
        job_function_criterion = ProfileCriterion(
            profile_id="807658477",  # Engineering
            profile_type=ProfileType.JOBFUNCTION
        )
        
        criterions.append(
            BiddableAdGroupCriterion(
                ad_group_id=ad_group_ids[0],
                criterion=job_function_criterion,
                criterion_bid=BidMultiplier(multiplier=20.0)
            )
        )
        
        # Add Negative Age Criterion (exclude ages 25-34)
        age_criterion = AgeCriterion(
            age_range=AgeRange.TWENTYFIVETOTHIRTYFOUR
        )
        
        criterions.append(
            NegativeAdGroupCriterion(
                ad_group_id=ad_group_ids[0],
                criterion=age_criterion
            )
        )
        
        add_criterions_request = AddAdGroupCriterionsRequest(
            ad_group_criterions=criterions,
            criterion_type=AdGroupCriterionType.TARGETS
        )
        
        add_criterions_response = campaign_service.add_ad_group_criterions(
            add_ad_group_criterions_request=add_criterions_request
        )
        
        criterion_ids = add_criterions_response.AdGroupCriterionIds
        print(f"Created Ad Group Criterion IDs: {criterion_ids}")
        
        if add_criterions_response.NestedPartialErrors:
            print(f"Nested Partial Errors: {add_criterions_response.NestedPartialErrors}")
        else:
            print("Ad group criterions created successfully")
        
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