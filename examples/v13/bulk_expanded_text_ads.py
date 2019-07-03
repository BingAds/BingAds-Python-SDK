from auth_helper import *
from bulk_service_manager_helper import *
from output_helper import *

# You must provide credentials in auth_helper.py.

def main(authorization_data):

    try:
        
        upload_entities=[]

        # Setup an ad customizer feed that can be referenced later in the ad copy. 

        bulk_feed=BulkFeed()        
        bulk_feed.name="My AdCustomizerFeed " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        bulk_feed.id=FEED_ID_KEY
        bulk_feed.status='Active' 
        bulk_feed.sub_type='AdCustomizerFeed'
        custom_attribute_0={}
        custom_attribute_0['feedAttributeType']='String'
        custom_attribute_0['name']='Product'
        custom_attribute_1={}
        custom_attribute_1['feedAttributeType']='String'
        custom_attribute_1['name']='Materials_Lightweight'
        custom_attribute_2={}
        custom_attribute_2['feedAttributeType']='String'
        custom_attribute_2['name']='Description_Lightweight'
        custom_attribute_3={}
        custom_attribute_3['feedAttributeType']='Int64'
        custom_attribute_3['name']='Finishes'
        custom_attribute_4={}
        custom_attribute_4['feedAttributeType']='Price'
        custom_attribute_4['name']='StartPrice'
        bulk_feed.custom_attributes=[]
        bulk_feed.custom_attributes.append(custom_attribute_0)
        bulk_feed.custom_attributes.append(custom_attribute_1)
        bulk_feed.custom_attributes.append(custom_attribute_2)
        bulk_feed.custom_attributes.append(custom_attribute_3)
        bulk_feed.custom_attributes.append(custom_attribute_4)
               
        upload_entities.append(bulk_feed)

        bulk_feed_item=BulkFeedItem()        
        bulk_feed_item.feed_id=FEED_ID_KEY
        feed_item_custom_attributes_string="""{"Product":"Contoso 900",\
            "Materials_Lightweight":"titanium or acetate",\
            "Description_Lightweight":"Stylish, lightweight shades",\
            "Finishes":8,\
            "StartPrice":"$24.99"}"""
        bulk_feed_item.custom_attributes=feed_item_custom_attributes_string
        daytime_ranges=[]
        monday_daytime_range=set_elements_to_none(campaign_service.factory.create('DayTime'))
        monday_daytime_range.Day='Monday'
        monday_daytime_range.StartHour=9
        monday_daytime_range.StartMinute='Zero'
        monday_daytime_range.EndHour=21
        monday_daytime_range.EndMinute='Zero'
        daytime_ranges.append(monday_daytime_range)
        bulk_feed_item.daytime_ranges=daytime_ranges
        bulk_feed_item.intent_option='PeopleIn'
        bulk_feed_item.keyword='lightweight sunglasses'
        bulk_feed_item.location_id=190
        bulk_feed_item.match_type='Broad'
        bulk_feed_item.status='Active'

        upload_entities.append(bulk_feed_item)

        # Add a search campaign.

        bulk_campaign=BulkCampaign()
        campaign=set_elements_to_none(campaign_service.factory.create('Campaign'))
        campaign.BudgetType='DailyBudgetStandard'
        campaign.DailyBudget=50
        languages=campaign_service.factory.create('ns3:ArrayOfstring')
        languages.string.append('All')
        campaign.Languages=languages
        campaign.Name="Summer Sunglasses " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        campaign.TimeZone='PacificTimeUSCanadaTijuana'
        campaign.Id=CAMPAIGN_ID_KEY
        bulk_campaign.campaign=campaign       
        upload_entities.append(bulk_campaign)

        # Add an ad group within the campaign.
        
        bulk_ad_group=BulkAdGroup()
        bulk_ad_group.campaign_id=CAMPAIGN_ID_KEY
        ad_group=set_elements_to_none(campaign_service.factory.create('AdGroup'))
        ad_group.Id=AD_GROUP_ID_KEY
        ad_group.Name="Sunglasses Sale"
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
        keyword.Text='Brand-A Sunglasses'
        bulk_keyword.keyword=keyword
        upload_entities.append(bulk_keyword) 

        bulk_expanded_text_ad=BulkExpandedTextAd()
        bulk_expanded_text_ad.ad_group_id=AD_GROUP_ID_KEY
        expanded_text_ad=set_elements_to_none(campaign_service.factory.create('ExpandedTextAd'))
        expanded_text_ad.TitlePart1='The latest {=Sunglasses.Product}s'
        expanded_text_ad.TitlePart2='In {=Sunglasses.Materials_Lightweight}'
        expanded_text_ad.TitlePart3=None
        expanded_text_ad.Text='{=Sunglasses.Description_Lightweight} in {=Sunglasses.Finishes} finishes.'
        expanded_text_ad.TextPart2='Starting at only {=Sunglasses.StartPrice}!'
        expanded_text_ad.Path1='deals'
        expanded_text_ad.Path2=None
        expanded_text_ad.Type='ExpandedText'
        final_urls=campaign_service.factory.create('ns3:ArrayOfstring')
        final_urls.string.append('https://www.contoso.com')
        expanded_text_ad.FinalUrls=final_urls
        bulk_expanded_text_ad.ad=expanded_text_ad
        upload_entities.append(bulk_expanded_text_ad)
                 
        # Upload and write the output
        
        output_status_message("-----\nAdding the ad customizer feed, campaign, ad group, keyword, and ad...")
        download_entities=write_entities_and_upload_file(
            bulk_service_manager=bulk_service_manager, 
            upload_entities=upload_entities)

        output_status_message("Upload results:")

        feed_results=[]
        campaign_results=[]

        for entity in download_entities:
            if isinstance(entity, BulkFeed):
                feed_results.append(entity)
                output_bulk_feeds([entity])
            if isinstance(entity, BulkFeedItem):
                output_bulk_feed_items([entity])
            if isinstance(entity, BulkCampaign):
                campaign_results.append(entity)
                output_bulk_campaigns([entity])
            if isinstance(entity, BulkAdGroup):
                output_bulk_ad_groups([entity])
            if isinstance(entity, BulkExpandedTextAd):
                output_bulk_expanded_text_ads([entity])
            if isinstance(entity, BulkKeyword):
                output_bulk_keywords([entity])

        # Delete the feed and campaign and everything it contains e.g., ad groups and ads. 
                
        upload_entities=[]

        for feed_result in feed_results:
            feed_result.status='Deleted'
            upload_entities.append(feed_result)

        for campaign_result in campaign_results:
            campaign_result.campaign.Status='Deleted'
            upload_entities.append(campaign_result)
            
        output_status_message("-----\nDeleting the feed and campaign and everything it contains e.g., ad groups and ads...")
        download_entities=write_entities_and_upload_file(
            bulk_service_manager=bulk_service_manager, 
            upload_entities=upload_entities)

        output_status_message("Upload results:")

        for entity in download_entities:
            if isinstance(entity, BulkFeed):
                output_bulk_feeds([entity])
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
