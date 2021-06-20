from auth_helper import *
from adinsight_example_helper import *
from bulk_service_manager_helper import *
from output_helper import *

# You must provide credentials in auth_helper.py.

DOMAIN_NAME="contoso.com"
LANGUAGE="EN"

def get_ad_group_webpage_positive_custom_label_example(ad_group_id):
    bulk_ad_group_dynamic_search_ad_target=BulkAdGroupDynamicSearchAdTarget()
    biddable_ad_group_criterion=set_elements_to_none(campaign_service.factory.create('BiddableAdGroupCriterion'))
    biddable_ad_group_criterion.Type='BiddableAdGroupCriterion'
    biddable_ad_group_criterion.AdGroupId=ad_group_id
    fixed_bid=set_elements_to_none(campaign_service.factory.create('FixedBid'))
    fixed_bid.Amount=0.45
    biddable_ad_group_criterion.CriterionBid=fixed_bid
    conditions=campaign_service.factory.create('ArrayOfWebpageCondition')
    condition=set_elements_to_none(campaign_service.factory.create('WebpageCondition'))
    condition.Operand='CustomLabel'
    condition.Argument='Label_1_3001'
    conditions.WebpageCondition.append(condition)
    webpage_parameter=set_elements_to_none(campaign_service.factory.create('WebpageParameter'))
    webpage_parameter.Conditions=conditions
    webpage_parameter.CriterionName='Ad Group Webpage Positive Custom Label Criterion'
    webpage=set_elements_to_none(campaign_service.factory.create('Webpage'))
    webpage.Type='Webpage'
    webpage.Parameter=webpage_parameter
    biddable_ad_group_criterion.Criterion=webpage
    bulk_ad_group_dynamic_search_ad_target.biddable_ad_group_criterion=biddable_ad_group_criterion

    return bulk_ad_group_dynamic_search_ad_target

def get_ad_group_webpage_positive_category_example(ad_group_id, category_name):
    bulk_ad_group_dynamic_search_ad_target=BulkAdGroupDynamicSearchAdTarget()
    biddable_ad_group_criterion=set_elements_to_none(campaign_service.factory.create('BiddableAdGroupCriterion'))
    biddable_ad_group_criterion.Type='BiddableAdGroupCriterion'
    biddable_ad_group_criterion.AdGroupId=ad_group_id
    fixed_bid=set_elements_to_none(campaign_service.factory.create('FixedBid'))
    fixed_bid.Amount=0.50
    biddable_ad_group_criterion.CriterionBid=fixed_bid
    conditions=campaign_service.factory.create('ArrayOfWebpageCondition')
    condition=set_elements_to_none(campaign_service.factory.create('WebpageCondition'))
    condition.Argument=category_name
    condition.Operand='Category'
    conditions.WebpageCondition.append(condition)
    webpage_parameter=set_elements_to_none(campaign_service.factory.create('WebpageParameter'))
    webpage_parameter.Conditions=conditions
    webpage_parameter.CriterionName='Ad Group Webpage Positive Category Criterion'
    webpage=set_elements_to_none(campaign_service.factory.create('Webpage'))
    webpage.Type='Webpage'
    webpage.Parameter=webpage_parameter
    biddable_ad_group_criterion.Criterion=webpage
    bulk_ad_group_dynamic_search_ad_target.biddable_ad_group_criterion=biddable_ad_group_criterion

    return bulk_ad_group_dynamic_search_ad_target

def get_ad_group_webpage_negative_url_example(ad_group_id):
    bulk_ad_group_negative_dynamic_search_ad_target=BulkAdGroupNegativeDynamicSearchAdTarget()
    negative_ad_group_criterion=set_elements_to_none(campaign_service.factory.create('NegativeAdGroupCriterion'))
    negative_ad_group_criterion.Type='NegativeAdGroupCriterion'
    negative_ad_group_criterion.AdGroupId=ad_group_id    
    # You can choose whether you want the criterion argument to match partial URLs, 
    # page content, page title, or categories that Bing thinks applies to your website.
    conditions=campaign_service.factory.create('ArrayOfWebpageCondition')
    condition=set_elements_to_none(campaign_service.factory.create('WebpageCondition'))
    condition.Operand='Url'
    condition.Argument="https://{0}/3001".format(DOMAIN_NAME)
    conditions.WebpageCondition.append(condition)
    webpage_parameter=set_elements_to_none(campaign_service.factory.create('WebpageParameter'))
    webpage_parameter.Conditions=conditions
    # If you do not specify any name, then it will be set to a concatenated list of conditions. 
    webpage_parameter.CriterionName=None
    webpage=set_elements_to_none(campaign_service.factory.create('Webpage'))
    webpage.Type='Webpage'
    webpage.Parameter=webpage_parameter
    negative_ad_group_criterion.Criterion=webpage
    bulk_ad_group_negative_dynamic_search_ad_target.negative_ad_group_criterion=negative_ad_group_criterion

    return bulk_ad_group_negative_dynamic_search_ad_target

def main(authorization_data):

    try:
        
        upload_entities=[]

        # Setup a page feed that can be associated with one or more campaigns. 

        bulk_feed=BulkFeed()        
        bulk_feed.name="My PageFeed " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        bulk_feed.id=FEED_ID_KEY
        bulk_feed.status='Active' 
        bulk_feed.sub_type='PageFeed'
        custom_attribute_0={}
        custom_attribute_0['feedAttributeType']='Url'
        custom_attribute_0['name']='Page Url'
        custom_attribute_0['isPartOfKey']=True
        custom_attribute_1={}
        custom_attribute_1['feedAttributeType']='StringList'
        custom_attribute_1['name']='Custom Label'
        bulk_feed.custom_attributes=[]
        bulk_feed.custom_attributes.append(custom_attribute_0)
        bulk_feed.custom_attributes.append(custom_attribute_1)
                
        upload_entities.append(bulk_feed)

        bulk_feed_item=BulkFeedItem()        
        bulk_feed_item.feed_id=FEED_ID_KEY
        feed_item_custom_attributes_string='{"Page Url":"https://' + DOMAIN_NAME + '/3001",' + \
            '"Custom Label":["Label_1_3001","Label_2_3001"]}'
        bulk_feed_item.custom_attributes=feed_item_custom_attributes_string
        bulk_feed_item.status='Active'

        upload_entities.append(bulk_feed_item)

        # To get started with dynamic search ads, first you'll need to add a new Search campaign 
        # Include a DynamicSearchAdsSetting that specifies the target website domain and language.
        # Page feeds can be associated at the campaign level via 'Source' and 'Page Feed Ids'.

        bulk_campaign=BulkCampaign()
        campaign=set_elements_to_none(campaign_service.factory.create('Campaign'))
        campaign.BudgetType='DailyBudgetStandard'
        campaign.CampaignType=['Search']
        campaign.DailyBudget=50
        languages=campaign_service.factory.create('ns3:ArrayOfstring')
        languages.string.append('All')
        campaign.Languages=languages
        campaign.Name="Summer Sunglasses " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        settings=campaign_service.factory.create('ArrayOfSetting')
        setting=set_elements_to_none(campaign_service.factory.create('DynamicSearchAdsSetting'))
        # Set the target website domain and language.
        # Be sure to set the Source to AdvertiserSuppliedUrls or All, 
        # otherwise the PageFeedIds will be ignored. 
        setting.DomainName=DOMAIN_NAME
        setting.Language=LANGUAGE
        setting.Source='All'
        page_feed_ids=campaign_service.factory.create('ns3:ArrayOflong')
        page_feed_ids.long.append(FEED_ID_KEY)
        setting.PageFeedIds=page_feed_ids
        settings.Setting.append(setting)
        campaign.Settings=settings
        campaign.TimeZone='PacificTimeUSCanadaTijuana'
        campaign.Id=CAMPAIGN_ID_KEY
        bulk_campaign.campaign=campaign       
        upload_entities.append(bulk_campaign)

        # Create a new ad group with type set to "SearchDynamic"
        
        bulk_ad_group=BulkAdGroup()
        bulk_ad_group.campaign_id=CAMPAIGN_ID_KEY
        ad_group=set_elements_to_none(campaign_service.factory.create('AdGroup'))
        ad_group.Id=AD_GROUP_ID_KEY
        ad_group.AdGroupType='SearchDynamic'
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

        # Create an auto target based on the custom label feed items created above e.g., "Label_1_3001".
        
        ad_group_webpage_positive_custom_label=get_ad_group_webpage_positive_custom_label_example(AD_GROUP_ID_KEY)
        upload_entities.append(ad_group_webpage_positive_custom_label)

        # To discover the categories that you can use for Webpage criterion (positive or negative), 
        # use the GetDomainCategories operation with the Ad Insight service.

        output_status_message("-----\nGetDomainCategories:")
        categories=adinsight_service.GetDomainCategories(
            CategoryName=None,
            DomainName=DOMAIN_NAME,
            Language=LANGUAGE
        )
        output_status_message("DomainCategories:")
        output_array_of_domaincategory(categories)

        # If any categories are available let's use one as a condition.
        if(categories is not None and len(categories) > 0):
            ad_group_webpage_positive_category=get_ad_group_webpage_positive_category_example(
                AD_GROUP_ID_KEY, 
                categories['DomainCategory'][0].CategoryName
                )
            upload_entities.append(ad_group_webpage_positive_category)

        # If you want to exclude certain portions of your website, you can add negative Webpage 
        # criterion at the campaign and ad group level. 

        ad_group_webpage_negative_url=get_ad_group_webpage_negative_url_example(AD_GROUP_ID_KEY)
        upload_entities.append(ad_group_webpage_negative_url)

        # Finally you must add at least one DynamicSearchAd into the ad group. The ad title and display URL 
        # are generated automatically based on the website domain and language that you want to target.

        bulk_dynamic_search_ad=BulkDynamicSearchAd()
        bulk_dynamic_search_ad.ad_group_id=AD_GROUP_ID_KEY
        dynamic_search_ad=set_elements_to_none(campaign_service.factory.create('DynamicSearchAd'))
        dynamic_search_ad.Text='Find New Customers & Increase Sales!'
        dynamic_search_ad.TextPart2='Start Advertising on Contoso Today.'
        dynamic_search_ad.Path1='seattle'
        dynamic_search_ad.Path2='shoe sale'
        dynamic_search_ad.Type='DynamicSearch'
        # You cannot set FinalUrls for dynamic search ads. 
        # The Final URL will be a dynamically selected landing page.
        # The final URL is distinct from the path that customers will see and click on in your ad.
        dynamic_search_ad.FinalUrls=None
        bulk_dynamic_search_ad.ad=dynamic_search_ad
        upload_entities.append(bulk_dynamic_search_ad)
                 
        # Upload and write the output
        
        output_status_message("-----\nAdding page feed, campaign, ad group, criterions, and ads...")
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
            if isinstance(entity, BulkDynamicSearchAd):
                output_bulk_dynamic_search_ads([entity])
            if isinstance(entity, BulkAdGroupDynamicSearchAdTarget):
                output_bulk_ad_group_dynamic_search_ad_targets([entity])
            if isinstance(entity, BulkAdGroupNegativeDynamicSearchAdTarget):
                output_bulk_ad_group_negative_dynamic_search_ad_targets([entity])

        # Delete the feed and campaign and everything it contains e.g., ad groups and ads.
                
        upload_entities=[]

        for feed_result in feed_results:
            feed_result.status='Deleted'
            upload_entities.append(feed_result)

        for campaign_result in campaign_results:
            campaign_result.campaign.Status='Deleted'
            upload_entities.append(campaign_result)
            
        output_status_message("-----\nDeleting page feed, DSA campaign, and all contained entities...")
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

    adinsight_service=ServiceClient(
        service='AdInsightService', 
        version=13,
        authorization_data=authorization_data, 
        environment=ENVIRONMENT,
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
