# The length of the Remarketing Rule field can be large. You may need to adjust the 
# field size limit to avoid the field larger than field limit csv error.

import csv
import sys
csv.field_size_limit(sys.maxsize)

from auth_helper import *
from bulk_service_manager_helper import *
from output_helper import *

# You must provide credentials in auth_helper.py.

def main(authorization_data):

    errors=[]

    try:
        download_parameters=DownloadParameters(
            download_entities=['RemarketingLists'],
            result_file_directory=FILE_DIRECTORY,
            result_file_name=DOWNLOAD_FILE_NAME,
            overwrite_result_file=True,
            last_sync_time_in_utc=None
        )

        output_status_message("-----\nDownloading all remarketing lists that the current user can associate with ad groups...")
        download_entities=download_file(
            bulk_service_manager=bulk_service_manager, 
            download_parameters=download_parameters)
        
        output_status_message("Download results:")

        remarketing_list_results=[]

        for entity in download_entities:
            if isinstance(entity, BulkRemarketingList):
                remarketing_list_results.append(entity)
        
        output_bulk_remarketing_lists(remarketing_list_results)
        
        # You must have at least one remarketing list. 

        if len(remarketing_list_results) < 1:
            output_status_message("There are no remarketing lists in the account.")
            sys.exit(0)

        upload_entities=[]

        # Add an ad group in a campaign. The ad group will later be associated with remarketing lists.

        bulk_campaign=BulkCampaign()
        bulk_campaign.client_id='YourClientIdGoesHere'
        campaign=set_elements_to_none(campaign_service.factory.create('Campaign'))
        campaign.BudgetType='DailyBudgetStandard'
        campaign.DailyBudget=50
        languages=campaign_service.factory.create('ns3:ArrayOfstring')
        languages.string.append('All')
        campaign.Languages=languages
        campaign.Name="Women's Shoes " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        campaign.TimeZone='PacificTimeUSCanadaTijuana'
        campaign.Id=CAMPAIGN_ID_KEY
        bulk_campaign.campaign=campaign       
        upload_entities.append(bulk_campaign)

        bulk_ad_group=BulkAdGroup()
        bulk_ad_group.campaign_id=CAMPAIGN_ID_KEY
        ad_group=set_elements_to_none(campaign_service.factory.create('AdGroup'))
        ad_group.Id=AD_GROUP_ID_KEY
        ad_group.Name="Women's Red Shoe Sale"
        end_date=campaign_service.factory.create('Date')
        end_date.Day=31
        end_date.Month=12
        end_date.Year=strftime("%Y", gmtime())
        ad_group.EndDate=end_date
        cpc_bid=campaign_service.factory.create('Bid')
        cpc_bid.Amount=0.09
        ad_group.CpcBid=cpc_bid
        # Applicable for all remarketing lists that are associated with this ad group. TargetAndBid indicates 
        # that you want to show ads only to people included in the remarketing list, with the option to change
        # the bid amount. Ads in this ad group will only show to people included in the remarketing list.
        ad_group_settings=campaign_service.factory.create('ArrayOfSetting')
        ad_group_target_setting=campaign_service.factory.create('TargetSetting')
        ad_group_audience_target_setting_detail=campaign_service.factory.create('TargetSettingDetail')
        ad_group_audience_target_setting_detail.CriterionTypeGroup='Audience'
        ad_group_audience_target_setting_detail.TargetAndBid=True
        ad_group_target_setting.Details.TargetSettingDetail.append(ad_group_audience_target_setting_detail)
        ad_group_settings.Setting.append(ad_group_target_setting)
        ad_group.Settings=ad_group_settings
        bulk_ad_group.ad_group=ad_group
        upload_entities.append(bulk_ad_group)
        
        # For example, associate all of the remarketing lists with the new ad group.

        for bulk_remarketing_list in remarketing_list_results:
            if bulk_remarketing_list.remarketing_list != None and bulk_remarketing_list.remarketing_list.Id != None:
                bulk_ad_group_remarketing_list_association=BulkAdGroupRemarketingListAssociation()
                biddable_ad_group_criterion=set_elements_to_none(campaign_service.factory.create('BiddableAdGroupCriterion'))
                audience_criterion=set_elements_to_none(campaign_service.factory.create('AudienceCriterion'))
                bid_multiplier=set_elements_to_none(campaign_service.factory.create('BidMultiplier'))
                bid_multiplier.Multiplier=90.00
                audience_criterion.AudienceId=bulk_remarketing_list.remarketing_list.Id
                biddable_ad_group_criterion.Status='Paused'
                biddable_ad_group_criterion.AdGroupId=AD_GROUP_ID_KEY
                biddable_ad_group_criterion.Criterion=audience_criterion
                biddable_ad_group_criterion.CriterionBid=bid_multiplier
                bulk_ad_group_remarketing_list_association.biddable_ad_group_criterion=biddable_ad_group_criterion
                bulk_ad_group_remarketing_list_association.ClientId="MyBulkAdGroupRemarketingList " + str(bulk_remarketing_list.remarketing_list.Id)
                
                upload_entities.append(bulk_ad_group_remarketing_list_association)
    
        output_status_message("-----\nAdding campaign, ad group, and ad group remarketing list associations...")
        download_entities=write_entities_and_upload_file(
            bulk_service_manager=bulk_service_manager, 
            upload_entities=upload_entities)

        output_status_message("Upload results:")

        campaign_results=[]
        ad_group_results=[]
        ad_group_remarketing_list_results=[]

        for entity in download_entities:
            if isinstance(entity, BulkCampaign):
                campaign_results.append(entity)
                output_bulk_campaigns([entity])
            if isinstance(entity, BulkAdGroup):
                ad_group_results.append(entity)
                output_bulk_ad_groups([entity])
            if isinstance(entity, BulkAdGroupRemarketingListAssociation):
                ad_group_remarketing_list_results.append([entity])
                output_bulk_ad_group_remarketing_list_associations([entity])
        
        # Delete the campaign and everything it contains e.g., ad groups and ads.
                
        upload_entities=[]

        for campaign_result in campaign_results:
            campaign_result.campaign.Status='Deleted'
            upload_entities.append(campaign_result)
            
        output_status_message("Deleting campaign, ad group, and ad group remarketing list associations . . .")
        download_entities=write_entities_and_upload_file(
            bulk_service_manager=bulk_service_manager, 
            upload_entities=upload_entities)

        output_status_message("Upload results:")

        for entity in download_entities:
            if isinstance(entity, BulkCampaign):
                output_bulk_campaigns([entity])
    
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
