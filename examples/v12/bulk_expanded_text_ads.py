from auth_helper import *
from bulk_service_manager_helper import *
from output_helper import *

# You must provide credentials in auth_helper.py.

def main(authorization_data):

    errors=[]

    try:
        # Add a search campaign.

        upload_entities=[]
                
        bulk_campaign=BulkCampaign()
        bulk_campaign.client_id='YourClientIdGoesHere'
        campaign=set_elements_to_none(campaign_service.factory.create('Campaign'))
        campaign.BudgetType='DailyBudgetStandard'
        campaign.DailyBudget=50
        campaign.Description="Red shoes line."
        languages=campaign_service.factory.create('ns3:ArrayOfstring')
        languages.string.append('All')
        campaign.Languages=languages
        campaign.Name="Women's Shoes " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        campaign.TimeZone='PacificTimeUSCanadaTijuana'
        campaign.Id=CAMPAIGN_ID_KEY
        bulk_campaign.campaign=campaign       
        upload_entities.append(bulk_campaign)

        # Add an ad group within the campaign.
        
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
        bulk_ad_group.ad_group=ad_group
        upload_entities.append(bulk_ad_group)

        # Add keywords and ads within the ad group.
        
        bulk_keyword=BulkKeyword()
        bulk_keyword.ad_group_id=AD_GROUP_ID_KEY
        keyword=set_elements_to_none(campaign_service.factory.create('Keyword'))
        keyword.Bid=set_elements_to_none(campaign_service.factory.create('Bid'))
        keyword.Bid.Amount=0.47
        keyword.Param2='10% Off'
        keyword.MatchType='Broad'
        keyword.Text='Brand-A Shoes'
        bulk_keyword.keyword=keyword
        upload_entities.append(bulk_keyword) 

        bulk_expanded_text_ad=BulkExpandedTextAd()
        bulk_expanded_text_ad.ad_group_id=AD_GROUP_ID_KEY
        expanded_text_ad=set_elements_to_none(campaign_service.factory.create('ExpandedTextAd'))
        expanded_text_ad.TitlePart1='Contoso'
        expanded_text_ad.TitlePart2='Quick & Easy Setup'
        expanded_text_ad.TitlePart3='Seemless Integration'
        expanded_text_ad.Text='Find New Customers & Increase Sales!'
        expanded_text_ad.TextPart2='Start Advertising on Contoso Today.'
        expanded_text_ad.Path1='seattle'
        expanded_text_ad.Path2='shoe sale'
        expanded_text_ad.Type='ExpandedText'
        final_urls=campaign_service.factory.create('ns3:ArrayOfstring')
        final_urls.string.append('http://www.contoso.com/womenshoesale')
        expanded_text_ad.FinalUrls=final_urls
        bulk_expanded_text_ad.ad=expanded_text_ad
        upload_entities.append(bulk_expanded_text_ad)
                 
        # Upload and write the output
        
        output_status_message("-----\nAdding campaign, ad group, keyword, and ad...")
        download_entities=write_entities_and_upload_file(
            bulk_service_manager=bulk_service_manager, 
            upload_entities=upload_entities)

        output_status_message("Upload results:")

        campaign_results=[]

        for entity in download_entities:
            if isinstance(entity, BulkCampaign):
                campaign_results.append(entity)
                output_bulk_campaigns([entity])
            if isinstance(entity, BulkAdGroup):
                output_bulk_ad_groups([entity])
            if isinstance(entity, BulkExpandedTextAd):
                output_bulk_expanded_text_ads([entity])
            if isinstance(entity, BulkKeyword):
                output_bulk_keywords([entity])

        # Delete the campaign and everything it contains e.g., ad groups and ads.
                
        upload_entities=[]

        for campaign_result in campaign_results:
            campaign_result.campaign.Status='Deleted'
            upload_entities.append(campaign_result)
            
        output_status_message("-----\nDeleting the campaign and everything it contains e.g., ad groups and ads...")
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
        version=12,
        authorization_data=authorization_data, 
        environment=ENVIRONMENT,
    )

    authenticate(authorization_data)
        
    main(authorization_data)
