from auth_helper import *
from adinsight_example_helper import *

# You must provide credentials in auth_helper.py.

# Summary
# This example demonstrates how to get keyword ideas and traffic estimates for search advertising campaigns.

def main(authorization_data):

    try:

        getkeywordideacategories_response = adinsight_service.GetKeywordIdeaCategories()

        # You must specify the attributes that you want in each returned KeywordIdea.

        ideas_attributes = adinsight_service.factory.create('ns2:ArrayOfKeywordIdeaAttribute')
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

        # Only one of each SearchParameter type can be specified per call.

        search_parameters = adinsight_service.factory.create('ns4:ArrayOfSearchParameter')
        '''
        DateRangeSearchParameter
        Determines the start and end month for MonthlySearchCounts data returned with each KeywordIdea. 
        The date range search parameter is optional. If you do not include the DateRangeSearchParameter  
        in the GetKeywordIdeas request, then you will not be able to confirm whether the first list item  
        within MonthlySearchCounts is data for the previous month, or the month prior. If the date range is  
        specified and the most recent month's data is not yet available, then GetKeywordIdeas will return an error. 
        '''

        date_range_search_parameter = adinsight_service.factory.create('ns4:DateRangeSearchParameter')
        end_date = adinsight_service.factory.create('ns1:DayMonthAndYear')
        end_date.Day = 31
        end_date.Month = 12
        end_date.Year = int(strftime("%Y", gmtime()))-1

        start_date = adinsight_service.factory.create('ns1:DayMonthAndYear')
        start_date.Day = 1
        start_date.Month = 1
        start_date.Year = int(strftime("%Y", gmtime()))-1

        date_range_search_parameter.EndDate = end_date
        date_range_search_parameter.StartDate = start_date

        '''
        The CategorySearchParameter corresponds to filling in 'Your product category' under 
        'Search for new keywords using a phrase, website, or category' in the  
        Bing Ads web application's Keyword Planner tool. 
        One or more CategorySearchParameter, QuerySearchParameter, or UrlSearchParameter is required. 
        '''

        category_search_parameter = adinsight_service.factory.create('ns4:CategorySearchParameter')
        # Use the GetKeywordIdeaCategories operation to get a list of valid category identifiers.
        category_search_parameter.CategoryId = getkeywordideacategories_response['KeywordIdeaCategory'][0].CategoryId

        '''
        The QuerySearchParameter corresponds to filling in 'Product or service' under 
        'Search for new keywords using a phrase, website, or category' in the  
        Bing Ads web application's Keyword Planner tool. 
        One or more CategorySearchParameter, QuerySearchParameter, or UrlSearchParameter is required. 
        When calling GetKeywordIdeas, if ExpandIdeas = false the QuerySearchParameter is required.  
        '''

        query_search_parameter = adinsight_service.factory.create('ns4:QuerySearchParameter')
        queries = adinsight_service.factory.create('ns7:ArrayOfstring')
        queries.string.append([
            'tennis',
            'tennis shoes',
            'running',
            'running shoes',
            'cross training',
            'running'])
        query_search_parameter.Queries = queries


        '''
        UrlSearchParameter
        The UrlSearchParameter corresponds to filling in 'Your landing page' under
        'Search for new keywords using a phrase, website, or category' in the 
        Bing Ads web application's Keyword Planner tool.
        One or more CategorySearchParameter, QuerySearchParameter, or UrlSearchParameter is required.
        '''

        url_search_parameter = adinsight_service.factory.create('ns4:UrlSearchParameter')
        url_search_parameter.Url = 'contoso.com'

        '''
        The LanguageSearchParameter, LocationSearchParameter, and NetworkSearchParameter 
        correspond to the 'Keyword Planner' -> 'Search for new keywords using a phrase, website, or category' -> 
        'Targeting' workflow in the Bing Ads web application. 
        Each of these search parameters are required. 
        '''

        language_search_parameter = adinsight_service.factory.create('ns4:LanguageSearchParameter')
        languages = adinsight_service.factory.create('ns3:ArrayOfLanguageCriterion')
        language = adinsight_service.factory.create('ns3:LanguageCriterion')
        # You must specify exactly one language
        language.Language = 'English'
        languages.LanguageCriterion.append([language])
        language_search_parameter.Languages = languages

        location_search_parameter = adinsight_service.factory.create('ns4:LocationSearchParameter')
        locations = adinsight_service.factory.create('ns3:ArrayOfLocationCriterion')
        # You must specify between 1 and 100 locations
        location = adinsight_service.factory.create('ns3:LocationCriterion')
        # United States
        location.LocationId = '190'
        locations.LocationCriterion.append([location])
        location_search_parameter.Locations = locations

        network_search_parameter = adinsight_service.factory.create('ns4:NetworkSearchParameter')
        network = adinsight_service.factory.create('ns3:NetworkCriterion')
        network.Network = 'OwnedAndOperatedAndSyndicatedSearch'
        network_search_parameter.Network = network

        '''
        The CompetitionSearchParameter, ExcludeAccountKeywordsSearchParameter, IdeaTextSearchParameter,  
        ImpressionShareSearchParameter, SearchVolumeSearchParameter, and SuggestedBidSearchParameter   
        correspond to the 'Keyword Planner' -> 'Search for new keywords using a phrase, website, or category' ->  
        'Search options' workflow in the Bing Ads web application. 
        Use these options to refine what keywords we suggest. You can limit the keywords by historical data,  
        hide keywords already in your account, and include or exclude specific keywords. 
        Each of these search parameters are optional. 
        '''

        competition_search_parameter = adinsight_service.factory.create('ns4:CompetitionSearchParameter')
        competition_levels = adinsight_service.factory.create('ns2:ArrayOfCompetitionLevel')
        competition_levels.CompetitionLevel.append([
            'High',
            'Medium',
            'Low'])
        competition_search_parameter.CompetitionLevels = competition_levels

        # ExcludeAccountKeywordsSearchParameter
        exclude_account_keyword_search_parameter = adinsight_service.factory.create('ns4:ExcludeAccountKeywordsSearchParameter')
        exclude_account_keyword_search_parameter.ExcludeAccountKeywords = False

        # IdeaTextSearchParameter
        idea_text_search_parameter = adinsight_service.factory.create('ns4:IdeaTextSearchParameter')
        # The match type is required.Only Broad is supported.
        excluded_list = adinsight_service.factory.create('ns2:ArrayOfKeyword')
        excluded_keyword = adinsight_service.factory.create('ns2:Keyword')
        excluded_keyword.MatchType = 'Broad'
        excluded_keyword.Text = 'tennis court'
        excluded_list.Keyword.append([excluded_keyword])

        included_list = adinsight_service.factory.create('ns2:ArrayOfKeyword')
        included_keyword = adinsight_service.factory.create('ns2:Keyword')
        included_keyword.MatchType = 'Broad'
        included_keyword.Text = 'athletic clothing'
        included_list.Keyword.append([included_keyword])

        idea_text_search_parameter.Excluded = excluded_list
        idea_text_search_parameter.Included = included_list

        # ImpressionShareSearchParameter
        impression_share_search_parameter = adinsight_service.factory.create('ns4:ImpressionShareSearchParameter')
        impression_share_search_parameter.Maximum = '50'
        impression_share_search_parameter.Minimum = '0'

        # SearchVolumeSearchParameter
        search_volume_search_parameter = adinsight_service.factory.create('ns4:SearchVolumeSearchParameter')
        search_volume_search_parameter.Maximum = None
        search_volume_search_parameter.Minimum = '50'

        # SuggestedBidSearchParameter
        suggested_bid_search_parameter = adinsight_service.factory.create('ns4:SuggestedBidSearchParameter')
        suggested_bid_search_parameter.Maximum = '1000'
        suggested_bid_search_parameter.Minimum = '4'

        '''
        Setting the device criterion is not available in the  
        'Keyword Planner' -> 'Search for new keywords using a phrase, website, or category' 
        workflow in the Bing Ads web application. 
        The DeviceSearchParameter is optional and by default the keyword ideas data 
        are aggregated for all devices. 
        '''

        device_search_parameter = adinsight_service.factory.create('ns4:DeviceSearchParameter')
        device = adinsight_service.factory.create('ns3:DeviceCriterion')
        # Possible values are All, Computers, Tablets, Smartphones
        device.DeviceName = 'All'
        device_search_parameter.Device = device

        # Populate ArrayOfSearchParameter

        search_parameters.SearchParameter.append([
            category_search_parameter,
            competition_search_parameter,
            date_range_search_parameter,
            device_search_parameter,
            exclude_account_keyword_search_parameter,
            idea_text_search_parameter,
            impression_share_search_parameter,
            language_search_parameter,
            location_search_parameter,
            network_search_parameter,
            query_search_parameter,            
            search_volume_search_parameter,
            suggested_bid_search_parameter,
            url_search_parameter])

        # Call the GetKeywordIdeas Function
        # If ExpandIdeas is false, the QuerySearchParameter is required.

        get_keyword_ideas_response=adinsight_service.GetKeywordIdeas(
            IdeaAttributes=ideas_attributes,
            SearchParameters=search_parameters,
            ExpandIdeas=True
        )

        output_array_of_keywordidea(get_keyword_ideas_response)
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
        version=11
    )

    # You should authenticate for Bing Ads production services with a Microsoft Account,
    # instead of providing the Bing Ads username and password set.
    # Authentication with a Microsoft Account is currently not supported in Sandbox.

    authenticate(authorization_data)

    main(authorization_data)
