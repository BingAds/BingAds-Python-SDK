from auth_helper import *
from bingads.v13.bulk import *
from openapi_client.models.campaign import *

def main(authorization_data):
    try:
        # Download all remarketing lists
        print("Downloading all remarketing lists...")
        
        download_parameters = DownloadParameters(
            download_entities=['RemarketingLists'],
            result_file_directory='c:/test/',
            result_file_name='download.csv',
            overwrite_result_file=True,
            last_sync_time_in_utc=None
        )
        
        download_entities = list(bulk_service_manager.download_entities(
            download_parameters=download_parameters
        ))
        
        print("Download results:")
        
        remarketing_list_results = []
        
        for entity in download_entities:
            if isinstance(entity, BulkRemarketingList):
                remarketing_list_results.append(entity)
                if entity.remarketing_list:
                    print(f"  Remarketing List ID: {entity.remarketing_list.Id}, Name: {entity.remarketing_list.Name}")
        
        print(f"\nFound {len(remarketing_list_results)} remarketing lists")
        
        # You must have at least one remarketing list
        if len(remarketing_list_results) < 1:
            print("\nNo remarketing lists found in the account.")
            print("Please run remarketing_lists_test.py first to create remarketing lists.")
            return
        
        # Create campaign and ad group for remarketing
        print("\nAdding campaign and ad group...")
        
        upload_entities = []
        
        # Create a BulkCampaign
        bulk_campaign = BulkCampaign()
        bulk_campaign.account_id = authorization_data.account_id
        campaign = Campaign(
            budget_type='DailyBudgetStandard',
            daily_budget=50,
            languages=['All'],
            name="Women's Shoes " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()),
            time_zone='PacificTimeUSCanadaTijuana'
        )
        bulk_campaign.campaign = campaign
        upload_entities.append(bulk_campaign)
        
        # Create a BulkAdGroup with TargetAndBid setting
        bulk_ad_group = BulkAdGroup()
        bulk_ad_group.campaign_id = -11  # Negative ID references the campaign in the same file
        
        from datetime import datetime
        current_year = datetime.now().year
        
        ad_group = AdGroup(
            name="Women's Red Shoe Sale",
            cpc_bid=Bid(amount=0.09),
            start_date=None,
            end_date=Date(day=31, month=12, year=current_year)
        )
        
        # Applicable for all remarketing lists associated with this ad group
        # TargetAndBid indicates ads will only show to people in the remarketing list
        target_setting = TargetSetting(
            details=[
                TargetSettingDetail(
                    criterion_type_group='Audience',
                    target_and_bid=True
                )
            ]
        )
        ad_group.Settings = [target_setting]
        
        bulk_ad_group.ad_group = ad_group
        upload_entities.append(bulk_ad_group)
        
        # Associate all remarketing lists with the ad group
        for bulk_remarketing_list in remarketing_list_results:
            if bulk_remarketing_list.remarketing_list and bulk_remarketing_list.remarketing_list.Id:
                bulk_ad_group_remarketing_list_association = BulkAdGroupRemarketingListAssociation()
                
                criterion = AudienceCriterion(
                    audience_id=str(bulk_remarketing_list.remarketing_list.Id),
                    audience_type='RemarketingList'
                )
                
                biddable_ad_group_criterion = BiddableAdGroupCriterion(
                    ad_group_id='-12',  # Negative ID references the ad group in the same file
                    criterion=criterion,
                    criterion_bid=BidMultiplier(multiplier=90.0),
                    status='Paused'
                )
                
                bulk_ad_group_remarketing_list_association.biddable_ad_group_criterion = biddable_ad_group_criterion
                upload_entities.append(bulk_ad_group_remarketing_list_association)
        
        print(f"Uploading campaign, ad group, and {len(remarketing_list_results)} remarketing list associations...")
        
        download_entities = list(bulk_service_manager.upload_entities(
            EntityUploadParameters(
                entities=upload_entities,
                response_mode='ErrorsAndResults'
            )
        ))
        
        print("\nUpload results:")
        
        campaign_results = []
        ad_group_results = []
        ad_group_remarketing_list_results = []
        
        for entity in download_entities:
            if isinstance(entity, BulkCampaign):
                campaign_results.append(entity)
                if entity.campaign and entity.campaign.Id:
                    print(f"Created Campaign ID: {entity.campaign.Id}, Name: {entity.campaign.Name}")
                if entity.has_errors:
                    print(f"  Errors: {entity.errors}")
            elif isinstance(entity, BulkAdGroup):
                ad_group_results.append(entity)
                if entity.ad_group and entity.ad_group.Id:
                    print(f"Created Ad Group ID: {entity.ad_group.Id}, Name: {entity.ad_group.Name}")
                if entity.has_errors:
                    print(f"  Errors: {entity.errors}")
            elif isinstance(entity, BulkAdGroupRemarketingListAssociation):
                ad_group_remarketing_list_results.append(entity)
                if entity.biddable_ad_group_criterion and entity.biddable_ad_group_criterion.Id:
                    audience_id = entity.biddable_ad_group_criterion.Criterion.AudienceId if entity.biddable_ad_group_criterion.Criterion else 'N/A'
                    multiplier = entity.biddable_ad_group_criterion.CriterionBid.Multiplier if entity.biddable_ad_group_criterion.CriterionBid else 'N/A'
                    print(f"Created Ad Group Remarketing List Association ID: {entity.biddable_ad_group_criterion.Id}, Audience ID: {audience_id}, Multiplier: {multiplier}")
                if entity.has_errors:
                    print(f"  Errors: {entity.errors}")
        
        print(f"\nSuccessfully created {len(ad_group_remarketing_list_results)} remarketing list associations")
        
        # Delete campaign (which will also delete ad group and associations)
        print("\nDeleting campaign, ad group, and ad group remarketing list associations...")
        
        upload_entities = []
        
        for campaign_result in campaign_results:
            if campaign_result.campaign:
                campaign_result.campaign.Status = 'Deleted'
            upload_entities.append(campaign_result)
        
        download_entities = list(bulk_service_manager.upload_entities(
            EntityUploadParameters(
                entities=upload_entities,
                response_mode='ErrorsAndResults'
            )
        ))
        
        print("Delete results:")
        for entity in download_entities:
            if isinstance(entity, BulkCampaign):
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
    
    bulk_service_manager = BulkServiceManager(
        authorization_data=authorization_data,
        poll_interval_in_milliseconds=5000,
        environment=ENVIRONMENT,
    )
    
    main(authorization_data)