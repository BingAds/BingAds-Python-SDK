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
        
        download_entities=download_file(bulk_service_manager, download_parameters)
        remarketing_list_results=[]
        output_status_message("Downloaded all remarketing lists that the current user can associate with ad groups.\n")
        for entity in download_entities:
            if isinstance(entity, BulkRemarketingList):
                remarketing_list_results.append(entity)
        
        output_bulk_remarketing_lists(remarketing_list_results)
        
        # For this example you must already have at least one remarketing list. 
        if len(remarketing_list_results) < 1:
            output_status_message("You do not have any remarketing lists that the current user can associate with ad groups.\n")
            sys.exit(0)

        # Prepare the bulk entities that you want to upload. Each bulk entity contains the corresponding campaign management object,  
        # and additional elements needed to read from and write to a bulk file.

        bulk_campaign=BulkCampaign()
        bulk_campaign.client_id='YourClientIdGoesHere'
        campaign=set_elements_to_none(campaign_service.factory.create('Campaign'))
        campaign.Id=CAMPAIGN_ID_KEY
        campaign.Name="Summer Shoes " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        campaign.Description="Summer shoes line."
        campaign.BudgetType='DailyBudgetStandard'
        campaign.DailyBudget=10
        campaign.TimeZone='PacificTimeUSCanadaTijuana'
        campaign.Status='Paused'
        
        bulk_campaign.campaign=campaign

        bulk_ad_group=BulkAdGroup()
        
        # The client_id may be used to associate records in the bulk upload file with records in the results file. The value of this field  
        # is not used or stored by the server; it is simply copied from the uploaded record to the corresponding result record. 
        # Note: This bulk file Client Id is not related to an application Client Id for OAuth. 
        
        bulk_ad_group.client_id='YourClientIdGoesHere'
        
        bulk_ad_group.campaign_id=CAMPAIGN_ID_KEY
        ad_group=set_elements_to_none(campaign_service.factory.create('AdGroup'))

        # When using the Campaign Management service, the Id cannot be set. In the context of a BulkAdGroup, the Id is optional 
        # and may be used as a negative reference key during bulk upload. For example the same negative value set for the  
        # ad group Id will be used when associating this new ad group with a new ad group remarketing list association
        # in the bulk_ad_group_remarketing_list_association object below. 
        ad_group.Id=AD_GROUP_ID_KEY

        ad_group.Name="Women's Red Shoes"
        ad_group.AdDistribution='Search'
        end_date=campaign_service.factory.create('Date')
        end_date.Day=31
        end_date.Month=12
        end_date.Year=strftime("%Y", gmtime())
        ad_group.EndDate=end_date
        search_bid=campaign_service.factory.create('Bid')
        search_bid.Amount=0.09
        ad_group.SearchBid=search_bid
        ad_group.Language='English'
        ad_group.TrackingUrlTemplate=None

        # Applicable for all remarketing lists that are associated with this ad group. TargetAndBid indicates 
        # that you want to show ads only to people included in the remarketing list, with the option to change
        # the bid amount. Ads in this ad group will only show to people included in the remarketing list.
        ad_group.RemarketingTargetingSetting='TargetAndBid'

        bulk_ad_group.ad_group=ad_group

        upload_entities=[]
        upload_entities.append(bulk_campaign)
        upload_entities.append(bulk_ad_group)
        
        # This example associates all of the remarketing lists with the new ad group.

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
    
        output_status_message("\nAdding campaign, ad group, and ad group remarketing list associations...\n")
        download_entities=write_entities_and_upload_file(bulk_service_manager, upload_entities)

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
            

        # Delete the campaign, ad group, and ad group remarketing list associations that were previously added. 
        # The remarketing lists will not be deleted. 
        # You should remove this region if you want to view the added entities in the 
        # Bing Ads web application or another tool.
                
        upload_entities=[]

        for campaign_result in campaign_results:
            campaign_result.campaign.Status='Deleted'
            upload_entities.append(campaign_result)
            
        output_status_message("\nDeleting campaign, ad group, and ad group remarketing list associations . . .")
        download_entities=write_entities_and_upload_file(bulk_service_manager, upload_entities)

        for entity in download_entities:
            if isinstance(entity, BulkCampaign):
                output_bulk_campaigns([entity])
            
        output_status_message("Program execution completed")

    except WebFault as ex:
        output_webfault_errors(ex)
    except Exception as ex:
        output_status_message(ex)

# Main execution
if __name__ == '__main__':

    print("Python loads the web service proxies at runtime, so you will observe " \
          "a performance delay between program launch and main execution...\n")
    
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
        authorization_data=authorization_data, 
        environment=ENVIRONMENT,
        version=11,
    )
        
    # You should authenticate for Bing Ads production services with a Microsoft Account, 
    # instead of providing the Bing Ads username and password set. 
    # Authentication with a Microsoft Account is currently not supported in Sandbox.
        
    authenticate(authorization_data)
        
    main(authorization_data)