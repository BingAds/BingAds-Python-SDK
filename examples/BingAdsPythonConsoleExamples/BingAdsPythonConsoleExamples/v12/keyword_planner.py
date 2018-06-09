from auth_helper import *
from output_helper import *
from adinsight_example_helper import *

# You must provide credentials in auth_helper.py.

def main(authorization_data):

    try:

        # You must specify the attributes that you want in each returned KeywordIdea.

        ideas_attributes=adinsight_service.factory.create('ns2:ArrayOfKeywordIdeaAttribute')
        ideas_attributes.KeywordIdeaAttribute.append([
            'AdGroupId',
            'AdGroupName',
            'AdImpressionShare',
            'Competition',
            'Keyword',
            'MonthlySearchCounts',
            'Relevance',
            'Source',
            'SuggestedBid'
        ])

        # Use the GetKeywordIdeaCategories operation to get a list of valid category identifiers.
        # A category identifier will be used in the CategorySearchParameter below.
        getkeywordideacategories_response=adinsight_service.GetKeywordIdeaCategories()
        category_id=getkeywordideacategories_response['KeywordIdeaCategory'][0].CategoryId
        
        # Only one of each SearchParameter type can be specified per call.

        search_parameters=adinsight_service.factory.create('ns4:ArrayOfSearchParameter')

        '''
        Determines the start and end month for MonthlySearchCounts data returned with each KeywordIdea. 
        The date range search parameter is optional. If you do not include the DateRangeSearchParameter  
        in the GetKeywordIdeas request, then you will not be able to confirm whether the first list item  
        within MonthlySearchCounts is data for the previous month, or the month prior. If the date range is  
        specified and the most recent month's data is not yet available, then GetKeywordIdeas will return an error. 
        '''
        date_range_search_parameter=adinsight_service.factory.create('ns4:DateRangeSearchParameter')
        end_date=adinsight_service.factory.create('ns1:DayMonthAndYear')
        end_date.Day=31
        end_date.Month=12
        end_date.Year=int(strftime("%Y", gmtime()))-1

        start_date=adinsight_service.factory.create('ns1:DayMonthAndYear')
        start_date.Day=1
        start_date.Month=1
        start_date.Year=int(strftime("%Y", gmtime()))-1

        date_range_search_parameter.EndDate=end_date
        date_range_search_parameter.StartDate=start_date

        '''
        The CategorySearchParameter corresponds to filling in 'Your product category' under 
        'Search for new keywords using a phrase, website, or category' in the  
        Bing Ads web application's Keyword Planner tool. 
        One or more CategorySearchParameter, QuerySearchParameter, or UrlSearchParameter is required. 
        '''
        category_search_parameter=adinsight_service.factory.create('ns4:CategorySearchParameter')
        category_search_parameter.CategoryId=category_id

        '''
        The QuerySearchParameter corresponds to filling in 'Product or service' under 
        'Search for new keywords using a phrase, website, or category' in the  
        Bing Ads web application's Keyword Planner tool. 
        One or more CategorySearchParameter, QuerySearchParameter, or UrlSearchParameter is required. 
        When calling GetKeywordIdeas, if ExpandIdeas=false the QuerySearchParameter is required.  
        '''
        query_search_parameter=adinsight_service.factory.create('ns4:QuerySearchParameter')
        queries=adinsight_service.factory.create('ns7:ArrayOfstring')
        queries.string.append([
            'tennis',
            'tennis shoes',
            'running',
            'running shoes',
            'cross training',
            'running',
        ])
        query_search_parameter.Queries=queries

        '''
        UrlSearchParameter
        The UrlSearchParameter corresponds to filling in 'Your landing page' under
        'Search for new keywords using a phrase, website, or category' in the 
        Bing Ads web application's Keyword Planner tool.
        One or more CategorySearchParameter, QuerySearchParameter, or UrlSearchParameter is required.
        '''
        url_search_parameter=adinsight_service.factory.create('ns4:UrlSearchParameter')
        url_search_parameter.Url='contoso.com'

        '''
        The LanguageSearchParameter, LocationSearchParameter, and NetworkSearchParameter 
        correspond to the 'Keyword Planner' -> 'Search for new keywords using a phrase, website, or category' -> 
        'Targeting' workflow in the Bing Ads web application. 
        Each of these search parameters are required. 
        '''
        language_search_parameter=adinsight_service.factory.create('ns4:LanguageSearchParameter')
        languages=adinsight_service.factory.create('ns3:ArrayOfLanguageCriterion')
        language=adinsight_service.factory.create('ns3:LanguageCriterion')
        # You must specify exactly one language
        language.Language='English'
        languages.LanguageCriterion.append([language])
        language_search_parameter.Languages=languages

        location_search_parameter=adinsight_service.factory.create('ns4:LocationSearchParameter')
        locations=adinsight_service.factory.create('ns3:ArrayOfLocationCriterion')
        # You must specify between 1 and 100 locations
        location=adinsight_service.factory.create('ns3:LocationCriterion')
        # United States
        location.LocationId='190'
        locations.LocationCriterion.append([location])
        location_search_parameter.Locations=locations

        network_search_parameter=adinsight_service.factory.create('ns4:NetworkSearchParameter')
        network=adinsight_service.factory.create('ns3:NetworkCriterion')
        network.Network='OwnedAndOperatedAndSyndicatedSearch'
        network_search_parameter.Network=network

        '''
        The CompetitionSearchParameter, ExcludeAccountKeywordsSearchParameter, IdeaTextSearchParameter,  
        ImpressionShareSearchParameter, SearchVolumeSearchParameter, and SuggestedBidSearchParameter   
        correspond to the 'Keyword Planner' -> 'Search for new keywords using a phrase, website, or category' ->  
        'Search options' workflow in the Bing Ads web application. 
        Use these options to refine what keywords we suggest. You can limit the keywords by historical data,  
        hide keywords already in your account, and include or exclude specific keywords. 
        Each of these search parameters are optional. 
        '''

        competition_search_parameter=adinsight_service.factory.create('ns4:CompetitionSearchParameter')
        competition_levels=adinsight_service.factory.create('ns2:ArrayOfCompetitionLevel')
        competition_levels.CompetitionLevel.append([
            'High',
            'Medium',
            'Low'])
        competition_search_parameter.CompetitionLevels=competition_levels

        exclude_account_keyword_search_parameter=adinsight_service.factory.create('ns4:ExcludeAccountKeywordsSearchParameter')
        exclude_account_keyword_search_parameter.ExcludeAccountKeywords=False

        idea_text_search_parameter=adinsight_service.factory.create('ns4:IdeaTextSearchParameter')
        excluded_list=adinsight_service.factory.create('ns2:ArrayOfKeyword')
        excluded_keyword1=adinsight_service.factory.create('ns2:Keyword')
        # The match type is required. Only Broad is supported.
        excluded_keyword1.MatchType='Broad'
        excluded_keyword1.Text='tennis court'
        excluded_list.Keyword.append([excluded_keyword1])
        excluded_keyword2=adinsight_service.factory.create('ns2:Keyword')
        excluded_keyword2.MatchType='Broad'
        excluded_keyword2.Text='tennis pro'
        excluded_list.Keyword.append([excluded_keyword2])

        included_list=adinsight_service.factory.create('ns2:ArrayOfKeyword')
        included_keyword1=adinsight_service.factory.create('ns2:Keyword')
        included_keyword1.MatchType='Broad'
        included_keyword1.Text='athletic clothing'
        included_list.Keyword.append([included_keyword1])
        included_keyword2=adinsight_service.factory.create('ns2:Keyword')
        included_keyword2.MatchType='Broad'
        included_keyword2.Text='athletic shoes'
        included_list.Keyword.append([included_keyword2])

        idea_text_search_parameter.Excluded=excluded_list
        idea_text_search_parameter.Included=included_list

        # Equivalent of '0 <= value <= 50'
        impression_share_search_parameter=adinsight_service.factory.create('ns4:ImpressionShareSearchParameter')
        impression_share_search_parameter.Maximum='50'
        impression_share_search_parameter.Minimum='0'

        # Equivalent of 'value >= 50'
        search_volume_search_parameter=adinsight_service.factory.create('ns4:SearchVolumeSearchParameter')
        search_volume_search_parameter.Maximum=None
        search_volume_search_parameter.Minimum='50'

        # Equivalent of both 'value <= 50' and '0 <= value <= 50'
        suggested_bid_search_parameter=adinsight_service.factory.create('ns4:SuggestedBidSearchParameter')
        suggested_bid_search_parameter.Maximum='50'
        suggested_bid_search_parameter.Minimum=None

        '''
        Setting the device criterion is not available in the  
        'Keyword Planner' -> 'Search for new keywords using a phrase, website, or category' 
        workflow in the Bing Ads web application. 
        The DeviceSearchParameter is optional and by default the keyword ideas data 
        are aggregated for all devices. 
        '''
        device_search_parameter=adinsight_service.factory.create('ns4:DeviceSearchParameter')
        device=adinsight_service.factory.create('ns3:DeviceCriterion')
        # Possible values are All, Computers, Tablets, Smartphones
        device.DeviceName='All'
        device_search_parameter.Device=device

        # Populate ArrayOfSearchParameter
        search_parameters.SearchParameter.append([
            date_range_search_parameter,
            category_search_parameter,
            query_search_parameter,
            url_search_parameter,
            language_search_parameter,
            location_search_parameter,
            network_search_parameter,
            competition_search_parameter,
            exclude_account_keyword_search_parameter,
            idea_text_search_parameter,
            impression_share_search_parameter,
            search_volume_search_parameter,
            suggested_bid_search_parameter,
            device_search_parameter
        ])
        
        # If ExpandIdeas is false, the QuerySearchParameter is required.
        get_keyword_ideas_response=adinsight_service.GetKeywordIdeas(
            IdeaAttributes=ideas_attributes,
            SearchParameters=search_parameters,
            ExpandIdeas=True
        )

        keyword_ideas=get_keyword_ideas_response
        output_array_of_keywordidea(keyword_ideas)
        
        '''
        Let's get traffic estimates for each returned keyword idea.

        The returned ad group ID within each keyword idea will either be null or negative.
        Negative identifiers can be used to map the keyword ideas into suggested new ad groups. 
        A null ad group identifier indicates that the keyword idea was sourced from your 
        keyword idea search parameter.

        In this example we will use the suggested ad groups to request traffic estimates.
        Each of the seed keyword ideas will be submitted in the same ad group.
        '''

        ad_group_ids=[]
        for keyword_idea in keyword_ideas['KeywordIdea']:
            ad_group_ids.append(keyword_idea.AdGroupId)
        distinct_ad_group_ids=list(set(ad_group_ids))
        ad_group_estimator_count=len(distinct_ad_group_ids)
        seed_offset=0 if distinct_ad_group_ids.__contains__(None) else 1

        ad_group_estimators=adinsight_service.factory.create('ns1:ArrayOfAdGroupEstimator')

        for index in range(0, ad_group_estimator_count):
            ad_group_estimator=adinsight_service.factory.create('ns1:AdGroupEstimator')
            # The AdGroupId is reserved for future use.
            # The traffic estimates are not based on any specific ad group.
            ad_group_estimator.AdGroupId=None
            # Optionally you can set an ad group level max CPC (maximum search bid)
            ad_group_estimator.MaxCpc='5.00'
            # We will add new keyword estimators while iterating the keyword ideas below.
            ad_group_estimator.KeywordEstimators=adinsight_service.factory.create('ns1:ArrayOfKeywordEstimator')
            ad_group_estimators.AdGroupEstimator.append(ad_group_estimator)

        for keyword_idea in keyword_ideas['KeywordIdea']:
            keyword_estimator=adinsight_service.factory.create('ns1:KeywordEstimator')
            keyword=adinsight_service.factory.create('ns2:Keyword')
            # The keyword Id is reserved for future use.
            # The returned estimates are not based on any specific keyword.
            keyword.Id=None
            # The match type is required. Exact, Broad, and Phrase are supported.
            keyword.MatchType='Exact'
            # Use the suggested keyword.
            keyword.Text=keyword_idea.Keyword
            keyword_estimator.Keyword=keyword
            # Round the suggested bid to two decimal places
            keyword_estimator.MaxCpc = keyword_idea.SuggestedBid if keyword_idea.SuggestedBid > 0.04 else None

            index = (keyword_idea.AdGroupId * -1) - seed_offset if keyword_idea.AdGroupId is not None else 0
            ad_group_estimators['AdGroupEstimator'][index].KeywordEstimators.KeywordEstimator.append(keyword_estimator)
        
        # Currently you can include only one CampaignEstimator per service call.
        campaign_estimators=adinsight_service.factory.create('ns1:ArrayOfCampaignEstimator')
        campaign_estimator=adinsight_service.factory.create('ns1:CampaignEstimator')
        
        # Let's use the ad group and keyword estimators that were sourced from keyword ideas above.
        campaign_estimator.AdGroupEstimators = ad_group_estimators

        # The CampaignId is reserved for future use.
        # The returned estimates are not based on any specific campaign.
        campaign_estimator.CampaignId = None

        campaign_estimator.DailyBudget = 50.00

        negative_keyword_estimators=adinsight_service.factory.create('ns1:ArrayOfKeywordEstimator')
        negative_keywords_list=adinsight_service.factory.create('ns2:ArrayOfNegativeKeyword')
        negative_keyword=adinsight_service.factory.create('ns2:NegativeKeyword')
        negative_keyword.MatchType='Exact'
        negative_keyword.Text='foo'
        negative_keywords_list.NegativeKeyword.append([negative_keyword])
        negative_keyword_estimators.KeywordEstimator=negative_keywords_list

        campaign_estimator.NegativeKeywords=negative_keyword_estimators

        # The location, language, and network criterions are required for traffic estimates.
        traffic_criteria=adinsight_service.factory.create('ns3:ArrayOfCriterion')

        # You must specify between 1 and 100 locations
        traffic_location=adinsight_service.factory.create('ns3:LocationCriterion')
        # United States
        traffic_location.LocationId='190'

        # You must specify exactly one language criterion
        traffic_language=adinsight_service.factory.create('ns3:LanguageCriterion')
        traffic_language.Language='English'

        # You must specify exactly one network criterion
        traffic_network=adinsight_service.factory.create('ns3:NetworkCriterion')
        traffic_network.Network='OwnedAndOperatedAndSyndicatedSearch'

        # Optionally you can specify exactly one device.
        # If you do not specify a device, the returned traffic estimates 
        # are aggregated for all devices.
        # The "All" device name is equivalent to omitting the DeviceCriterion.
        traffic_device=adinsight_service.factory.create('ns3:DeviceCriterion')
        traffic_device.DeviceName='All'

        traffic_criteria.Criterion.append([
            traffic_location,
            traffic_language,
            traffic_network,
            traffic_device
        ])
        campaign_estimator.Criteria=traffic_criteria
        campaign_estimators.CampaignEstimator.append(campaign_estimator)

        get_keyword_traffic_estimates_response=adinsight_service.GetKeywordTrafficEstimates(
            CampaignEstimators=campaign_estimators)

        output_array_of_campaignestimate(get_keyword_traffic_estimates_response)

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

    adinsight_service=ServiceClient(
        service='AdInsightService',
        authorization_data=authorization_data,
        environment=ENVIRONMENT,
        version=12
    )

    # You should authenticate for Bing Ads production services with a Microsoft Account.
        
    authenticate(authorization_data)
        
    main(authorization_data)